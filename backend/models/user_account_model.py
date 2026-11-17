import uuid
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, Boolean, Integer, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from backend.database import UUIDModel, TimestampedModel


# 2. Import the model conditionally so the type checker sees it, 
# but circular imports are avoided at runtime.
if TYPE_CHECKING:
    from backend.models.subject_workspace_model import SubjectWorkspace
    from backend.models.retrieval_session_model import RetrievalSession
class UserRole(str, enum.Enum):
    STUDENT = "student"
    ADMIN = "admin"

class User(UUIDModel, TimestampedModel):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)  # Nullable for users authenticating solely via Google OAuth
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    
    # Account Settings & Roles
    role: Mapped[UserRole] = mapped_column(SQLEnum(UserRole), default=UserRole.STUDENT, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    daily_intake_limit: Mapped[int] = mapped_column(Integer, default=5, nullable=False)  # Systems advisory intake cap
    
    # Google OAuth integration fields
    google_id: Mapped[Optional[str]] = mapped_column(String(255), unique=True, index=True, nullable=True)
    avatar_url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    
    
    # Relationships
    retrieval_sessions: Mapped[list["RetrievalSession"]] = relationship("RetrievalSession", back_populates="user", cascade="all, delete-orphan")
    workspaces: Mapped[list["SubjectWorkspace"]] = relationship("SubjectWorkspace", back_populates="owner", cascade="all, delete-orphan")