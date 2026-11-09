import uuid
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from backend.database import Base

class UserRole(str, enum.Enum):
    STUDENT = "student"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=True)  # Nullable for users authenticating solely via Google OAuth
    full_name = Column(String(100), nullable=False)
    
    # Account Settings & Roles
    role = Column(SQLEnum(UserRole), default=UserRole.STUDENT, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    daily_intake_limit = Column(Integer, default=5, nullable=False)  # Systems advisory intake cap
    
    # Google OAuth integration fields
    google_id = Column(String(255), unique=True, index=True, nullable=True)
    avatar_url = Column(String(512), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    workspaces = relationship("SubjectWorkspace", back_populates="owner", cascade="all, delete-orphan")