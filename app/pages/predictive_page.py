from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_optional_user, get_templates
from app.services.predictive_service import PredictiveAnalyticsService

router = APIRouter(prefix="/predictive")
pred_service = PredictiveAnalyticsService()

@router.get("", response_class=HTMLResponse)
def predictive_dashboard_page(
    request: Request,
    db: Session = Depends(get_db),
    user = Depends(get_optional_user),
    templates = Depends(get_templates)
):
    if not user:
        return RedirectResponse(url="/login", status_code=302)

    forecast_data = pred_service.get_forecast(db, forecast_days=14)
    hotspots = pred_service.get_recurring_hotspots(db)
    seasonal = pred_service.get_seasonal_insights(db)

    context = {
        "request": request,
        "user": user,
        "forecast": forecast_data,
        "hotspots": hotspots,
        "seasonal": seasonal
    }
    return templates.TemplateResponse(request=request, name="pages/predictive.html", context=context)
