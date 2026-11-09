from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from backend.config import settings

# Initialize the SQLAlchemy engine using the database URL from settings.
# Notice the 'postgresql+psycopg://' prefix in DATABASE_URL which connects via Psycopg 3.
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # Verifies connection health before usage
)

# Create a configured session factory class
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Modern SQLAlchemy 2.0 declarative base class for all database models
class Base(DeclarativeBase):
    pass

def get_db():
    """
    FastAPI dependency that creates a new SQLAlchemy database session for a request,
    yields it to the route endpoint, and ensures it closes cleanly afterward
    even if an exception occurs.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()