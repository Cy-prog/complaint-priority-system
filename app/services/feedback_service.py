from sqlalchemy.orm import Session
from app.models import Complaint, ComplaintFeedback
from app.schemas.analysis import FeedbackRequest
from app.core.exceptions import ComplaintNotFoundError

class FeedbackService:
    def submit_feedback(self, complaint_id: str, feedback: FeedbackRequest, user_id: int, db: Session) -> ComplaintFeedback:
        complaint = db.query(Complaint).filter(Complaint.complaint_id == complaint_id).first()
        if not complaint:
            raise ComplaintNotFoundError(f"Complaint {complaint_id} not found")
            
        new_feedback = ComplaintFeedback(
            complaint_id=complaint.id,
            feedback_type=feedback.feedback_type,
            original_value=feedback.original_value,
            corrected_value=feedback.corrected_value,
            reason=feedback.reason,
            submitted_by_user_id=user_id,
            used_for_training=False
        )
        
        db.add(new_feedback)
        db.commit()
        db.refresh(new_feedback)
        return new_feedback

    def get_feedback(self, complaint_id: str, db: Session) -> list[ComplaintFeedback]:
        complaint = db.query(Complaint).filter(Complaint.complaint_id == complaint_id).first()
        if not complaint:
            raise ComplaintNotFoundError(f"Complaint {complaint_id} not found")
            
        return db.query(ComplaintFeedback).filter(ComplaintFeedback.complaint_id == complaint.id).all()
