import os
import uuid
import hashlib
from typing import Optional
from fastapi import APIRouter, Depends, Request, Form, File, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_optional_user, get_current_user, get_templates
from app.services.complaint_service import ComplaintService
from app.services.duplicate_service import DuplicateService
from app.schemas.complaint import ComplaintFilters
from app.schemas.common import PaginationParams
from app.models import Category, Department, Complaint

router = APIRouter()
complaint_service = ComplaintService()
duplicate_service = DuplicateService()

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.get("/complaints", response_class=HTMLResponse)
@router.get("/partials/complaint_rows", response_class=HTMLResponse)
def list_complaints_page(
    request: Request, 
    filters: ComplaintFilters = Depends(),
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db), 
    user = Depends(get_optional_user),
    templates = Depends(get_templates)
):
    if not user:
        return RedirectResponse(url="/login", status_code=302)
        
    paginated_response = complaint_service.list_complaints(filters, pagination, db)
    categories = db.query(Category).filter(Category.is_active == True).all()
    
    context = {
        "request": request,
        "user": user,
        "complaints": paginated_response,
        "categories": categories,
        "filters": filters
    }
    
    if "HX-Request" in request.headers:
        return templates.TemplateResponse(request=request, name="partials/complaint_rows.html", context=context)
        
    return templates.TemplateResponse(request=request, name="pages/complaint_list.html", context=context)

@router.get("/complaints/new", response_class=HTMLResponse)
def new_complaint_page(request: Request, user = Depends(get_optional_user), templates = Depends(get_templates)):
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    return templates.TemplateResponse(request=request, name="pages/complaint_new.html", context={"request": request, "user": user})

@router.post("/complaints/new")
def submit_new_complaint_page(
    request: Request,
    complaint_text: str = Form(...),
    complainant_name: Optional[str] = Form(None),
    complainant_contact: Optional[str] = Form(None),
    city: Optional[str] = Form(None),
    ward: Optional[str] = Form(None),
    area: Optional[str] = Form(None),
    state: Optional[str] = Form(None),
    pincode: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    from app.schemas.complaint import ComplaintCreate
    from app.services.analysis_service import AnalysisService
    
    data = ComplaintCreate(
        complaint_text=complaint_text,
        complainant_name=complainant_name,
        complainant_contact=complainant_contact,
        city=city,
        ward=ward,
        area=area,
        state=state,
        pincode=pincode
    )
    created = complaint_service.create_complaint(data, db, user.id)
    try:
        analysis_service = AnalysisService()
        analysis_service.analyze_complaint(created.complaint_id, db)
    except Exception:
        pass
    return RedirectResponse(url=f"/complaints/{created.complaint_id}", status_code=303)

@router.get("/complaints/{complaint_id}", response_class=HTMLResponse)
def complaint_detail_page(complaint_id: str, request: Request, db: Session = Depends(get_db), user = Depends(get_optional_user), templates = Depends(get_templates)):
    if not user:
        return RedirectResponse(url="/login", status_code=302)
        
    complaint = complaint_service.get_complaint(complaint_id, db)
    categories = db.query(Category).filter(Category.is_active == True).all()
    departments = db.query(Department).filter(Department.is_active == True).all()
    
    try:
        similar = duplicate_service.find_similar(complaint_id, db)
    except Exception:
        similar = []
        
    context = {
        "request": request,
        "user": user,
        "complaint": complaint,
        "categories": categories,
        "departments": departments,
        "similar_complaints": similar
    }
    
    return templates.TemplateResponse(request=request, name="pages/complaint_detail.html", context=context)

@router.post("/complaints/{complaint_id}/resolve")
async def resolve_with_proof_action(
    complaint_id: str,
    resolution_notes: str = Form(...),
    resolution_photo_file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    from app.core.security import validate_and_sanitize_upload
    photo_url = None
    if resolution_photo_file and resolution_photo_file.filename:
        content = await resolution_photo_file.read()
        if content:
            safe_name = validate_and_sanitize_upload(
                resolution_photo_file.filename,
                content,
                resolution_photo_file.content_type
            )
            file_path = os.path.join(UPLOAD_DIR, safe_name)
            with open(file_path, "wb") as f:
                f.write(content)
            photo_url = f"/uploads/{safe_name}"
        
    complaint_service.resolve_with_proof(complaint_id, resolution_notes, photo_url, user.id, db)
    return RedirectResponse(url=f"/complaints/{complaint_id}", status_code=303)

@router.post("/complaints/{complaint_id}/status")
def update_status_form_action(
    complaint_id: str,
    status: str = Form(...),
    notes: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    from app.schemas.complaint import ComplaintUpdate
    update_data = ComplaintUpdate(status=status, notes=notes)
    complaint_service.update_complaint(complaint_id, update_data, db, user.id)
    return RedirectResponse(url=f"/complaints/{complaint_id}?updated=true", status_code=303)

@router.post("/complaints/{complaint_id}/override")
def override_priority_form_action(
    complaint_id: str,
    new_priority: str = Form(...),
    reason: str = Form(...),
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    from app.services.priority_service import PriorityService
    from app.schemas.analysis import PriorityOverrideRequest
    p_service = PriorityService()
    req = PriorityOverrideRequest(new_priority=new_priority, reason=reason)
    p_service.override_priority(complaint_id, req, user.id, db)
    return RedirectResponse(url=f"/complaints/{complaint_id}?overridden=true", status_code=303)

@router.post("/complaints/{complaint_id}/reopen")
def reopen_complaint_form_action(
    complaint_id: str,
    reason: Optional[str] = Form("Citizen dissatisfaction with resolution"),
    db: Session = Depends(get_db),
    user = Depends(get_optional_user)
):
    complaint = complaint_service.get_complaint(complaint_id, db)
    complaint.status = "open"
    complaint.citizen_feedback_status = "reopened"
    complaint.reopen_count = (complaint.reopen_count or 0) + 1
    
    # Audit status change
    from app.models import ComplaintStatusHistory
    history = ComplaintStatusHistory(
        complaint_id=complaint.id,
        old_status="resolved",
        new_status="open",
        changed_by_user_id=user.id if user else None,
        notes=f"Reopened by citizen: {reason}"
    )
    db.add(history)
    db.commit()
    return RedirectResponse(url=f"/complaints/{complaint_id}?reopened=true", status_code=303)

@router.get("/map", response_class=HTMLResponse)
def map_page(request: Request, db: Session = Depends(get_db), user = Depends(get_optional_user), templates = Depends(get_templates)):
    if not user:
        return RedirectResponse(url="/login", status_code=302)
        
    categories = db.query(Category).filter(Category.is_active == True).all()
    from app.services.gis_service import GISService
    gis_svc = GISService()
    map_points = gis_svc.get_map_markers(db, limit=300)
    ward_summaries = gis_svc.get_ward_spatial_summary(db)
    
    context = {
        "request": request,
        "user": user,
        "categories": categories,
        "map_points": map_points,
        "ward_summaries": ward_summaries
    }
    return templates.TemplateResponse(request=request, name="pages/map.html", context=context)
