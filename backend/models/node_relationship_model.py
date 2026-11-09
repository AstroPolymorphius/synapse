import uuid
from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from backend.database import Base

class NodeRelationship(Base):
    __tablename__ = "node_relationships"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Directed edge: source_node -> target_node
    source_node_id = Column(UUID(as_uuid=True), ForeignKey("concept_nodes.id", ondelete="CASCADE"), nullable=False, index=True)
    target_node_id = Column(UUID(as_uuid=True), ForeignKey("concept_nodes.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Relationship categorization (e.g., "prerequisite", "causes", "composes", "correlates")
    relationship_type = Column(String(50), default="prerequisite", nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    source_node = relationship("ConceptNode", foreign_keys=[source_node_id], back_populates="outgoing_links")
    target_node = relationship("ConceptNode", foreign_keys=[target_node_id], back_populates="incoming_links")