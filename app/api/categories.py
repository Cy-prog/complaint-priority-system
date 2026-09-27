from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.complaint import CategoryResponse, DepartmentResponse
from app.models import Category, Department
from app.dependencies import get_db
from typing import List

router = APIRouter()

@router.get("/categories", response_model=List[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()

@router.get("/departments", response_model=List[DepartmentResponse])
def get_departments(db: Session = Depends(get_db)):
    return db.query(Department).all()
