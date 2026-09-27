from fastapi import APIRouter
from .auth import router as auth_router
from .complaints import router as complaints_router
from .dashboard import router as dashboard_router
from .categories import router as categories_router
from .feedback import router as feedback_router

api_router = APIRouter()
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(complaints_router, prefix="/complaints", tags=["complaints"])
api_router.include_router(dashboard_router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(categories_router, prefix="", tags=["categories"])
api_router.include_router(feedback_router, prefix="/feedback", tags=["feedback"])
