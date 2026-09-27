from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class SLARecord(Base):
    __tablename__ = "sla_records"
    
    id = Column(Integer, primary_key=True)
    complaint_id = Column(Integer, ForeignKey("complaints.id"), unique=True, nullable=False)
    priority = Column(String(20), nullable=False)
    sla_deadline = Column(DateTime, nullable=False)
    is_breached = Column(Boolean, default=False)
    response_at = Column(DateTime, nullable=True)
    resolved_at = Column(DateTime, nullable=True)
    response_time_minutes = Column(Integer, nullable=True)
    resolution_time_minutes = Column(Integer, nullable=True)
    
    complaint = relationship("Complaint", back_populates="sla_record")

    def __repr__(self):
        return f"<SLARecord(id={self.id}, complaint_id={self.complaint_id}, is_breached={self.is_breached})>"
