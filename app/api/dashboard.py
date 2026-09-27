from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.dashboard import DashboardSummary, AnalyticsResponse, TrendData
from app.services.analytics_service import AnalyticsService
from app.dependencies import get_db, get_current_user
from typing import List

router = APIRouter()
analytics_service = AnalyticsService()

@router.get("/summary", response_model=DashboardSummary)
def get_summary(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return analytics_service.get_dashboard_summary(db)

@router.get("/analytics", response_model=AnalyticsResponse)
def get_analytics(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return analytics_service.get_analytics(db)

@router.get("/trends", response_model=List[TrendData])
def get_trends(days: int = 30, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return analytics_service.get_complaints_trend(days, db)
