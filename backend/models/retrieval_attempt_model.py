import uuid
from sqlalchemy import Column, String, Text, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database import Base

class RetrievalAttempt(Base):
    __tablename__ = "retrieval_attempts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    session_id = Column(UUID(as_uuid=True), ForeignKey("retrieval_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    concept_node_id = Column(UUID(as_uuid=True), ForeignKey("concept_nodes.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Attempt Details
    user_recall_input = Column(Text, nullable=True) # What the student typed/recalled under masked conditions
    was_successful = Column(Boolean, default=False, nullable=False)
    confidence_rating = Column(Float, default=0.0, nullable=False) # Self-reported confidence score
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    session = relationship("RetrievalSession", back_populates="attempts")
    concept_node = relationship("ConceptNode")
    error_log = relationship("DiagnosticErrorLog", back_populates="attempt", uselist=False, cascade="all, delete-orphan")