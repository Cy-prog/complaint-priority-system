from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, func
from app.core.database import Base

class SimilarComplaint(Base):
    __tablename__ = "similar_complaints"
    
    id = Column(Integer, primary_key=True)
    complaint_id = Column(Integer, ForeignKey("complaints.id"), nullable=False)
    similar_complaint_id = Column(Integer, ForeignKey("complaints.id"), nullable=False)
    similarity_score = Column(Float, nullable=False)
    detected_at = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return f"<SimilarComplaint(complaint_id={self.complaint_id}, similar_complaint_id={self.similar_complaint_id})>"
