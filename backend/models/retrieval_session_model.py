import uuid
from typing import Optional, TYPE_CHECKING
from datetime import datetime
from sqlalchemy import String, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database import UUIDModel, TimestampedModel

if TYPE_CHECKING:
    from backend.models.subject_workspace_model import SubjectWorkspace
    from backend.models.retrieval_attempt_model import RetrievalAttempt

class RetrievalSession(UUIDModel, TimestampedModel):
    __tablename__ = "retrieval_sessions"

    workspace_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("subject_workspaces.id", ondelete="CASCADE"), nullable=False, index=True)
    # Session Metadata
    session_type: Mapped[str] = mapped_column(String(50), default="closed_book", nullable=False)
    total_items: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    accuracy_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False) # Percentage or score 0.0 to 1.0
    
    # Timestamps that aren't in the TimestampedModel class
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    workspace: Mapped["SubjectWorkspace"] = relationship("SubjectWorkspace")
    attempts: Mapped[list["RetrievalAttempt"]] = relationship("RetrievalAttempt", back_populates="session", cascade="all, delete-orphan")