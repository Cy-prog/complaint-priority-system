from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import os
import json

from app.core.database import Base, engine, SessionLocal
from app.api.router import api_router
from app.pages.dashboard import router as pages_dashboard_router
from app.pages.complaints import router as pages_complaints_router
from app.pages.analytics import router as pages_analytics_router
from app.pages.settings_page import router as pages_settings_router
from app.pages.auth_pages import router as pages_auth_router
from app.pages.portal import router as pages_portal_router
from app.pages.reports import router as pages_reports_router
from app.middleware.rate_limit import setup_rate_limiting
from app.services.auth_service import AuthService
from app.models import Category, Department
from app.core.exceptions import ComplaintNotFoundError, AuthenticationError, AuthorizationError, AIAnalysisError

def create_app() -> FastAPI:
    app = FastAPI(
        title="AI Complaint Priority System",
        description="Backend API layer of an AI-Based Complaint Priority System",
        version="1.0.0"
    )

    # Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    setup_rate_limiting(app)

    # Static files
    static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

    upload_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "uploads")
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    app.mount("/uploads", StaticFiles(directory=upload_dir), name="uploads")

    # PWA Endpoints
    @app.get("/manifest.json")
    def get_manifest():
        manifest_path = os.path.join(static_dir, "manifest.json")
        return FileResponse(manifest_path, media_type="application/manifest+json")

    @app.get("/sw.js")
    def get_service_worker():
        sw_path = os.path.join(static_dir, "sw.js")
        return FileResponse(sw_path, media_type="application/javascript", headers={"Service-Worker-Allowed": "/"})

    # API Routers
    app.include_router(api_router, prefix="/api")

    # Page Routers
    app.include_router(pages_auth_router)
    app.include_router(pages_dashboard_router)
    app.include_router(pages_complaints_router)
    app.include_router(pages_analytics_router)
    app.include_router(pages_settings_router)
    app.include_router(pages_portal_router)
    app.include_router(pages_reports_router)

    # Exception Handlers
    @app.exception_handler(ComplaintNotFoundError)
    async def complaint_not_found_handler(request: Request, exc: ComplaintNotFoundError):
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @app.exception_handler(AuthenticationError)
    async def auth_error_handler(request: Request, exc: AuthenticationError):
        return JSONResponse(status_code=401, content={"detail": str(exc)})

    @app.exception_handler(AuthorizationError)
    async def authz_error_handler(request: Request, exc: AuthorizationError):
        return JSONResponse(status_code=403, content={"detail": str(exc)})

    @app.exception_handler(AIAnalysisError)
    async def ai_error_handler(request: Request, exc: AIAnalysisError):
        return JSONResponse(status_code=500, content={"detail": str(exc)})

    @app.on_event("startup")
    def startup_event():
        Base.metadata.create_all(bind=engine)
        db = SessionLocal()
        try:
            # Seed Admin
            AuthService().create_initial_admin(db)
            
            # Seed Departments
            if db.query(Department).count() == 0:
                dept_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "seed", "departments.json")
                if os.path.exists(dept_file):
                    with open(dept_file, 'r') as f:
                        depts = json.load(f)
                        for d in depts:
                            dept = Department(**d)
                            db.add(dept)
                    db.commit()

            # Seed Categories
            if db.query(Category).count() == 0:
                cat_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "seed", "categories.json")
                if os.path.exists(cat_file):
                    with open(cat_file, 'r') as f:
                        cats = json.load(f)
                        for c in cats:
                            cat = Category(**c)
                            db.add(cat)
                    db.commit()
        finally:
            db.close()
            
    @app.get("/api/health")
    def health_check():
        return {"status": "ok"}

    return app

app = create_app()
