from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_optional_user, get_templates
from app.services.analytics_service import AnalyticsService

router = APIRouter()
analytics_service = AnalyticsService()

@router.get("/analytics", response_class=HTMLResponse)
def analytics_page(request: Request, db: Session = Depends(get_db), user = Depends(get_optional_user), templates = Depends(get_templates)):
    if not user:
        return RedirectResponse(url="/login", status_code=302)
        
    analytics_data = analytics_service.get_analytics(db)
    context = {
        "request": request,
        "user": user,
        "analytics": analytics_data.model_dump()
    }
        
    return templates.TemplateResponse(request=request, name="pages/analytics.html", context=context)
