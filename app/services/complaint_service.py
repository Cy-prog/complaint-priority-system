from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc, asc
from app.models import Complaint, ComplaintStatusHistory, ComplaintAnalysis
from app.schemas.complaint import ComplaintCreate, ComplaintUpdate, ComplaintFilters
from app.schemas.common import PaginationParams, PaginatedResponse
from app.core.exceptions import ComplaintNotFoundError
from typing import Optional

class ComplaintService:
    def create_complaint(self, data: ComplaintCreate, db: Session, user_id: Optional[int] = None) -> Complaint:
        count = db.query(Complaint).count()
        complaint_id_str = f"CMP-{count + 1:06d}"
        
        complaint = Complaint(
            complaint_id=complaint_id_str,
            complaint_text=data.complaint_text,
            complainant_name=data.complainant_name,
            complainant_contact=data.complainant_contact,
            state=data.state or "Maharashtra",
            city=data.city or "Gram Panchayat",
            district=data.district,
            ward=data.ward,
            area=data.area,
            pincode=data.pincode,
            latitude=data.latitude,
            longitude=data.longitude,
            status='pending',
            created_by_user_id=user_id
        )
        db.add(complaint)
        db.commit()
        db.refresh(complaint)
        return complaint

    def create_citizen_complaint(
        self,
        complaint_text: str,
        complainant_name: Optional[str],
        complainant_contact: Optional[str],
        ward: Optional[str],
        area: Optional[str],
        city: Optional[str],
        evidence_photo_path: Optional[str],
        db: Session
    ) -> Complaint:
        """Citizen portal submission with auto-analysis."""
        from app.services.analysis_service import AnalysisService
        
        count = db.query(Complaint).count()
        complaint_id_str = f"CMP-{count + 1:06d}"
        
        complaint = Complaint(
            complaint_id=complaint_id_str,
            complaint_text=complaint_text,
            complainant_name=complainant_name or "Anonymous Citizen",
            complainant_contact=complainant_contact,
            ward=ward,
            area=area,
            city=city or "Gram Panchayat Area",
            evidence_photo=evidence_photo_path,
            status='pending'
        )
        db.add(complaint)
        db.commit()
        db.refresh(complaint)
        
        # Trigger immediate AI analysis so citizen gets priority on their receipt!
        try:
            analysis_service = AnalysisService()
            analysis_service.analyze_complaint(complaint.complaint_id, db)
            db.refresh(complaint)
        except Exception:
            pass
            
        return complaint

    def get_complaint(self, complaint_id: str, db: Session) -> Complaint:
        complaint = db.query(Complaint).filter(Complaint.complaint_id == complaint_id).first()
        if not complaint:
            raise ComplaintNotFoundError(f"Complaint {complaint_id} not found")
        return complaint
        
    def search_by_contact_or_id(self, query_str: str, db: Session) -> list[Complaint]:
        clean_q = query_str.strip()
        return db.query(Complaint).filter(
            or_(
                Complaint.complaint_id.ilike(f"%{clean_q}%"),
                Complaint.complainant_contact.ilike(f"%{clean_q}%")
            )
        ).order_by(desc(Complaint.created_at)).all()

    def list_complaints(self, filters: ComplaintFilters, pagination: PaginationParams, db: Session) -> PaginatedResponse:
        query = db.query(Complaint)
        
        if filters.category_id:
            query = query.filter(Complaint.category_id == filters.category_id)
        if filters.status:
            query = query.filter(Complaint.status == filters.status)
        if filters.city:
            query = query.filter(Complaint.city == filters.city)
        if filters.ward:
            query = query.filter(Complaint.ward == filters.ward)
        if filters.date_from:
            query = query.filter(Complaint.created_at >= filters.date_from)
        if filters.date_to:
            query = query.filter(Complaint.created_at <= filters.date_to)
        if filters.priority:
            query = query.join(ComplaintAnalysis, Complaint.id == ComplaintAnalysis.complaint_id)\
                         .filter(ComplaintAnalysis.priority == filters.priority.upper())
        if filters.search:
            search_term = f"%{filters.search}%"
            query = query.filter(
                or_(
                    Complaint.complaint_text.ilike(search_term),
                    Complaint.complaint_id.ilike(search_term),
                    Complaint.complainant_name.ilike(search_term),
                    Complaint.ward.ilike(search_term),
                    Complaint.area.ilike(search_term)
                )
            )
            
        total = query.count()
        query = query.order_by(desc(Complaint.created_at))
        
        offset = (pagination.page - 1) * pagination.page_size
        items = query.offset(offset).limit(pagination.page_size).all()
        total_pages = (total + pagination.page_size - 1) // pagination.page_size
        
        return PaginatedResponse(
            items=items,
            total=total,
            page=pagination.page,
            page_size=pagination.page_size,
            total_pages=total_pages
        )

    def update_complaint(self, complaint_id: str, data: ComplaintUpdate, db: Session, user_id: Optional[int] = None) -> Complaint:
        complaint = self.get_complaint(complaint_id, db)
        
        old_status = complaint.status
        if data.status and data.status != old_status:
            history = ComplaintStatusHistory(
                complaint_id=complaint.id,
                old_status=old_status,
                new_status=data.status,
                changed_by_user_id=user_id,
                notes="Status updated"
            )
            db.add(history)
            
        if data.status is not None:
            complaint.status = data.status
        if data.category_id is not None:
            complaint.category_id = data.category_id
        if data.assigned_department_id is not None:
            complaint.assigned_department_id = data.assigned_department_id
        if data.assigned_user_id is not None:
            complaint.assigned_user_id = data.assigned_user_id
            
        complaint.updated_at = datetime.utcnow()
        if complaint.status in ['resolved', 'closed'] and old_status not in ['resolved', 'closed']:
            complaint.resolved_at = datetime.utcnow()
            
        db.commit()
        db.refresh(complaint)
        return complaint

    def resolve_with_proof(
        self,
        complaint_id: str,
        resolution_notes: str,
        resolution_photo_path: Optional[str],
        user_id: Optional[int],
        db: Session
    ) -> Complaint:
        complaint = self.get_complaint(complaint_id, db)
        old_status = complaint.status
        complaint.status = 'resolved'
        complaint.resolved_at = datetime.utcnow()
        complaint.updated_at = datetime.utcnow()
        complaint.resolution_notes = resolution_notes
        if resolution_photo_path:
            complaint.resolution_photo = resolution_photo_path
            
        history = ComplaintStatusHistory(
            complaint_id=complaint.id,
            old_status=old_status,
            new_status='resolved',
            changed_by_user_id=user_id,
            notes=f"Resolved with proof: {resolution_notes}"
        )
        db.add(history)
        db.commit()
        db.refresh(complaint)
        return complaint

    def verify_citizen_feedback(
        self,
        complaint_id: str,
        satisfied: bool,
        comments: Optional[str],
        db: Session
    ) -> Complaint:
        complaint = self.get_complaint(complaint_id, db)
        
        actor_id = complaint.assigned_user_id or 1
        
        if satisfied:
            old_st = complaint.status
            complaint.citizen_feedback_status = 'satisfied'
            complaint.status = 'closed'
            complaint.updated_at = datetime.utcnow()
            history = ComplaintStatusHistory(
                complaint_id=complaint.id,
                old_status=old_st,
                new_status='closed',
                changed_by_user_id=actor_id,
                notes="Citizen verified resolution: Satisfied."
            )
            db.add(history)
        else:
            complaint.citizen_feedback_status = 'reopened'
            complaint.status = 'in_progress'
            complaint.reopen_count = (complaint.reopen_count or 0) + 1
            complaint.updated_at = datetime.utcnow()
            
            # Escalate priority to CRITICAL because work was falsely marked done
            from app.services.priority_service import PriorityService
            from app.schemas.analysis import PriorityOverrideRequest
            
            try:
                priority_service = PriorityService()
                override_req = PriorityOverrideRequest(
                    new_priority="CRITICAL",
                    new_score=95,
                    reason=f"Citizen Reopened: Work not done / incomplete ({comments or 'Citizen rejected resolution'}). Auto-escalated to BDO."
                )
                priority_service.override_priority(complaint_id, override_req, actor_id, db)
            except Exception:
                pass
                
            history = ComplaintStatusHistory(
                complaint_id=complaint.id,
                old_status='resolved',
                new_status='in_progress',
                changed_by_user_id=actor_id,
                notes=f"Citizen rejected resolution: '{comments}'. Priority escalated to CRITICAL for Block/BDO intervention."
            )
            db.add(history)
            
        db.commit()
        db.refresh(complaint)
        return complaint

    def delete_complaint(self, complaint_id: str, db: Session) -> bool:
        complaint = self.get_complaint(complaint_id, db)
        complaint.status = 'closed'
        db.commit()
        return True
