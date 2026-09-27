from sqlalchemy.orm import Session
from app.models import Complaint, ComplaintAnalysis, Category
from app.core.exceptions import ComplaintNotFoundError, AIAnalysisError
from .sla_service import SLAService
from typing import Optional

def get_ai_pipeline():
    from ai.pipeline import get_pipeline
    return get_pipeline()

class AnalysisService:
    def __init__(self):
        self.sla_service = SLAService()

    def analyze_complaint(self, complaint_id: str, db: Session) -> ComplaintAnalysis:
        complaint = db.query(Complaint).filter(Complaint.complaint_id == complaint_id).first()
        if not complaint:
            raise ComplaintNotFoundError(f"Complaint {complaint_id} not found")
            
        # Check if already analyzed
        existing_analysis = db.query(ComplaintAnalysis).filter(ComplaintAnalysis.complaint_id == complaint.id).first()
        if existing_analysis:
            return existing_analysis
            
        try:
            pipeline = get_ai_pipeline()
            result = pipeline.analyze(complaint.complaint_text, complaint.id)
            
            # Map category
            if not complaint.category_id and result.category:
                cat = db.query(Category).filter(Category.name.ilike(result.category)).first()
                if cat:
                    complaint.category_id = cat.id
                    
            analysis = ComplaintAnalysis(
                complaint_id=complaint.id,
                priority=result.priority,
                priority_score=result.priority_score,
                urgency_score=result.urgency_score,
                severity_score=result.severity_score,
                impact_score=result.impact_score,
                safety_score=result.safety_score,
                duration_score=result.duration_score,
                confidence=result.confidence,
                sentiment=result.sentiment,
                risk_level=result.risk_level,
                entities=result.entities,
                key_issues=result.key_issues,
                affected_population=result.affected_population,
                affected_population_estimate=result.affected_population_estimate,
                reasoning_summary=result.reasoning_summary,
                recommended_action=result.recommended_action,
                duplicate_probability=result.duplicate_probability,
                analysis_model_version=result.analysis_model_version,
                analysis_latency_ms=result.analysis_latency_ms
            )
            
            if complaint.status == 'pending':
                complaint.status = 'open'
                
            db.add(analysis)
            db.commit()
            db.refresh(analysis)
            
            # Create SLA record
            self.sla_service.create_sla_record(complaint.id, analysis.priority, db)
            
            return analysis
        except Exception as e:
            raise AIAnalysisError(f"Failed to analyze complaint: {str(e)}")

    def reanalyze_complaint(self, complaint_id: str, db: Session) -> ComplaintAnalysis:
        complaint = db.query(Complaint).filter(Complaint.complaint_id == complaint_id).first()
        if not complaint:
            raise ComplaintNotFoundError(f"Complaint {complaint_id} not found")
            
        existing_analysis = db.query(ComplaintAnalysis).filter(ComplaintAnalysis.complaint_id == complaint.id).first()
        if existing_analysis:
            db.delete(existing_analysis)
            db.commit()
            
        return self.analyze_complaint(complaint_id, db)

    def get_analysis(self, complaint_id: str, db: Session) -> ComplaintAnalysis:
        complaint = db.query(Complaint).filter(Complaint.complaint_id == complaint_id).first()
        if not complaint:
            raise ComplaintNotFoundError(f"Complaint {complaint_id} not found")
            
        analysis = db.query(ComplaintAnalysis).filter(ComplaintAnalysis.complaint_id == complaint.id).first()
        return analysis
