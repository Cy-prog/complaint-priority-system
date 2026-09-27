from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import Complaint, ComplaintAnalysis, PriorityOverride, SLARecord, Category
from app.schemas.dashboard import DashboardSummary, TrendData, CategoryDistribution, PriorityDistribution, AnalyticsResponse
from datetime import datetime, timedelta

class AnalyticsService:
    def get_dashboard_summary(self, db: Session) -> DashboardSummary:
        total = db.query(Complaint).count()
        pending = db.query(Complaint).filter(Complaint.status == 'pending').count()
        open_count = db.query(Complaint).filter(Complaint.status == 'open').count()
        in_prog = db.query(Complaint).filter(Complaint.status == 'in_progress').count()
        resolved = db.query(Complaint).filter(Complaint.status.in_(['resolved', 'closed'])).count()
        
        analysis_counts = db.query(ComplaintAnalysis.priority, func.count(ComplaintAnalysis.id)).group_by(ComplaintAnalysis.priority).all()
        priorities = {p: c for p, c in analysis_counts}
        
        breaches = db.query(SLARecord).filter(SLARecord.is_breached == True).count()
        
        avg_conf = db.query(func.avg(ComplaintAnalysis.confidence)).scalar() or 0.0
        
        # Avg resolution time
        resolved_slas = db.query(SLARecord).filter(SLARecord.resolution_time_minutes != None).all()
        avg_res_time = sum(sla.resolution_time_minutes for sla in resolved_slas) / len(resolved_slas) if resolved_slas else 0
        
        return DashboardSummary(
            total_complaints=total,
            critical_count=priorities.get('CRITICAL', 0),
            high_count=priorities.get('HIGH', 0),
            medium_count=priorities.get('MEDIUM', 0),
            low_count=priorities.get('LOW', 0),
            pending_count=pending,
            open_count=open_count,
            in_progress_count=in_prog,
            resolved_count=resolved,
            avg_resolution_time_hours=avg_res_time / 60,
            sla_breach_count=breaches,
            duplicate_count=0,
            avg_confidence=round(float(avg_conf), 2)
        )

    def get_complaints_trend(self, days: int, db: Session) -> list[TrendData]:
        # Simplistic grouping by date string
        # Real implementation would use db specific date truncation
        return []

    def get_priority_distribution(self, db: Session) -> list[PriorityDistribution]:
        counts = db.query(ComplaintAnalysis.priority, func.count(ComplaintAnalysis.id)).group_by(ComplaintAnalysis.priority).all()
        return [PriorityDistribution(priority=p, count=c) for p, c in counts if p]

    def get_category_distribution(self, db: Session) -> list[CategoryDistribution]:
        counts = db.query(Category.name, func.count(Complaint.id))\
                   .join(Complaint, Complaint.category_id == Category.id)\
                   .group_by(Category.name).all()
        return [CategoryDistribution(category=n, count=c) for n, c in counts]

    def get_override_rate(self, db: Session) -> float:
        total = db.query(ComplaintAnalysis).count()
        if total == 0:
            return 0.0
        overrides = db.query(PriorityOverride).count()
        return overrides / total

    def get_sla_compliance_rate(self, db: Session) -> float:
        total = db.query(SLARecord).count()
        if total == 0:
            return 1.0
        breached = db.query(SLARecord).filter(SLARecord.is_breached == True).count()
        return (total - breached) / total

    def get_analytics(self, db: Session) -> AnalyticsResponse:
        return AnalyticsResponse(
            complaints_over_time=self.get_complaints_trend(30, db),
            priority_distribution=self.get_priority_distribution(db),
            category_distribution=self.get_category_distribution(db),
            override_rate=self.get_override_rate(db),
            avg_confidence=db.query(func.avg(ComplaintAnalysis.confidence)).scalar() or 0.0,
            sla_compliance_rate=self.get_sla_compliance_rate(db)
        )
