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
        resp.set_cookie(key="session_token", value=token, httponly=True, samesite="lax", max_age=86400 * 7)
        return resp
    except AuthenticationError as e:
        context = {"request": request, "error": str(e)}
        return templates.TemplateResponse(request=request, name="pages/login.html", context=context, status_code=401)

@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request, user = Depends(get_optional_user), templates = Depends(get_templates)):
    if user:
        return RedirectResponse(url="/", status_code=302)
    return templates.TemplateResponse(request=request, name="pages/login.html", context={"request": request, "mode": "register"})

@router.post("/register")
def register_submit(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    full_name: str = Form(...),
    phone: str = Form(None),
    db: Session = Depends(get_db),
    templates = Depends(get_templates)
):
    try:
        user = auth_service.register_citizen(
            username=username,
            email=email,
            password=password,
            full_name=full_name,
            phone=phone,
            db=db
        )
        _, token = auth_service.login(username, password, db)
        resp = RedirectResponse(url="/portal", status_code=302)
        resp.set_cookie(key="session_token", value=token, httponly=True, samesite="lax", max_age=86400 * 7)
        return resp
    except Exception as e:
        context = {"request": request, "error": str(e), "mode": "register"}
        return templates.TemplateResponse(request=request, name="pages/login.html", context=context, status_code=400)

@router.get("/switch-persona/{role}")
def switch_persona(role: str, request: Request, db: Session = Depends(get_db)):
    role_lower = role.lower()
    
    # 4 Canonical Personas for seamless demonstration & evaluation
    if role_lower in ("super_admin", "admin", "apex"):
        username, password, target_url = "admin", "admin123", "/"
    elif role_lower in ("department_admin", "deptadmin", "dept_admin"):
        username, password, target_url = "deptadmin", "admin123", "/department"
    elif role_lower in ("officer", "operator", "field"):
        username, password, target_url = "operator", "operator123", "/officer"
    elif role_lower in ("citizen", "public"):
        username, password, target_url = "citizen", "citizen123", "/portal"
    else:
        resp = RedirectResponse(url="/portal", status_code=302)
        resp.delete_cookie("session_token")
        return resp

    try:
        user, token = auth_service.login(username, password, db)
        resp = RedirectResponse(url=target_url, status_code=302)
        resp.set_cookie(key="session_token", value=token, httponly=True, samesite="lax", max_age=86400 * 7)
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
