from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_optional_user, get_templates
from app.models import Complaint, Category, Department
from app.services.department_service import DepartmentService

router = APIRouter(prefix="/officer")
dept_service = DepartmentService()

@router.get("", response_class=HTMLResponse)
def officer_workspace(
    request: Request,
    db: Session = Depends(get_db),
    user = Depends(get_optional_user),
    templates = Depends(get_templates)
):
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    if user.role not in ["officer", "operator", "department_admin", "super_admin", "admin"]:
        return RedirectResponse(url="/", status_code=302)

    # Fetch complaints assigned directly to this officer
    assigned_complaints = db.query(Complaint).filter(
        Complaint.assigned_user_id == user.id
    ).order_by(Complaint.created_at.desc()).all()

    # If none assigned directly, fetch unassigned or department pool
    if not assigned_complaints and user.department_id:
        assigned_complaints = db.query(Complaint).filter(
            Complaint.assigned_department_id == user.department_id
        ).order_by(Complaint.created_at.desc()).limit(15).all()

    workload = dept_service.get_officer_workload(user.id, db)

    context = {
        "request": request,
        "user": user,
        "complaints": assigned_complaints,
        "workload": workload
    }
    return templates.TemplateResponse(request=request, name="pages/officer_workspace.html", context=context)
