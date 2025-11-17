"""
Asset model
"""
from sqlalchemy import Column, String, DateTime, Boolean, Enum
from sqlalchemy.dialects.postgresql import UUID, JSONB, INET
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum
from app.db.database import Base


class AssetType(str, enum.Enum):
    WINDOWS = "Windows"
    LINUX = "Linux"
    MACOS = "MacOS"
    NETWORK = "Network"
    CLOUD = "Cloud"
    APPLICATION = "Application"


class AssetCriticality(str, enum.Enum):
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class Asset(Base):
    __tablename__ = "assets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    hostname = Column(String(255), nullable=False, index=True)
    ip_address = Column(INET)
    asset_type = Column(Enum(AssetType), nullable=False)
    operating_system = Column(String(100))
    os_version = Column(String(50))
    department = Column(String(100))
    criticality = Column(Enum(AssetCriticality))
    is_active = Column(Boolean, default=True)
    last_seen = Column(DateTime(timezone=True))
    metadata = Column(JSONB)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    evidence = relationship("Evidence", back_populates="asset", cascade="all, delete-orphan")
    assessment_results = relationship("AssessmentResult", back_populates="asset")
    drift_events = relationship("DriftEvent", back_populates="asset")
    remediation_tasks = relationship("RemediationTask", back_populates="asset")
    agents = relationship("Agent", back_populates="asset", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Asset {self.hostname} ({self.asset_type})>"
