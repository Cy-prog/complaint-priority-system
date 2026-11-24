from fastapi import APIRouter, Depends, HTTPException, Response, Request, status
from sqlalchemy.orm import Session
from app.schemas.auth import LoginRequest, LoginResponse, RegisterRequest, UserResponse
from app.schemas.common import MessageResponse
from app.services.auth_service import AuthService
from app.dependencies import get_db, get_current_user
from app.models import User

router = APIRouter()
auth_service = AuthService()

@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, response: Response, db: Session = Depends(get_db)):
    try:
        user, token = auth_service.login(request.username, request.password, db)
        response.set_cookie(
            key="session_token",
            value=token,
            httponly=True,
            samesite="lax",
            max_age=86400 * 7
        )
        return LoginResponse(
            token=token,
            user=UserResponse.model_validate(user)
        )
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.post("/register", response_model=LoginResponse, status_code=status.HTTP_201_CREATED)
def register(request: RegisterRequest, response: Response, db: Session = Depends(get_db)):
    try:
        user = auth_service.register_citizen(
            username=request.username,
            email=request.email,
            password=request.password,
            full_name=request.full_name,
            phone=request.phone,
            db=db
        )
        _, token = auth_service.login(request.username, request.password, db)
        response.set_cookie(
            key="session_token",
            value=token,
            httponly=True,
            samesite="lax",
            max_age=86400 * 7
        )
        return LoginResponse(
            token=token,
            user=UserResponse.model_validate(user)
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/logout", response_model=MessageResponse)
def logout(request: Request, response: Response):
    token = request.cookies.get("session_token")
    if token:
        auth_service.logout(token)
    response.delete_cookie("session_token")
    return MessageResponse(message="Logged out successfully", success=True)

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return UserResponse.model_validate(current_user)
