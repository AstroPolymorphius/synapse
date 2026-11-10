import uuid
from sqlalchemy import Column, String, Text, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from backend.database import Base

class DiagnosticErrorLog(Base):
    __tablename__ = "diagnostic_error_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    attempt_id = Column(UUID(as_uuid=True), ForeignKey("retrieval_attempts.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    
    # Error Root-Cause Categorization (e.g., "misunderstood_first_principle", "broken_connection", "recall_decay")
    error_category = Column(String(100), nullable=False)
    reflective_correction = Column(Text, nullable=True) # Student's written fix or updated mental model notes
    status = Column(String(50), default="unresolved", nullable=False) # unresolved, resolved
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    resolved_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    attempt = relationship("RetrievalAttempt", back_populates="error_log")