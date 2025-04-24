from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

Base = declarative_base()

def get_database_url():
    if settings.DB_ENGINE == "sqlite":
        return f"sqlite:///./{settings.DB_NAME}.db"
    elif settings.DB_ENGINE == "postgres":
        return (
            f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@"
            f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
        )
    elif settings.DB_ENGINE == "mysql":
        return (
            f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}@"
            f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
        )
    else:
        raise ValueError(f"Unsupported DB_ENGINE: {settings.DB_ENGINE}")

# Create engine with dynamic DB URL
DATABASE_URL = get_database_url()
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if settings.DB_ENGINE == "sqlite" else {}
)

# Session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency injection for DB sessions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Optional: called on startup to create tables
def init_db():
    from app.models import packet_model  # ⬅️ Import all model files
    print("📦 Initializing DB... Creating tables:", Base.metadata.tables.keys())
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
