import uuid
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from backend.database import UUIDModel, TimestampedModel

if TYPE_CHECKING:
    from backend.models.concept_node_model import ConceptNode

#The types of relationships students can make between nodes/concepts/ideas to strengthen their understanding
class RelationshipType(str, enum.Enum):
    IS_AN_EXAMPLE_OF = "is an example of"
    IS_A_PART_OF = "is a part of"
    CAUSES = "causes"
    PREVENTS = "prevents"
    ENABLES = "enables"
    REGULATES = "regulates"
    SIMILAR_TO = "similar to"
    CONTRASTS_WITH = "contrasts with"
    USED_FOR = "used for"
    DEPENDS_ON = "depends on"
    FOLLOWS = "follows"
    LOCATED = "located"

class NodeRelationship(UUIDModel, TimestampedModel):
    __tablename__ = "node_relationships"

    
    # Directed edge: source_node -> target_node
    source_node_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("concept_nodes.id", ondelete="CASCADE"), nullable=False, index=True)
    target_node_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("concept_nodes.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Relationship categorization (e.g., "prerequisite", "causes", "composes", "correlates")
    relationship_type: Mapped[RelationshipType] = mapped_column(SQLEnum(RelationshipType), default=RelationshipType.DEPENDS_ON, nullable=False)
    
    # Relationships
    source_node: Mapped["ConceptNode"] = relationship("ConceptNode", foreign_keys=[source_node_id], back_populates="outgoing_links")
    target_node: Mapped["ConceptNode"] = relationship("ConceptNode", foreign_keys=[target_node_id], back_populates="incoming_links")