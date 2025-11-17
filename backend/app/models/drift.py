"""
Drift Event model
"""
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Boolean, Enum, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum
from app.db.database import Base


class DriftSeverity(str, enum.Enum):
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    INFO = "Info"


class DriftType(str, enum.Enum):
    REGRESSION = "Regression"
    IMPROVEMENT = "Improvement"
    CONFIGURATION = "Configuration"
    EVIDENCE = "Evidence"


class DriftEvent(Base):
    __tablename__ = "drift_events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    control_id = Column(UUID(as_uuid=True), ForeignKey("controls.id", ondelete="CASCADE"), nullable=False)
    asset_id = Column(UUID(as_uuid=True), ForeignKey("assets.id", ondelete="CASCADE"), nullable=False)
    previous_maturity_level = Column(Integer)
    current_maturity_level = Column(Integer)
    severity = Column(Enum(DriftSeverity))
    drift_type = Column(Enum(DriftType))
    description = Column(Text)
    detected_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    acknowledged = Column(Boolean, default=False)
    acknowledged_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    acknowledged_at = Column(DateTime(timezone=True))
    resolution_notes = Column(Text)

    # Relationships
    control = relationship("Control", back_populates="drift_events")
    asset = relationship("Asset", back_populates="drift_events")

    def __repr__(self):
        return f"<DriftEvent {self.drift_type} {self.severity}>"
