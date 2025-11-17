"""
Core configuration settings for EEMCARS
"""
from pydantic_settings import BaseSettings
from typing import Optional, List
from functools import lru_cache


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Essential Eight Maturity Continuous Assessment & Remediation System"
    APP_VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = False

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://eemcars:eemcars123@localhost:5432/eemcars"
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 10

    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Azure Configuration
    AZURE_REGION: str = "australiaeast"
    AZURE_TENANT_ID: Optional[str] = None
    AZURE_CLIENT_ID: Optional[str] = None
    AZURE_CLIENT_SECRET: Optional[str] = None
    AZURE_KEYVAULT_URL: Optional[str] = None
    AZURE_STORAGE_ACCOUNT: Optional[str] = None
    AZURE_STORAGE_CONTAINER: str = "eemcars-evidence"

    # Microsoft Graph API
    GRAPH_API_ENDPOINT: str = "https://graph.microsoft.com/v1.0"
    GRAPH_API_SCOPES: List[str] = [
        "https://graph.microsoft.com/.default"
    ]

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    CACHE_TTL: int = 300

    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"

    # Assessment Configuration
    ASSESSMENT_SCHEDULE_DEFAULT: str = "0 */6 * * *"  # Every 6 hours
    DRIFT_DETECTION_ENABLED: bool = True
    EVIDENCE_RETENTION_DAYS: int = 365

    # Scoring Configuration
    SCORING_WEIGHTS: dict = {
        "evidence_completeness": 0.3,
        "validation_results": 0.5,
        "temporal_decay": 0.2
    }

    # Agent Configuration
    AGENT_HEARTBEAT_TIMEOUT_MINUTES: int = 15
    AGENT_VERSION_REQUIRED: str = "1.0.0"

    # Reporting
    REPORTS_STORAGE_PATH: str = "/tmp/eemcars/reports"
    REPORTS_RETENTION_DAYS: int = 90

    # Remediation
    REMEDIATION_AUTO_APPROVE: bool = False
    ANSIBLE_PLAYBOOK_PATH: str = "/app/ansible/playbooks"

    # Monitoring
    PROMETHEUS_ENABLED: bool = True
    LOG_LEVEL: str = "INFO"

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "https://eemcars.local"
    ]

    # Demo Mode
    DEMO_MODE: bool = False
    DEMO_DATA_SEED: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
