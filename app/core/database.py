import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from config.settings import get_settings

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
settings = get_settings()

if settings.DATABASE_URL.startswith("sqlite"):
    # If path is relative like sqlite:///./data/complaints.db or sqlite:///data/complaints.db
    raw_path = settings.DATABASE_URL.split("sqlite:///", 1)[1] if "sqlite:///" in settings.DATABASE_URL else settings.DATABASE_URL.split("sqlite://", 1)[1]
    if raw_path.startswith("./"):
        raw_path = raw_path[2:]
    
    db_file_path = Path(raw_path)
    if not db_file_path.is_absolute():
        db_file_path = (PROJECT_ROOT / db_file_path).resolve()
        
    db_file_path.parent.mkdir(parents=True, exist_ok=True)
    db_url = f"sqlite:///{db_file_path.as_posix()}"
    engine = create_engine(db_url, connect_args={"check_same_thread": False})
else:
    engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    Base.metadata.create_all(bind=engine)
