"""
Control and Maturity Requirement models
"""
from sqlalchemy import Column, String, Text, DateTime, Integer, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum
from app.db.database import Base


class ControlPillar(str, enum.Enum):
    APPLICATION_CONTROL = "Application Control"
    PATCH_APPLICATIONS = "Patch Applications"
    MICROSOFT_OFFICE_MACROS = "Configure Microsoft Office Macro Settings"
    USER_APPLICATION_HARDENING = "User Application Hardening"
    RESTRICT_ADMIN_PRIVILEGES = "Restrict Administrative Privileges"
    PATCH_OPERATING_SYSTEMS = "Patch Operating Systems"
    MULTI_FACTOR_AUTH = "Multi-Factor Authentication"
    REGULAR_BACKUPS = "Regular Backups"


class Control(Base):
    __tablename__ = "controls"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    control_id = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    pillar = Column(Enum(ControlPillar), nullable=False)
    acsc_reference = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    requirements = relationship("MaturityRequirement", back_populates="control", cascade="all, delete-orphan")
    evidence = relationship("Evidence", back_populates="control")
    assessment_results = relationship("AssessmentResult", back_populates="control")
    drift_events = relationship("DriftEvent", back_populates="control")
    remediation_tasks = relationship("RemediationTask", back_populates="control")

    def __repr__(self):
        return f"<Control {self.control_id}: {self.name}>"


class MaturityRequirement(Base):
    __tablename__ = "maturity_requirements"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    control_id = Column(UUID(as_uuid=True), ForeignKey("controls.id", ondelete="CASCADE"), nullable=False)
    maturity_level = Column(Integer, nullable=False)
    requirement_text = Column(Text, nullable=False)
    validation_criteria = Column(JSONB)
    remediation_guidance = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    control = relationship("Control", back_populates="requirements")

    def __repr__(self):
        return f"<MaturityRequirement L{self.maturity_level} for {self.control_id}>"
