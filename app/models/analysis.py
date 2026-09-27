from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, JSON, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class ComplaintAnalysis(Base):
    __tablename__ = "complaint_analysis"
    
    id = Column(Integer, primary_key=True)
    complaint_id = Column(Integer, ForeignKey("complaints.id"), unique=True, nullable=False)
    priority = Column(String(20), nullable=False)
    priority_score = Column(Integer, nullable=False)
    urgency_score = Column(Integer, nullable=False, default=0)
    severity_score = Column(Integer, nullable=False, default=0)
    impact_score = Column(Integer, nullable=False, default=0)
    safety_score = Column(Integer, nullable=False, default=0)
    duration_score = Column(Integer, nullable=False, default=0)
    confidence = Column(Float, nullable=False, default=0.0)
    sentiment = Column(String(20), nullable=True)
    risk_level = Column(String(20), nullable=True)
    entities = Column(JSON, nullable=True)
    key_issues = Column(JSON, nullable=True)
    affected_population = Column(String(200), nullable=True)
    affected_population_estimate = Column(Integer, nullable=True)
    reasoning_summary = Column(Text, nullable=True)
    recommended_action = Column(Text, nullable=True)
    duplicate_probability = Column(Float, default=0.0)
    analysis_model_version = Column(String(50), nullable=True)
    analysis_latency_ms = Column(Float, nullable=True)
    analyzed_at = Column(DateTime, server_default=func.now())
    
    complaint = relationship("Complaint", back_populates="analysis")

    def __repr__(self):
        return f"<ComplaintAnalysis(id={self.id}, complaint_id={self.complaint_id}, priority='{self.priority}')>"
