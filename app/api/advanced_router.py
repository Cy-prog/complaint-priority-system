from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from fastapi.responses import Response
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional

from app.dependencies import get_db, get_current_user, get_optional_user, require_roles
from app.models import User
from app.services.department_service import DepartmentService
from app.services.sla_service import SLAService
from app.services.gis_service import GISService
from app.services.predictive_service import PredictiveAnalyticsService
from app.services.notification_service import NotificationService
from app.services.report_service import ReportService
from app.schemas.common import MessageResponse

router = APIRouter()
dept_service = DepartmentService()
sla_service = SLAService()
gis_service = GISService()
pred_service = PredictiveAnalyticsService()
notif_service = NotificationService()
report_service = ReportService()

# ==================== DEPARTMENT MANAGEMENT ====================
@router.get("/departments/{dept_id}/officers")
def get_dept_officers(dept_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    officers = dept_service.list_department_officers(dept_id, db)
    return [dept_service.get_officer_workload(o.id, db) for o in officers]

@router.get("/complaints/{complaint_id}/recommend-assignment")
def recommend_assignment(complaint_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return dept_service.recommend_assignment(complaint_id, db)

@router.post("/complaints/{complaint_id}/assign")
def assign_complaint(
    complaint_id: str,
    department_id: Optional[int] = Query(None),
    officer_id: Optional[int] = Query(None),
    notes: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    try:
        updated = dept_service.assign_complaint(complaint_id, department_id, officer_id, user.id, notes, db)
        return {"success": True, "complaint_id": updated.complaint_id, "status": updated.status}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ==================== SLA & ESCALATION ====================
@router.get("/sla/{complaint_id}")
def get_sla_status(complaint_id: str, db: Session = Depends(get_db)):
    return sla_service.get_sla_status(complaint_id, db)

@router.post("/sla/check-breaches")
@router.post("/sla/check-escalations")
def check_sla_breaches(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return sla_service.check_and_escalate_slas(db)

@router.get("/departments/{dept_id}/sla-metrics")
def get_dept_sla_metrics(dept_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return sla_service.get_department_sla_metrics(dept_id, db)

# ==================== GIS SPATIAL INTELLIGENCE ====================
@router.get("/gis/markers")
def get_gis_markers(
    category_id: Optional[int] = None,
    priority: Optional[str] = None,
    ward: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return gis_service.get_map_markers(db, category_id, priority, ward)

@router.get("/gis/wards")
def get_ward_spatial_summary(db: Session = Depends(get_db)):
    return gis_service.get_ward_spatial_summary(db)

# ==================== PREDICTIVE ANALYTICS ====================
@router.get("/predictive/forecast")
def get_complaint_forecast(days: int = 14, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return pred_service.get_forecast(db, days)

@router.get("/predictive/hotspots")
def get_recurring_hotspots(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return pred_service.get_recurring_hotspots(db)

@router.get("/predictive/seasonal")
def get_seasonal_insights(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return pred_service.get_seasonal_insights(db)

# ==================== NOTIFICATIONS ====================
@router.get("/notifications")
def get_user_notifications(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    notifs = notif_service.list_user_notifications(user.id, db)
    return [
        {
            "id": n.id,
            "title": n.title,
            "message": n.message,
            "type": n.notification_type,
            "reference_id": n.reference_id,
            "is_read": n.is_read,
            "created_at": n.created_at.strftime("%Y-%m-%d %H:%M") if n.created_at else ""
        }
        for n in notifs
    ]

@router.get("/notifications/unread-count")
def get_unread_notification_count(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return {"unread_count": notif_service.get_unread_count(user.id, db)}

@router.post("/notifications/{notif_id}/read")
def mark_notification_read(notif_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    success = notif_service.mark_as_read(notif_id, db)
    return {"success": success}

@router.post("/notifications/read-all")
def mark_all_notifications_read(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    count = notif_service.mark_all_as_read(user.id, db)
    return {"marked_read": count}

# ==================== REPORTING & EXPORTS ====================
@router.get("/reports/csv")
def export_complaints_csv(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    csv_data = report_service.export_csv(db)
    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=SmartCivic_Complaints_Report.csv"}
    )

@router.get("/reports/excel")
def export_complaints_excel(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    excel_bytes = report_service.export_excel(db)
    return Response(
        content=excel_bytes,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=SmartCivic_Governance_Analytics.xlsx"}
    )

@router.get("/reports/pdf")
def export_complaints_pdf(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    pdf_bytes = report_service.generate_pdf_dossier(db)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": "inline; filename=SmartCivic_Executive_Dossier.pdf"}
    )

# ==================== PUBLIC TRANSPARENCY (PRIVACY SAFE) ====================
@router.get("/public/transparency-summary")
@router.get("/transparency/metrics")
def get_public_transparency_data(db: Session = Depends(get_db)):
    """Returns privacy-safe public governance statistics. Zero Citizen PII is exposed."""
    from app.models import Complaint, Category, SLARecord, ComplaintAnalysis
    total = db.query(Complaint).count()
    resolved = db.query(Complaint).filter(Complaint.status.in_(["resolved", "closed"])).count()
    breached = db.query(SLARecord).filter(SLARecord.is_breached == True).count()
    compliance = round(((total - breached) / total) * 100, 1) if total > 0 else 100.0

    cat_counts = db.query(Category.name, func.count(Complaint.id))\
                   .join(Complaint, Complaint.category_id == Category.id)\
                   .group_by(Category.name).all()

    # Privacy-safe recent resolutions
    recent_resolved = db.query(Complaint).filter(Complaint.status.in_(["resolved", "closed"]))\
                        .order_by(Complaint.resolved_at.desc()).limit(10).all()

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

    return {
        "platform": "SmartCivic AI Transparency Portal",
        "total_complaints": total,
        "total_grievances_received": total,
        "resolved_complaints": resolved,
        "resolved_grievances": resolved,
        "resolution_percentage": round((resolved / total) * 100, 1) if total > 0 else 0.0,
        "sla_compliance_rate": compliance,
        "overall_sla_compliance_rate": compliance,
        "category_distribution": [{"category": name, "count": cnt} for name, cnt in cat_counts],
        "recent_verified_resolutions": sanitized_feed
    }
