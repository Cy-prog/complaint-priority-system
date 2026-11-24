import os
from typing import Optional
from fastapi import APIRouter, Depends, Request, Form, File, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_templates, get_optional_user
from app.services.complaint_service import ComplaintService
from app.core.security import validate_and_sanitize_upload
from app.models import Category, Department, Complaint

router = APIRouter(prefix="/portal")
complaint_service = ComplaintService()

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.get("", response_class=HTMLResponse)
def citizen_portal_page(
    request: Request,
    db: Session = Depends(get_db),
    user = Depends(get_optional_user),
    templates = Depends(get_templates)
):
    categories = db.query(Category).filter(Category.is_active == True).all()
    gwalior_wards = [
        "वार्ड 18 (महाराज बाड़ा / सराफा / लश्कर)",
        "वार्ड 12 (हजीरा / किला गेट / तानसेन नगर)",
        "वार्ड 34 (थाटीपुर / मयूर मार्केट / गांधी रोड)",
        "वार्ड 48 (सिटी सेंटर / कलेक्ट्रेट / बाल भवन)",
        "वार्ड 22 (लश्कर / कंपू / माधव डिस्पेंसरी)",
        "वार्ड 7 (मुरार सदर बाजार / एमएच चौराहा)",
        "वार्ड 15 (फूलबाग / पड़ाव / रेलवे स्टेशन)",
        "वार्ड 28 (दीनदयाल नगर / एयरपोर्ट रोड)",
        "वार्ड 31 (गोविंदपुरी / जीवाजी विश्वविद्यालय)",
        "वार्ड 42 (शिंदे की छावनी / नदी गेट)",
        "वार्ड 54 (पिंटो पार्क / मुरार कैंट)",
        "वार्ड 60 (आनंद नगर / बहोड़ापुर / मोतीझील)",
    ] + [f"वार्ड {i} (ग्वालियर नगर निगम)" for i in range(1, 67) if i not in [18, 12, 34, 48, 22, 7, 15, 28, 31, 42, 54, 60]]
    context = {
        "request": request,
        "user": user,
        "categories": categories,
        "wards": gwalior_wards
    }
    return templates.TemplateResponse(request=request, name="pages/citizen_portal.html", context=context)

@router.post("/submit")
async def citizen_submit(
    request: Request,
    complaint_text: str = Form(...),
    complainant_name: Optional[str] = Form(None),
    complainant_contact: Optional[str] = Form(None),
    ward: Optional[str] = Form(None),
    area: Optional[str] = Form(None),
    city: Optional[str] = Form("ग्वालियर (Gwalior)"),
    latitude: Optional[float] = Form(None),
    longitude: Optional[float] = Form(None),
    evidence_file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    user = Depends(get_optional_user)
):
    photo_url = None
    if evidence_file and evidence_file.filename:
        content = await evidence_file.read()
        if content:
            safe_name = validate_and_sanitize_upload(
                evidence_file.filename,
                content,
                evidence_file.content_type
            )
            file_path = os.path.join(UPLOAD_DIR, safe_name)
            with open(file_path, "wb") as f:
                f.write(content)
            photo_url = f"/uploads/{safe_name}"

    complaint = complaint_service.create_citizen_complaint(
        complaint_text=complaint_text,
        complainant_name=complainant_name or (user.full_name if user else None),
        complainant_contact=complainant_contact or (user.phone if user else None),
        ward=ward,
        area=area,
        city=city,
        evidence_photo_path=photo_url,
        db=db,
        latitude=latitude,
        longitude=longitude,
        user_id=user.id if user else None
    )
    
    return RedirectResponse(url=f"/portal/receipt/{complaint.complaint_id}", status_code=303)

@router.get("/receipt/{complaint_id}", response_class=HTMLResponse)
def citizen_receipt_page(
    complaint_id: str,
    request: Request,
    db: Session = Depends(get_db),
    user = Depends(get_optional_user),
    templates = Depends(get_templates)
):
    complaint = complaint_service.get_complaint(complaint_id, db)
    context = {
        "request": request,
        "user": user,
        "complaint": complaint
    }
    return templates.TemplateResponse(request=request, name="pages/citizen_receipt.html", context=context)

@router.get("/track", response_class=HTMLResponse)
def citizen_track_page(
    request: Request,
    q: Optional[str] = None,
    db: Session = Depends(get_db),
    user = Depends(get_optional_user),
    templates = Depends(get_templates)
):
    results = []
    if q and q.strip():
        results = complaint_service.search_by_contact_or_id(q.strip(), db)
    elif user:
        # If logged in as citizen, show user's own complaints automatically
        results = db.query(Complaint).filter(Complaint.created_by_user_id == user.id).order_by(Complaint.created_at.desc()).all()
    context = {
        "request": request,
        "user": user,
        "query": q or "",
        "results": results
    }
    return templates.TemplateResponse(request=request, name="pages/citizen_track.html", context=context)

@router.post("/verify/{complaint_id}")
def citizen_verify_resolution(
    complaint_id: str,
    satisfied: bool = Form(...),
    comments: Optional[str] = Form(""),
    db: Session = Depends(get_db)
):
    complaint_service.verify_citizen_feedback(complaint_id, satisfied, comments, db)
    return RedirectResponse(url=f"/portal/track?q={complaint_id}&verified=true", status_code=303)
