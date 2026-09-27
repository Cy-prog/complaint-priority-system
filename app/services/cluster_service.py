from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import Complaint, Category, Incident, IncidentComplaint

class ClusterService:
    def detect_clusters(self, db: Session, window_hours: int = 72, min_complaints: int = 3) -> list[dict]:
        """
        Detects localized clusters and potential community outbreaks:
        >= min_complaints in the same ward and category within window_hours.
        """
        cutoff = datetime.utcnow() - timedelta(hours=window_hours)
        
        # Query groups
        groups = db.query(
            Complaint.ward,
            Complaint.category_id,
            func.count(Complaint.id).label('count')
        ).filter(
            Complaint.created_at >= cutoff,
            Complaint.ward != None,
            Complaint.category_id != None
        ).group_by(
            Complaint.ward,
            Complaint.category_id
        ).having(
            func.count(Complaint.id) >= min_complaints
        ).all()
        
        clusters = []
        for ward, cat_id, count in groups:
            category = db.query(Category).filter(Category.id == cat_id).first()
            cat_name = category.name if category else "General"
            risk_level = category.risk_level if category else "medium"
            
            # Fetch complaints in this cluster
            cluster_complaints = db.query(Complaint).filter(
                Complaint.created_at >= cutoff,
                Complaint.ward == ward,
                Complaint.category_id == cat_id
            ).order_by(Complaint.created_at.asc()).all()
            
            first_time = cluster_complaints[0].created_at if cluster_complaints else cutoff
            last_time = cluster_complaints[-1].created_at if cluster_complaints else datetime.utcnow()
            
            # High risk or essential service clusters trigger Emergency Alert
            severity = "CRITICAL" if risk_level in ["critical", "high"] or (category and category.is_essential_service) else "HIGH"
            
            rec_action = (
                f"Urgent Gram Sabha Intervention: Multiple recurring {cat_name} failures reported in {ward}. "
                f"Dispatch field supervisor and convene emergency Ward review."
            )
            if "water" in cat_name.lower():
                rec_action = f"Water Contamination / Outbreak Alert in {ward}: Check main pipeline and test potable water samples immediately."
            elif "electric" in cat_name.lower():
                rec_action = f"Electrical Grid Hazard Alert in {ward}: Power line / transformer fault endangering multiple households."
            elif "sanitation" in cat_name.lower() or "drainage" in cat_name.lower():
                rec_action = f"Public Health Risk in {ward}: Sewage overflow / waterlogging creating epidemic hazard. Mobilize sanitation team."
                
            clusters.append({
                "ward": ward,
                "category_id": cat_id,
                "category_name": cat_name,
                "count": count,
                "severity": severity,
                "title": f"{cat_name} Cluster Alert in {ward} ({count} Reports)",
                "recommended_action": rec_action,
                "first_reported": first_time.strftime("%d %b, %H:%M") if hasattr(first_time, 'strftime') else str(first_time),
                "last_updated": last_time.strftime("%d %b, %H:%M") if hasattr(last_time, 'strftime') else str(last_time),
                "complaints": [
                    {
                        "complaint_id": c.complaint_id,
                        "text": c.complaint_text,
                        "status": c.status,
                        "priority": c.analysis.priority if c.analysis else "PENDING",
                        "area": c.area or ward
                    } for c in cluster_complaints
                ]
            })
            
        return clusters
