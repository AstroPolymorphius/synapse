import enum
import uuid
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlalchemy import Text, Boolean, ForeignKey, DateTime, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database import UUIDModel, TimestampedModel

if TYPE_CHECKING:
    from backend.models.retrieval_attempt_model import RetrievalAttempt
    from backend.models.concept_node_model import ConceptNode

#Defines the ErrorCategory class which stores the different category of errors a student can make
class ErrorCategory(str, enum.Enum):
    SURFACE_MEMORIZATION = "surface memorization"
    DISCONNECTED_CONCEPT = "disconnected concept"
    INCOMPLETE_MENTAL_MODEL = "incomplete mental model"
    RETRIEVAL_DECAY = "retrieval decay"

class DiagnosticErrorLog(UUIDModel, TimestampedModel):
    __tablename__ = "diagnostic_error_logs"

    attempt_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("retrieval_attempts.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    concept_node_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("concept_nodes.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Error Root-Cause Categorization (e.g., "surface memorization", "broken_connection", "recall_decay")
    error_category: Mapped[ErrorCategory] = mapped_column(SQLEnum(ErrorCategory), nullable=False)
    reflective_correction: Mapped[Optional[str]] = mapped_column(Text, nullable=True) # Student's written fix or updated mental model notes
    is_resolved: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False) # unresolved, resolved
    
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    attempt: Mapped["RetrievalAttempt"] = relationship("RetrievalAttempt", back_populates="error_log")
    concept_node: Mapped["ConceptNode"] = relationship("ConceptNode", back_populates="error_logs", foreign_keys=[concept_node_id])