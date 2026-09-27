from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models import Complaint, ComplaintAnalysis, PriorityOverride, AuditLog, SLARecord
from app.schemas.analysis import PriorityOverrideRequest
from app.core.exceptions import ComplaintNotFoundError
from app.core.config_loader import load_priority_config
from .sla_service import SLAService

class PriorityService:
    def __init__(self):
        self.sla_service = SLAService()
        
    def override_priority(self, complaint_id: str, override: PriorityOverrideRequest, user_id: int, db: Session) -> PriorityOverride:
        complaint = db.query(Complaint).filter(Complaint.complaint_id == complaint_id).first()
        if not complaint:
            raise ComplaintNotFoundError(f"Complaint {complaint_id} not found")
            
        analysis = db.query(ComplaintAnalysis).filter(ComplaintAnalysis.complaint_id == complaint.id).first()
        
        original_priority = analysis.priority if analysis else "unassigned"
        original_score = analysis.priority_score if analysis else 0
        
        new_score = override.new_score
        if new_score is None:
            # Map priority string to score
            score_map = {"CRITICAL": 90, "HIGH": 70, "MEDIUM": 45, "LOW": 15}
            new_score = score_map.get(override.new_priority.upper(), 50)
            
        override_record = PriorityOverride(
            complaint_id=complaint.id,
            original_priority=original_priority,
            original_score=original_score,
            new_priority=override.new_priority,
            new_score=new_score,
            changed_by_user_id=user_id,
            reason=override.reason
        )
        db.add(override_record)
        
        if analysis:
            analysis.priority = override.new_priority
            analysis.priority_score = new_score
            
        # Update or create SLA record
        sla = db.query(SLARecord).filter(SLARecord.complaint_id == complaint.id).first()
        if sla:
            priority_config = load_priority_config()
            sla_hours = 48
            if hasattr(priority_config, 'sla_policies') and override.new_priority in priority_config.sla_policies:
                sla_hours = priority_config.sla_policies[override.new_priority].resolution_hours
            base_time = complaint.created_at or datetime.utcnow()
            sla.priority = override.new_priority
            sla.sla_deadline = base_time + timedelta(hours=sla_hours)
            sla.is_breached = False
        else:
            self.sla_service.create_sla_record(complaint.id, override.new_priority, db)
            
        # Audit Log
        audit = AuditLog(
            user_id=user_id,
            action="override_priority",
            resource_type="complaint",
            resource_id=complaint.id,
            old_value={"priority": original_priority, "score": original_score},
            new_value={"priority": override.new_priority, "score": new_score},
            ip_address="127.0.0.1"
        )
        db.add(audit)
        
        db.commit()
        db.refresh(override_record)
        return override_record
