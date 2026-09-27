from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.analysis import FeedbackRequest, FeedbackResponse
from app.services.feedback_service import FeedbackService
from app.dependencies import get_db, get_current_user
from app.models import User

router = APIRouter()
feedback_service = FeedbackService()

@router.post("", response_model=FeedbackResponse)
def submit_general_feedback(complaint_id: str, feedback: FeedbackRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    try:
        return feedback_service.submit_feedback(complaint_id, feedback, user.id, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
