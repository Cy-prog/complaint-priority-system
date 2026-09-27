import uuid
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.core.database import Base

def generate_incident_id() -> str:
    uid = uuid.uuid4().hex[:6].upper()
    return f"INC-{uid}"

class Incident(Base):
    __tablename__ = "incidents"
    
    id = Column(Integer, primary_key=True)
    incident_id = Column(String(20), unique=True, nullable=False, default=generate_incident_id)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(20), default="active")  # active, monitoring, resolved
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    area = Column(String(200), nullable=True)
    complaint_count = Column(Integer, default=0)
    first_reported = Column(DateTime, server_default=func.now())
    last_updated = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    category = relationship("Category")
    linked_complaints = relationship("IncidentComplaint", back_populates="incident")

    def __repr__(self):
        return f"<Incident(id={self.id}, incident_id='{self.incident_id}', status='{self.status}')>"

class IncidentComplaint(Base):
    __tablename__ = "incident_complaints"
    
    id = Column(Integer, primary_key=True)
    incident_id = Column(Integer, ForeignKey("incidents.id"), nullable=False)
    complaint_id = Column(Integer, ForeignKey("complaints.id"), nullable=False)
    linked_at = Column(DateTime, server_default=func.now())
    
    incident = relationship("Incident", back_populates="linked_complaints")
    complaint = relationship("Complaint")

    def __repr__(self):
        return f"<IncidentComplaint(id={self.id}, incident_id={self.incident_id}, complaint_id={self.complaint_id})>"
