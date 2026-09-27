from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import func, case
from app.dependencies import get_db, get_optional_user, get_templates
from app.models import Complaint, Category, Department, ComplaintAnalysis, SLARecord

router = APIRouter(prefix="/reports")

@router.get("/gram-sabha", response_class=HTMLResponse)
def gram_sabha_report_page(request: Request, db: Session = Depends(get_db), user = Depends(get_optional_user), templates = Depends(get_templates)):
    if not user:
        return RedirectResponse(url="/login", status_code=302)
        
    now = datetime.utcnow()
    month_str = now.strftime("%B %Y")
    
    # 1. High level statistics
    total = db.query(Complaint).count()
    resolved = db.query(Complaint).filter(Complaint.status.in_(['resolved', 'closed'])).count()
    pending = db.query(Complaint).filter(Complaint.status.in_(['pending', 'open', 'in_progress'])).count()
    
    # 2. SLA compliance
    breached = db.query(SLARecord).filter(SLARecord.is_breached == True).count()
    
    # 3. Satisfaction
    satisfied_count = db.query(Complaint).filter(Complaint.citizen_feedback_status == 'satisfied').count()
    reopened_count = db.query(Complaint).filter(Complaint.citizen_feedback_status == 'reopened').count()
    
    # 4. Ward-by-Ward Aggregation
    ward_counts = db.query(
        Complaint.ward,
        func.count(Complaint.id).label('total'),
        func.sum(case((Complaint.status.in_(['resolved', 'closed']), 1), else_=0)).label('resolved')
    ).filter(Complaint.ward != None).group_by(Complaint.ward).all()
    
    ward_stats = []
    for w, tot, res in ward_counts:
        ward_stats.append({
            "ward": w,
            "total": tot,
            "resolved": res or 0,
            "pending": tot - (res or 0)
        })
        
    # 5. Critical Emergency Grievances Tabled for Gram Sabha Discussion
    critical_complaints = db.query(Complaint).join(ComplaintAnalysis).filter(
        ComplaintAnalysis.priority == 'CRITICAL'
    ).order_by(Complaint.created_at.desc()).limit(10).all()
    
    # 6. All complaints ledger
    all_complaints = db.query(Complaint).order_by(Complaint.created_at.desc()).limit(50).all()
    
    context = {
        "request": request,
        "user": user,
        "report_date": now.strftime("%d-%m-%Y"),
        "month_str": month_str,
        "total": total,
        "resolved": resolved,
        "pending": pending,
        "breached": breached,
        "satisfied_count": satisfied_count,
        "reopened_count": reopened_count,
        "ward_stats": ward_stats,
        "critical_complaints": critical_complaints,
        "complaints": all_complaints
    }
    
    return templates.TemplateResponse(request=request, name="pages/gram_sabha_report.html", context=context)
