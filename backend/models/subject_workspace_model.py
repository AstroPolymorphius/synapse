import uuid
from sqlalchemy import Column, String, Text, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from backend.database import Base

class SubjectWorkspace(Base):
    __tablename__ = "subject_workspaces"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    color_tag = Column(String(50), default="blue", nullable=False) # For UI workspace badges
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    owner = relationship("User", back_populates="workspaces")
    concept_nodes = relationship("ConceptNode", back_populates="workspace", cascade="all, delete-orphan")