from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class PriorityOverride(Base):
    __tablename__ = "priority_overrides"
    
    id = Column(Integer, primary_key=True)
    complaint_id = Column(Integer, ForeignKey("complaints.id"), nullable=False)
    original_priority = Column(String(20), nullable=False)
    original_score = Column(Integer, nullable=False)
    new_priority = Column(String(20), nullable=False)
    new_score = Column(Integer, nullable=True)
    changed_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    reason = Column(Text, nullable=False)
    changed_at = Column(DateTime, server_default=func.now())
    
    complaint = relationship("Complaint", back_populates="priority_overrides")
    changed_by = relationship("User")

    def __repr__(self):
        return f"<PriorityOverride(id={self.id}, complaint_id={self.complaint_id})>"

class ComplaintStatusHistory(Base):
    __tablename__ = "complaint_status_history"
    
    id = Column(Integer, primary_key=True)
    complaint_id = Column(Integer, ForeignKey("complaints.id"), nullable=False)
    old_status = Column(String(20), nullable=False)
    new_status = Column(String(20), nullable=False)
    changed_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    notes = Column(Text, nullable=True)
    changed_at = Column(DateTime, server_default=func.now())
    
    complaint = relationship("Complaint", back_populates="status_history")
    changed_by = relationship("User")

    def __repr__(self):
        return f"<ComplaintStatusHistory(id={self.id}, complaint_id={self.complaint_id}, {self.old_status}->{self.new_status})>"

class ComplaintFeedback(Base):
    __tablename__ = "complaint_feedback"
    
    id = Column(Integer, primary_key=True)
    complaint_id = Column(Integer, ForeignKey("complaints.id"), nullable=False)
    feedback_type = Column(String(50), nullable=False)  # priority_correction, category_correction, general
    original_value = Column(String(255), nullable=True)
    corrected_value = Column(String(255), nullable=True)
    reason = Column(Text, nullable=True)
    submitted_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    used_for_training = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    
    complaint = relationship("Complaint", back_populates="feedbacks")
    submitted_by = relationship("User")

    def __repr__(self):
        return f"<ComplaintFeedback(id={self.id}, complaint_id={self.complaint_id}, type='{self.feedback_type}')>"
