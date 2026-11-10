import uuid
from typing import TYPE_CHECKING, Optional
from sqlalchemy import String, Text, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database import UUIDModel, TimestampedModel


# 2. Import the model conditionally so the type checker sees it, 
# but circular imports are avoided at runtime.
if TYPE_CHECKING:
    from backend.models.subject_workspace_model import SubjectWorkspace
    from backend.models.node_relationship_model import NodeRelationship
class ConceptNode(UUIDModel, TimestampedModel):
    __tablename__ = "concept_nodes"

    workspace_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("subject_workspaces.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Content & Metadata
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[Optional[str]] = mapped_column(Text, nullable=True) # Markdown or LaTeX notes explaining the first principle
    status: Mapped[str] = mapped_column(String(50), default="unexplored", nullable=False) # unexplored, learning, mastered
    mastery_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False) # 0.0 to 1.0 calculated from retrieval sessions
    
    # Canvas Spatial Coordinates (for persistent drag-and-drop UI positioning)
    position_x: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    position_y: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    

    # Relationships
    workspace: Mapped["SubjectWorkspace"] = relationship("SubjectWorkspace", back_populates="concept_nodes")
    
    # Outgoing and incoming directional relationships to other nodes
    outgoing_links: Mapped[list["NodeRelationship"]] = relationship("NodeRelationship", foreign_keys="[NodeRelationship.source_node_id]", back_populates="source_node", cascade="all, delete-orphan")
    incoming_links: Mapped[list["NodeRelationship"]] = relationship("NodeRelationship", foreign_keys="[NodeRelationship.target_node_id]", back_populates="target_node", cascade="all, delete-orphan")