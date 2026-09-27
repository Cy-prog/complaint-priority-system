from sqlalchemy.orm import Session
from app.models import Complaint, SimilarComplaint
from app.schemas.analysis import SimilarComplaintResponse
from app.core.exceptions import ComplaintNotFoundError

class DuplicateService:
    def find_similar(self, complaint_id: str, db: Session) -> list[SimilarComplaintResponse]:
        complaint = db.query(Complaint).filter(Complaint.complaint_id == complaint_id).first()
        if not complaint:
            raise ComplaintNotFoundError(f"Complaint {complaint_id} not found")
            
        # In a real implementation, this would query ChromaDB for similar embeddings
        # Here we just mock returning similar complaints from the DB
        similars = db.query(SimilarComplaint).filter(SimilarComplaint.complaint_id == complaint.id).all()
        
        results = []
        for sim in similars:
            sim_complaint = db.query(Complaint).filter(Complaint.id == sim.similar_complaint_id).first()
            if sim_complaint:
                results.append(
                    SimilarComplaintResponse(
                        complaint_id=sim_complaint.complaint_id,
                        complaint_text=sim_complaint.complaint_text[:100] + "..." if len(sim_complaint.complaint_text) > 100 else sim_complaint.complaint_text,
                        similarity_score=sim.similarity_score,
                        category=sim_complaint.category.name if sim_complaint.category else "Uncategorized",
                        priority=sim_complaint.analysis.priority if sim_complaint.analysis else "Pending"
                    )
                )
        return results
