from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(500), nullable=True)
    risk_level = Column(String(20), default="medium")  # low, medium, high, critical
    is_essential_service = Column(Boolean, default=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    
    department = relationship("Department", back_populates="categories")
    complaints = relationship("Complaint", back_populates="category")

    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}', risk_level='{self.risk_level}')>"
