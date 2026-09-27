from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from app.dependencies import get_optional_user, get_templates
from app.core.config_loader import load_priority_config, load_categories_config, load_safety_config

router = APIRouter()

@router.get("/settings", response_class=HTMLResponse)
def settings_page(request: Request, user = Depends(get_optional_user), templates = Depends(get_templates)):
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    if user.role != "admin":
        return HTMLResponse("<h1>403 Forbidden</h1><p>Requires admin privileges.</p>", status_code=403)
        
    priority_config = load_priority_config()
    categories_config = load_categories_config()
    safety_config = load_safety_config()
    
    context = {
        "request": request,
        "user": user,
        "priority_config": priority_config,
        "categories_config": categories_config,
        "safety_config": safety_config
    }
        
    return templates.TemplateResponse(request=request, name="pages/settings.html", context=context)
