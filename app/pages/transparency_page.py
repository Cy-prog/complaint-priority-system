from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.dependencies import get_db, get_optional_user, get_templates
from app.models import Complaint, Category, Department, SLARecord, ComplaintAnalysis

router = APIRouter(prefix="/transparency")

@router.get("", response_class=HTMLResponse)
def public_transparency_page(
    request: Request,
    db: Session = Depends(get_db),
    user = Depends(get_optional_user),
    templates = Depends(get_templates)
):
    total = db.query(Complaint).count()
    resolved = db.query(Complaint).filter(Complaint.status.in_(["resolved", "closed"])).count()
    breached = db.query(SLARecord).filter(SLARecord.is_breached == True).count()
    compliance = round(((total - breached) / total) * 100, 1) if total > 0 else 100.0

    cat_counts = db.query(Category.name, func.count(Complaint.id))\
                   .join(Complaint, Complaint.category_id == Category.id)\
                   .group_by(Category.name).all()

    # Privacy-safe recent resolutions
    recent_resolved = db.query(Complaint).filter(Complaint.status.in_(["resolved", "closed"]))\
                        .order_by(Complaint.resolved_at.desc()).limit(15).all()

    sanitized_feed = [
        {
            "id": c.complaint_id,
            "category": c.category.name if c.category else "Civic Service",
            "ward": c.ward or "General Ward",
            "resolved_at": c.resolved_at.strftime("%d-%m-%Y") if c.resolved_at else "Recently",
            "status": "Resolved & Verified"
        }
        for c in recent_resolved
    ]

    context = {
        "request": request,
        "user": user,
        "total": total,
        "resolved": resolved,
        "pending": total - resolved,
        "resolution_percentage": round((resolved / total) * 100, 1) if total > 0 else 0.0,
        "sla_compliance_rate": compliance,
        "category_distribution": [{"category": name, "count": cnt} for name, cnt in cat_counts],
        "recent_resolutions": sanitized_feed
    }
    return templates.TemplateResponse(request=request, name="pages/transparency.html", context=context)
