from fastapi import APIRouter, Depends, Request, Form, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_templates, get_optional_user
from app.services.auth_service import AuthService
from app.core.exceptions import AuthenticationError

router = APIRouter()
auth_service = AuthService()

@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request, user = Depends(get_optional_user), templates = Depends(get_templates)):
    if user:
        return RedirectResponse(url="/", status_code=302)
    return templates.TemplateResponse(request=request, name="pages/login.html", context={"request": request})

@router.post("/login")
def login_submit(
    request: Request,
    response: Response,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
    templates = Depends(get_templates)
):
    try:
        user, token = auth_service.login(username, password, db)
        resp = RedirectResponse(url="/", status_code=302)
        resp.set_cookie(key="session_token", value=token, httponly=True, samesite="lax")
        return resp
    except AuthenticationError as e:
        context = {"request": request, "error": str(e)}
        return templates.TemplateResponse(request=request, name="pages/login.html", context=context, status_code=401)

@router.get("/switch-persona/{role}")
def switch_persona(role: str, request: Request, db: Session = Depends(get_db)):
    if role == "citizen":
        resp = RedirectResponse(url="/portal", status_code=302)
        resp.delete_cookie("session_token")
        return resp
    
    username = "admin" if role == "admin" else "operator"
    password = "admin123" if role == "admin" else "operator123"
    
    try:
        user, token = auth_service.login(username, password, db)
        resp = RedirectResponse(url="/", status_code=302)
        resp.set_cookie(key="session_token", value=token, httponly=True, samesite="lax")
        return resp
    except Exception:
        return RedirectResponse(url="/login", status_code=302)

@router.get("/logout")
def logout(request: Request, response: Response):
    token = request.cookies.get("session_token")
    if token:
        auth_service.logout(token)
    resp = RedirectResponse(url="/login", status_code=302)
    resp.delete_cookie("session_token")
    return resp
