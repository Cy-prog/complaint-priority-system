from sqlalchemy.orm import Session
from app.models import User, Department
from app.core.security import (
    verify_password,
    hash_password,
    create_session_token,
    verify_session_token,
    Role
)
from app.core.exceptions import AuthenticationError
from config.settings import get_settings

# Fast memory cache for revoked / active sessions
active_sessions: dict[str, int] = {}

class AuthService:
    def login(self, username: str, password: str, db: Session) -> tuple[User, str]:
        user = db.query(User).filter(User.username == username).first()
        if not user or not verify_password(password, user.password_hash):
            raise AuthenticationError("Invalid username or password")
        
        if not user.is_active:
            raise AuthenticationError("User account is disabled")

        # Cryptographically signed stateful session payload
        token = create_session_token({"user_id": user.id, "role": user.role, "username": user.username})
        active_sessions[token] = user.id
        return user, token

    def get_current_user(self, token: str, db: Session) -> User | None:
        if not token:
            return None
        # 1. In-memory fast cache
        user_id = active_sessions.get(token)
        if user_id:
            return db.query(User).filter(User.id == user_id, User.is_active == True).first()

        # 2. Cryptographic signature verification
        payload = verify_session_token(token)
        if payload and "user_id" in payload:
            uid = payload["user_id"]
            user = db.query(User).filter(User.id == uid, User.is_active == True).first()
            if user:
                active_sessions[token] = user.id
                return user
        return None

    def logout(self, token: str):
        if token in active_sessions:
            del active_sessions[token]

    def register_citizen(
        self,
        username: str,
        email: str,
        password: str,
        full_name: str,
        phone: str | None,
        db: Session
    ) -> User:
        """Register a new citizen in the platform."""
        clean_user = username.strip().lower()
        if db.query(User).filter(User.username == clean_user).first():
            raise AuthenticationError(f"Username '{clean_user}' is already registered.")
        if db.query(User).filter(User.email == email.strip().lower()).first():
            raise AuthenticationError(f"Email '{email}' is already registered.")

        citizen = User(
            username=clean_user,
            email=email.strip().lower(),
            password_hash=hash_password(password),
            full_name=full_name.strip(),
            role=Role.CITIZEN.value,
            phone=phone.strip() if phone else None,
            is_active=True
        )
        db.add(citizen)
        db.commit()
        db.refresh(citizen)
        return citizen

    def create_initial_admin(self, db: Session):
        return self.create_initial_users(db)

    def create_initial_users(self, db: Session):
        settings = get_settings()

        # Find Water Department ID if present
        water_dept = db.query(Department).filter(Department.name.like("%Water%")).first()
        water_dept_id = water_dept.id if water_dept else None
        
        # 1. Super Admin (Apex Municipal Authority)
        admin = db.query(User).filter(User.username == settings.ADMIN_USERNAME).first()
        if not admin:
            admin = User(
                username=settings.ADMIN_USERNAME,
                email=f"{settings.ADMIN_USERNAME}@jansamadhan.gov.in",
                password_hash=hash_password(settings.ADMIN_PASSWORD),
                full_name="श्री राजेश कुमार (BDO / Apex Authority)",
                role=Role.SUPER_ADMIN.value,
                is_active=True
            )
            db.add(admin)
        else:
            admin.role = Role.SUPER_ADMIN.value
            admin.full_name = "श्री राजेश कुमार (BDO / Apex Authority)"

        # 2. Dedicated Department Admin
        dept_admin = db.query(User).filter(User.username == "deptadmin").first()
        if not dept_admin:
            dept_admin = User(
                username="deptadmin",
                email="water.admin@jansamadhan.gov.in",
                password_hash=hash_password("admin123"),
                full_name="डॉ. सुनीता शर्मा (Executive Engineer - Water)",
                role=Role.DEPARTMENT_ADMIN.value,
                department_id=water_dept_id,
                phone="9876543210",
                is_active=True
            )
            db.add(dept_admin)
            
        # 3. Ward Officer / Field Operator
        operator = db.query(User).filter(User.username == "operator").first()
        if not operator:
            operator = User(
                username="operator",
                email="operator@jansamadhan.gov.in",
                password_hash=hash_password("operator123"),
                full_name="अभियंता अमित वर्मा (Ward Field Officer)",
                role=Role.OFFICER.value,
                department_id=water_dept_id,
                phone="9876543211",
                is_active=True
            )
            db.add(operator)
        else:
            operator.role = Role.OFFICER.value
            operator.full_name = "अभियंता अमित वर्मा (Ward Field Officer)"
            if not operator.department_id:
                operator.department_id = water_dept_id

        # 4. Standard Citizen Account
        citizen = db.query(User).filter(User.username == "citizen").first()
        if not citizen:
            citizen = User(
                username="citizen",
                email="citizen@jansamadhan.gov.in",
                password_hash=hash_password("citizen123"),
                full_name="विक्रम सिंह (Resident Citizen - Ward 15)",
                role=Role.CITIZEN.value,
                phone="9876543212",
                is_active=True
            )
            db.add(citizen)
            
        db.commit()
        db.refresh(admin)
        return admin
