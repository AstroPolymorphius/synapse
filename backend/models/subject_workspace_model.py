import uuid
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database import UUIDModel, TimestampedModel

# 2. Import the model conditionally so the type checker sees it, 
# but circular imports are avoided at runtime.
if TYPE_CHECKING:
    from backend.models.user_account_model import User
    from backend.models.concept_node_model import ConceptNode

class SubjectWorkspace(UUIDModel, TimestampedModel):
    __tablename__ = "subject_workspaces"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    color_tag: Mapped[str] = mapped_column(String(50), default="blue", nullable=False) # For UI workspace badges
    
    # Relationships
    owner: Mapped["User"] = relationship("User", back_populates="workspaces")
    concept_nodes: Mapped[list["ConceptNode"]] = relationship("ConceptNode", back_populates="workspace", cascade="all, delete-orphan")