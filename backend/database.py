import uuid
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func
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

class UUIDModel(Base):
    """
    Abstract base class providing a standard UUID primary key across all models.
    """
    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )

class TimestampedModel(Base):
    """
    Abstract base class providing automated created_at and updated_at timestamps.
    """
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
            server_default=func.now(),
            onupdate=func.now(),
            nullable=False
        )



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