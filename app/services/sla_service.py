from sqlalchemy.orm import Session
from app.models import SLARecord, Complaint
from datetime import datetime, timedelta
from app.core.config_loader import load_priority_config

class SLAService:
    def create_sla_record(self, complaint_id: int, priority: str, db: Session) -> SLARecord:
        # Load SLA policies from config
        priority_config = load_priority_config()
        # Default fallback SLA in hours
        sla_hours = 48 
        
        if hasattr(priority_config, 'sla_policies') and priority in priority_config.sla_policies:
            sla_hours = priority_config.sla_policies[priority].resolution_hours
        elif isinstance(priority_config, dict) and "sla_policies" in priority_config:
            policy = priority_config["sla_policies"].get(priority, {})
            sla_hours = policy.get("resolution_hours", 48)
                
        deadline = datetime.utcnow() + timedelta(hours=sla_hours)
        
        sla = SLARecord(
            complaint_id=complaint_id,
            priority=priority,
            sla_deadline=deadline,
            is_breached=False
        )
        db.add(sla)
        db.commit()
        db.refresh(sla)
        return sla

    def check_sla_breach(self, db: Session) -> list[SLARecord]:
        now = datetime.utcnow()
        breached = db.query(SLARecord).filter(
            SLARecord.is_breached == False,
            SLARecord.resolved_at == None,
            SLARecord.sla_deadline < now
        ).all()
        
        for record in breached:
            record.is_breached = True
            
        if breached:
            db.commit()
            
        return breached

    def get_sla_status(self, complaint_id: str, db: Session) -> dict:
        complaint = db.query(Complaint).filter(Complaint.complaint_id == complaint_id).first()
        if not complaint:
            return {}
            
        sla = db.query(SLARecord).filter(SLARecord.complaint_id == complaint.id).first()
        if not sla:
            return {}
            
        now = datetime.utcnow()
        remaining = sla.sla_deadline - now if not sla.resolved_at else timedelta(0)
        
        total_allowed = (sla.sla_deadline - complaint.created_at).total_seconds()
        remaining_seconds = remaining.total_seconds()
        
        is_approaching = False
        if remaining_seconds > 0 and total_allowed > 0:
            if (remaining_seconds / total_allowed) < 0.25:
                is_approaching = True
                
        return {
            "deadline": sla.sla_deadline,
            "remaining_time_minutes": remaining_seconds / 60,
            "is_breached": sla.is_breached or (remaining_seconds < 0 and not sla.resolved_at),
            "is_approaching": is_approaching,
            "resolved_at": sla.resolved_at
        }
