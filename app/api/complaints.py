from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.complaint import ComplaintCreate, ComplaintUpdate, ComplaintResponse, ComplaintListResponse, ComplaintFilters
from app.schemas.common import PaginationParams, PaginatedResponse, MessageResponse
from app.schemas.analysis import AnalysisResponse, SimilarComplaintResponse, PriorityOverrideRequest, PriorityOverrideResponse, FeedbackRequest, FeedbackResponse
from app.services.complaint_service import ComplaintService
from app.services.analysis_service import AnalysisService
from app.services.duplicate_service import DuplicateService
from app.services.priority_service import PriorityService
from app.services.feedback_service import FeedbackService
from app.dependencies import get_db, get_current_user, get_optional_user
from app.models import User

router = APIRouter()
complaint_service = ComplaintService()
analysis_service = AnalysisService()
duplicate_service = DuplicateService()
priority_service = PriorityService()
feedback_service = FeedbackService()

@router.post("", response_model=ComplaintResponse)
def create_complaint(data: ComplaintCreate, db: Session = Depends(get_db), user: User = Depends(get_optional_user)):
    user_id = user.id if user else None
    return complaint_service.create_complaint(data, db, user_id)

@router.get("", response_model=PaginatedResponse[ComplaintListResponse])
def list_complaints(
    filters: ComplaintFilters = Depends(),
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db)
):
    return complaint_service.list_complaints(filters, pagination, db)

@router.get("/{complaint_id}", response_model=ComplaintResponse)
def get_complaint(complaint_id: str, db: Session = Depends(get_db)):
    try:
        return complaint_service.get_complaint(complaint_id, db)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{complaint_id}", response_model=ComplaintResponse)
def update_complaint(complaint_id: str, data: ComplaintUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    try:
        return complaint_service.update_complaint(complaint_id, data, db, user.id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{complaint_id}", response_model=MessageResponse)
def delete_complaint(complaint_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    try:
        complaint_service.delete_complaint(complaint_id, db)
        return MessageResponse(message="Complaint deleted", success=True)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/{complaint_id}/analyze", response_model=AnalysisResponse)
def analyze_complaint(complaint_id: str, db: Session = Depends(get_db)):
    try:
        return analysis_service.analyze_complaint(complaint_id, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{complaint_id}/reprioritize", response_model=AnalysisResponse)
def reprioritize_complaint(complaint_id: str, db: Session = Depends(get_db)):
    try:
        return analysis_service.reanalyze_complaint(complaint_id, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{complaint_id}/similar", response_model=list[SimilarComplaintResponse])
def get_similar_complaints(complaint_id: str, db: Session = Depends(get_db)):
    try:
        return duplicate_service.find_similar(complaint_id, db)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/{complaint_id}/override", response_model=PriorityOverrideResponse)
def override_priority(complaint_id: str, override: PriorityOverrideRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    try:
        ov = priority_service.override_priority(complaint_id, override, user.id, db)
        return PriorityOverrideResponse(
            id=ov.id,
            original_priority=ov.original_priority,
            original_score=ov.original_score,
            new_priority=ov.new_priority,
            new_score=ov.new_score,
            reason=ov.reason,
            changed_at=ov.changed_at,
            changed_by_username=user.username
        )
    except ComplaintNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{complaint_id}/feedback", response_model=FeedbackResponse)
def submit_feedback(complaint_id: str, feedback: FeedbackRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    try:
        return feedback_service.submit_feedback(complaint_id, feedback, user.id, db)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
