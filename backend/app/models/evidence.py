"""
Evidence model
"""
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum
from app.db.database import Base


class CollectionMethod(str, enum.Enum):
    AGENT = "Agent"
    API = "API"
    MANUAL = "Manual"
    INTEGRATION = "Integration"


class Evidence(Base):
    __tablename__ = "evidence"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    asset_id = Column(UUID(as_uuid=True), ForeignKey("assets.id", ondelete="CASCADE"), nullable=False)
    control_id = Column(UUID(as_uuid=True), ForeignKey("controls.id", ondelete="CASCADE"), nullable=False)
    evidence_type = Column(String(100), nullable=False)
    evidence_data = Column(JSONB, nullable=False)
    evidence_hash = Column(String(64), nullable=False)
    collected_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    collection_method = Column(Enum(CollectionMethod))
    is_valid = Column(Boolean, default=True)
    validation_errors = Column(JSONB)
    metadata = Column(JSONB)

    # Relationships
    asset = relationship("Asset", back_populates="evidence")
    control = relationship("Control", back_populates="evidence")

    def __repr__(self):
        return f"<Evidence {self.evidence_type} for {self.asset_id}>"
