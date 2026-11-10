import uuid
from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from backend.database import Base

class RetrievalSession(Base):
    __tablename__ = "retrieval_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("subject_workspaces.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Session Metadata
    session_type = Column(String(50), default="closed_book", nullable=False) # closed_book, targeted_review
    total_items = Column(Integer, default=0, nullable=False)
    accuracy_score = Column(Float, default=0.0, nullable=False) # Percentage or score 0.0 to 1.0
    
    # Timestamps
    started_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    workspace = relationship("SubjectWorkspace")
    attempts = relationship("RetrievalAttempt", back_populates="session", cascade="all, delete-orphan")