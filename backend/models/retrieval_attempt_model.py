import uuid
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, Text, Float, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database import UUIDModel, TimestampedModel

if TYPE_CHECKING:
    from backend.models.retrieval_session_model import RetrievalSession
    from backend.models.concept_node_model import ConceptNode
    from backend.models.diagnostic_error_log_model import DiagnosticErrorLog

#Defines the RetrievalAttempt model which records the student's specific answer and accuracy score for an individual ConceptNode tested during a retrieval session.
class RetrievalAttempt(UUIDModel, TimestampedModel):
    __tablename__ = "retrieval_attempts"

    session_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("retrieval_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    concept_node_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("concept_nodes.id", ondelete="CASCADE"), nullable=False, index=True)

    # Attempt Details
    user_recall_input: Mapped[Optional[str]] = mapped_column(Text, nullable=True) # What the student typed/recalled under masked conditions
    is_correct: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    confidence_rating: Mapped[float] = mapped_column(Float, default=0.0, nullable=False) # Self-reported confidence score
    
    # Relationships
    session: Mapped["RetrievalSession"] = relationship("RetrievalSession", back_populates="attempts")
    concept_node: Mapped["ConceptNode"] = relationship("ConceptNode")
    error_log: Mapped[Optional["DiagnosticErrorLog"]] = relationship("DiagnosticErrorLog", back_populates="attempt", uselist=False, cascade="all, delete-orphan")
    