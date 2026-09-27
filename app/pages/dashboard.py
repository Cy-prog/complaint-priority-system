from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_optional_user, get_templates
from app.services.analytics_service import AnalyticsService
from app.services.cluster_service import ClusterService
from app.models import Complaint

router = APIRouter()
analytics_service = AnalyticsService()
cluster_service = ClusterService()

@router.get("/", response_class=HTMLResponse)
def dashboard_page(request: Request, db: Session = Depends(get_db), user = Depends(get_optional_user), templates = Depends(get_templates)):
    if not user:
        return RedirectResponse(url="/login", status_code=302)
        
    summary = analytics_service.get_dashboard_summary(db)
    priority_dist = [
        {"priority": p.priority, "count": p.count} 
        for p in analytics_service.get_priority_distribution(db)
    ]
    category_dist = [
        {"category": c.category, "count": c.count} 
        for c in analytics_service.get_category_distribution(db)
    ]
    recent_complaints = db.query(Complaint).order_by(Complaint.created_at.desc()).limit(10).all()
    
    # Active Community Outbreak / Cluster Alerts
    active_clusters = cluster_service.detect_clusters(db)
    
    context = {
        "request": request,
        "user": user,
        "summary": summary,
        "priority_distribution": priority_dist,
        "category_distribution": category_dist,
        "recent_complaints": recent_complaints,
        "active_clusters": active_clusters
    }
    
    if "HX-Request" in request.headers and request.headers.get("HX-Target") == "kpi-cards":
        return templates.TemplateResponse(request=request, name="partials/kpi_update.html", context=context)
        
    return templates.TemplateResponse(request=request, name="pages/dashboard.html", context=context)
