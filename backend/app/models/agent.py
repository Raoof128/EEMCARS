"""
Agent model
"""
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum
from app.db.database import Base


class AgentStatus(str, enum.Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    ERROR = "Error"


class Agent(Base):
    __tablename__ = "agents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id = Column(String(100), unique=True, nullable=False, index=True)
    asset_id = Column(UUID(as_uuid=True), ForeignKey("assets.id", ondelete="CASCADE"), nullable=False)
    agent_version = Column(String(50))
    platform = Column(String(50))
    status = Column(Enum(AgentStatus), default=AgentStatus.ACTIVE)
    last_heartbeat = Column(DateTime(timezone=True), index=True)
    capabilities = Column(JSONB)
    registered_at = Column(DateTime(timezone=True), server_default=func.now())
    configuration = Column(JSONB)

    # Relationships
    asset = relationship("Asset", back_populates="agents")

    def __repr__(self):
        return f"<Agent {self.agent_id} ({self.status})>"
