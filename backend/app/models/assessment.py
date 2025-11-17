"""
Assessment models
"""
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Enum, Numeric, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum
from app.db.database import Base


class RunType(str, enum.Enum):
    FULL = "Full"
    INCREMENTAL = "Incremental"
    ON_DEMAND = "OnDemand"
    SCHEDULED = "Scheduled"


class RunStatus(str, enum.Enum):
    RUNNING = "Running"
    COMPLETED = "Completed"
    FAILED = "Failed"
    CANCELLED = "Cancelled"


class AssessmentRun(Base):
    __tablename__ = "assessment_runs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    run_type = Column(Enum(RunType), nullable=False)
    status = Column(Enum(RunStatus), nullable=False)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))
    triggered_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    total_assets = Column(Integer)
    total_controls = Column(Integer)
    overall_maturity_score = Column(Numeric(3, 2))
    results = Column(JSONB)
    error_log = Column(Text)

    # Relationships
    assessment_results = relationship("AssessmentResult", back_populates="assessment_run", cascade="all, delete-orphan")
    reports = relationship("Report", back_populates="assessment_run")

    def __repr__(self):
        return f"<AssessmentRun {self.id} {self.status}>"


class AssessmentResult(Base):
    __tablename__ = "assessment_results"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    assessment_run_id = Column(UUID(as_uuid=True), ForeignKey("assessment_runs.id", ondelete="CASCADE"), nullable=False)
    control_id = Column(UUID(as_uuid=True), ForeignKey("controls.id", ondelete="CASCADE"), nullable=False)
    asset_id = Column(UUID(as_uuid=True), ForeignKey("assets.id", ondelete="CASCADE"), nullable=False)
    maturity_level = Column(Integer)
    score = Column(Numeric(5, 2))
    passed_checks = Column(Integer)
    total_checks = Column(Integer)
    evidence_count = Column(Integer)
    findings = Column(JSONB)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    # Relationships
    assessment_run = relationship("AssessmentRun", back_populates="assessment_results")
    control = relationship("Control", back_populates="assessment_results")
    asset = relationship("Asset", back_populates="assessment_results")

    def __repr__(self):
        return f"<AssessmentResult L{self.maturity_level} for {self.control_id}>"
