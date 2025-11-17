"""
Report model
"""
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum
from app.db.database import Base


class ReportType(str, enum.Enum):
    EXECUTIVE = "Executive"
    DETAILED = "Detailed"
    COMPLIANCE = "Compliance"
    TREND = "Trend"


class ReportFormat(str, enum.Enum):
    PDF = "PDF"
    CSV = "CSV"
    JSON = "JSON"
    HTML = "HTML"


class Report(Base):
    __tablename__ = "reports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    report_type = Column(Enum(ReportType))
    format = Column(Enum(ReportFormat))
    generated_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    assessment_run_id = Column(UUID(as_uuid=True), ForeignKey("assessment_runs.id"))
    parameters = Column(JSONB)
    file_path = Column(String(500))
    file_hash = Column(String(64))
    generated_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True))

    # Relationships
    assessment_run = relationship("AssessmentRun", back_populates="reports")

    def __repr__(self):
        return f"<Report {self.report_type} {self.format}>"
