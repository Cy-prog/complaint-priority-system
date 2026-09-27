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
    photo_url = None
    if resolution_photo_file and resolution_photo_file.filename:
        ext = os.path.splitext(resolution_photo_file.filename)[1]
        unique_name = f"res_{uuid.uuid4().hex[:10]}{ext}"
        file_path = os.path.join(UPLOAD_DIR, unique_name)
        with open(file_path, "wb") as f:
            content = await resolution_photo_file.read()
            f.write(content)
        photo_url = f"/uploads/{unique_name}"
        
    complaint_service.resolve_with_proof(complaint_id, resolution_notes, photo_url, user.id, db)
    return RedirectResponse(url=f"/complaints/{complaint_id}", status_code=303)

@router.get("/map", response_class=HTMLResponse)
def map_page(request: Request, db: Session = Depends(get_db), user = Depends(get_optional_user), templates = Depends(get_templates)):
    if not user:
        return RedirectResponse(url="/login", status_code=302)
        
    complaints = db.query(Complaint).order_by(Complaint.created_at.desc()).limit(150).all()
    categories = db.query(Category).filter(Category.is_active == True).all()
    
    # Gwalior Municipal Corporation (GMC) Base Coordinates (26.2183° N, 78.1828° E)
    base_lat = 26.2183
    base_lng = 78.1828
    
    # Specific Gwalior landmark anchor points
    gwalior_hubs = {
        "महाराज बाड़ा": (26.2045, 78.1578),
        "लश्कर": (26.2080, 78.1550),
        "थाटीपुर": (26.2230, 78.2180),
        "मुरार": (26.2285, 78.2290),
        "हजीरा": (26.2350, 78.1760),
        "सिटी सेंटर": (26.2025, 78.1925),
        "कलेक्ट्रेट": (26.2010, 78.1910),
        "कंपू": (26.1950, 78.1500),
        "दीनदयाल नगर": (26.2550, 78.2250),
        "फूलबाग": (26.2150, 78.1710),
        "किला गेट": (26.2310, 78.1690)
    }
    
    map_points = []
    for c in complaints:
        if c.latitude and c.longitude and c.latitude > 25.0 and c.latitude < 28.0:
            lat, lng = c.latitude, c.longitude
        else:
            # Check if area or ward matches a known Gwalior hub
            matched_hub = None
            text_to_check = f"{c.area or ''} {c.ward or ''} {c.complaint_text or ''}"
            for hub_name, coords in gwalior_hubs.items():
                if hub_name in text_to_check:
                    matched_hub = coords
                    break
                    
            h = int(hashlib.md5((c.complaint_id or str(c.id)).encode()).hexdigest(), 16)
            lat_jitter = ((h % 1000) - 500) / 25000.0
            lng_jitter = (((h // 1000) % 1000) - 500) / 25000.0
            
            if matched_hub:
                lat = matched_hub[0] + lat_jitter * 0.4
                lng = matched_hub[1] + lng_jitter * 0.4
            else:
                lat = base_lat + lat_jitter
                lng = base_lng + lng_jitter
            
        prio = c.analysis.priority if c.analysis else "LOW"
        map_points.append({
            "id": c.complaint_id,
            "lat": lat,
            "lng": lng,
            "title": c.complaint_text[:60] + "..." if len(c.complaint_text) > 60 else c.complaint_text,
            "category": c.category.name if c.category else "General",
            "priority": prio,
            "status": c.status,
            "ward": c.ward or "General",
            "area": c.area or "",
            "photo": c.evidence_photo,
            "date": c.created_at.strftime("%d-%m-%Y") if c.created_at else ""
        })
        
    context = {
        "request": request,
        "user": user,
        "categories": categories,
        "map_points": map_points
    }
    return templates.TemplateResponse(request=request, name="pages/map.html", context=context)
