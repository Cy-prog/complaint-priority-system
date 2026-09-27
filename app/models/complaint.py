import uuid
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.core.database import Base

def generate_complaint_id() -> str:
    # Use part of a UUID for uniqueness
    uid = uuid.uuid4().hex[:6].upper()
    return f"CMP-{uid}"

class Complaint(Base):
    __tablename__ = "complaints"
    
    id = Column(Integer, primary_key=True)
    complaint_id = Column(String(20), unique=True, nullable=False, index=True, default=generate_complaint_id)
    complaint_text = Column(Text, nullable=False)
    complainant_name = Column(String(100), nullable=True)
    complainant_contact = Column(String(100), nullable=True)
    language = Column(String(10), default="en")
    status = Column(String(20), default="pending", index=True)
    
    # Location fields
    state = Column(String(100), nullable=True)
    city = Column(String(100), nullable=True)
    district = Column(String(100), nullable=True)
    ward = Column(String(50), nullable=True)
    area = Column(String(200), nullable=True)
    pincode = Column(String(10), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    
    # Foreign keys
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    assigned_department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    assigned_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now(), index=True)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    resolved_at = Column(DateTime, nullable=True)
    
    # Evidence and Resolution Verification fields
    evidence_photo = Column(String(500), nullable=True)
    resolution_photo = Column(String(500), nullable=True)
    resolution_notes = Column(Text, nullable=True)
    citizen_feedback_status = Column(String(20), default="pending")  # pending, satisfied, reopened
    reopen_count = Column(Integer, default=0)
    
    # Relationships
    analysis = relationship("ComplaintAnalysis", back_populates="complaint", uselist=False)
    category = relationship("Category", back_populates="complaints")
    assigned_department = relationship("Department", back_populates="complaints")
    sla_record = relationship("SLARecord", back_populates="complaint", uselist=False)
    status_history = relationship("ComplaintStatusHistory", back_populates="complaint", order_by="ComplaintStatusHistory.changed_at.desc()")
    priority_overrides = relationship("PriorityOverride", back_populates="complaint", order_by="PriorityOverride.changed_at.desc()")
    feedbacks = relationship("ComplaintFeedback", back_populates="complaint")

    @classmethod
    def generate_id(cls, db_session) -> str:
        # Better sequential approach using DB state if preferred over UUID, but keeping simple UUID for now
        return generate_complaint_id()

    def __repr__(self):
        return f"<Complaint(id={self.id}, complaint_id='{self.complaint_id}', status='{self.status}')>"
