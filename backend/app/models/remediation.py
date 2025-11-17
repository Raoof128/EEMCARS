"""
Remediation Task model
"""
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum
from app.db.database import Base


class TaskType(str, enum.Enum):
    ANSIBLE = "Ansible"
    POWERSHELL = "PowerShell"
    BASH = "Bash"
    MANUAL = "Manual"
    API = "API"


class TaskPriority(str, enum.Enum):
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class TaskStatus(str, enum.Enum):
    OPEN = "Open"
    IN_PROGRESS = "InProgress"
    COMPLETED = "Completed"
    FAILED = "Failed"
    CANCELLED = "Cancelled"


class RemediationTask(Base):
    __tablename__ = "remediation_tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    control_id = Column(UUID(as_uuid=True), ForeignKey("controls.id", ondelete="CASCADE"), nullable=False)
    asset_id = Column(UUID(as_uuid=True), ForeignKey("assets.id", ondelete="CASCADE"))
    task_type = Column(Enum(TaskType))
    title = Column(String(255), nullable=False)
    description = Column(Text)
    priority = Column(Enum(TaskPriority))
    status = Column(Enum(TaskStatus), default=TaskStatus.OPEN)
    playbook_path = Column(String(500))
    script_content = Column(Text)
    assigned_to = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    execution_log = Column(Text)
    execution_result = Column(JSONB)

    # Relationships
    control = relationship("Control", back_populates="remediation_tasks")
    asset = relationship("Asset", back_populates="remediation_tasks")

    def __repr__(self):
        return f"<RemediationTask {self.title} ({self.status})>"
