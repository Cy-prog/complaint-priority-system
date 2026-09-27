from sqlalchemy.orm import Session
from app.models import User
from app.core.security import verify_password, hash_password
from app.core.exceptions import AuthenticationError
from config.settings import get_settings

# Simple in-memory session store for demo purposes
# In production, use Redis or database table
active_sessions = {}

class AuthService:
    def login(self, username: str, password: str, db: Session) -> tuple[User, str]:
        user = db.query(User).filter(User.username == username).first()
        if not user or not verify_password(password, user.password_hash):
            raise AuthenticationError("Invalid username or password")
        
        if not user.is_active:
            raise AuthenticationError("User account is disabled")

        import secrets
        token = secrets.token_urlsafe(32)
        active_sessions[token] = user.id
        return user, token

    def get_current_user(self, token: str, db: Session) -> User | None:
        user_id = active_sessions.get(token)
        if not user_id:
            return None
        return db.query(User).filter(User.id == user_id).first()

    def logout(self, token: str):
        if token in active_sessions:
            del active_sessions[token]

    def create_initial_admin(self, db: Session):
        return self.create_initial_users(db)

    def create_initial_users(self, db: Session):
        settings = get_settings()
        
        # 1. Apex Executive / BDO / Sarpanch
        admin = db.query(User).filter(User.username == settings.ADMIN_USERNAME).first()
        if not admin:
            admin = User(
                username=settings.ADMIN_USERNAME,
                email=f"{settings.ADMIN_USERNAME}@jansamadhan.gov.in",
                password_hash=hash_password(settings.ADMIN_PASSWORD),
                full_name="श्री राजेश कुमार (BDO / Apex Authority)",
                role="admin",
                is_active=True
            )
            db.add(admin)
        else:
            admin.full_name = "श्री राजेश कुमार (BDO / Apex Authority)"
            
        # 2. Ward Officer / Field Operator
        operator = db.query(User).filter(User.username == "operator").first()
        if not operator:
            operator = User(
                username="operator",
                email="operator@jansamadhan.gov.in",
                password_hash=hash_password("operator123"),
                full_name="अभियंता अमित वर्मा (Ward Field Officer)",
                role="operator",
                is_active=True
            )
            db.add(operator)
        else:
            operator.full_name = "अभियंता अमित वर्मा (Ward Field Officer)"
            
        db.commit()
        db.refresh(admin)
        return admin
