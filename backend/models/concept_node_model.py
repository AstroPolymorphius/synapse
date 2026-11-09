import uuid
from sqlalchemy import Column, String, Text, Float, Integer, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from backend.database import Base

class ConceptNode(Base):
    __tablename__ = "concept_nodes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("subject_workspaces.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Content & Metadata
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=True)  # Markdown or LaTeX notes explaining the first principle
    status = Column(String(50), default="unexplored", nullable=False)  # unexplored, learning, mastered
    mastery_score = Column(Float, default=0.0, nullable=False)  # 0.0 to 1.0 calculated from retrieval sessions
    
    # Canvas Spatial Coordinates (for persistent drag-and-drop UI positioning)
    position_x = Column(Float, default=0.0, nullable=False)
    position_y = Column(Float, default=0.0, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    workspace = relationship("SubjectWorkspace", back_populates="concept_nodes")
    
    # Outgoing and incoming directional relationships to other nodes
    outgoing_links = relationship(
        "NodeRelationship",
        foreign_keys="[NodeRelationship.source_node_id]",
        back_populates="source_node",
        cascade="all, delete-orphan"
    )
    incoming_links = relationship(
        "NodeRelationship",
        foreign_keys="[NodeRelationship.target_node_id]",
        back_populates="target_node",
        cascade="all, delete-orphan"
    )