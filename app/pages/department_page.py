from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_optional_user, get_templates, get_current_dept_admin
from app.services.department_service import DepartmentService
from app.services.sla_service import SLAService
from app.models import Complaint, Category, Department

router = APIRouter(prefix="/department")
dept_service = DepartmentService()
sla_service = SLAService()

@router.get("", response_class=HTMLResponse)
def department_workspace(
    request: Request,
    db: Session = Depends(get_db),
    user = Depends(get_optional_user),
    templates = Depends(get_templates)
):
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    if user.role not in ["department_admin", "super_admin", "admin"]:
        return RedirectResponse(url="/", status_code=302)

    # If department admin has an assigned department, focus on that; else default to first
    dept_id = user.department_id or 1
    department = dept_service.get_department(dept_id, db)
    all_depts = dept_service.list_departments(db)

    officers_workload = dept_service.list_department_officers(dept_id, db)
    officers_stats = [dept_service.get_officer_workload(o.id, db) for o in officers_workload]

    dept_complaints = db.query(Complaint).filter(
        Complaint.assigned_department_id == dept_id
    ).order_by(Complaint.created_at.desc()).limit(20).all()

    sla_metrics = sla_service.get_department_sla_metrics(dept_id, db)

    context = {
        "request": request,
        "user": user,
        "department": department,
        "all_departments": all_depts,
        "officers": officers_stats,
        "complaints": dept_complaints,
        "sla_metrics": sla_metrics
    }
    return templates.TemplateResponse(request=request, name="pages/department_dashboard.html", context=context)
