"""
Demo data seeding script for EEMCARS
Populates the database with sample assets, evidence, and assessment results
"""
import asyncio
import sys
from pathlib import Path
from datetime import datetime, timedelta
import random
from uuid import uuid4

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.core.config import get_settings
from app.models.asset import Asset, AssetType, AssetCriticality
from app.models.evidence import Evidence, CollectionMethod
from app.models.assessment import AssessmentRun, AssessmentResult, RunType, RunStatus
from app.models.control import Control
from app.scoring.engine import ScoringEngine

settings = get_settings()

# Create async engine
engine = create_async_engine(settings.DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def seed_demo_assets(session: AsyncSession):
    """Create demo assets"""
    print("Creating demo assets...")

    demo_assets = [
        # Windows Workstations
        Asset(
            hostname="WIN-WS-001",
            ip_address="10.0.1.10",
            asset_type=AssetType.WINDOWS,
            operating_system="Windows 11 Enterprise",
            os_version="22H2",
            department="Finance",
            criticality=AssetCriticality.HIGH,
            is_active=True,
            last_seen=datetime.utcnow(),
            metadata={"location": "Sydney Office", "owner": "Finance Team"}
        ),
        Asset(
            hostname="WIN-WS-002",
            ip_address="10.0.1.11",
            asset_type=AssetType.WINDOWS,
            operating_system="Windows 11 Enterprise",
            os_version="22H2",
            department="HR",
            criticality=AssetCriticality.MEDIUM,
            is_active=True,
            last_seen=datetime.utcnow(),
            metadata={"location": "Melbourne Office", "owner": "HR Team"}
        ),
        # Linux Servers
        Asset(
            hostname="LNX-SRV-001",
            ip_address="10.0.2.10",
            asset_type=AssetType.LINUX,
            operating_system="Ubuntu Server",
            os_version="22.04 LTS",
            department="IT",
            criticality=AssetCriticality.CRITICAL,
            is_active=True,
            last_seen=datetime.utcnow(),
            metadata={"location": "Sydney DC", "role": "Web Server"}
        ),
        Asset(
            hostname="LNX-SRV-002",
            ip_address="10.0.2.11",
            asset_type=AssetType.LINUX,
            operating_system="Red Hat Enterprise Linux",
            os_version="8.7",
            department="IT",
            criticality=AssetCriticality.CRITICAL,
            is_active=True,
            last_seen=datetime.utcnow(),
            metadata={"location": "Melbourne DC", "role": "Database Server"}
        ),
        # Cloud Resources
        Asset(
            hostname="AZURE-VM-001",
            ip_address="10.0.3.10",
            asset_type=AssetType.CLOUD,
            operating_system="Windows Server 2022",
            os_version="21H2",
            department="DevOps",
            criticality=AssetCriticality.HIGH,
            is_active=True,
            last_seen=datetime.utcnow(),
            metadata={"location": "Azure Australia East", "role": "Application Server"}
        ),
    ]

    for asset in demo_assets:
        session.add(asset)

    await session.commit()
    print(f"Created {len(demo_assets)} demo assets")

    return demo_assets


async def seed_demo_evidence(session: AsyncSession, assets: list, controls: list):
    """Create demo evidence for various controls"""
    print("Creating demo evidence...")

    evidence_count = 0

    for asset in assets[:3]:  # Evidence for first 3 assets
        for control in controls[:5]:  # Evidence for first 5 controls
            # Create 1-3 evidence items per asset/control combination
            num_evidence = random.randint(1, 3)

            for i in range(num_evidence):
                # Randomize collection time (last 7 days)
                collected_at = datetime.utcnow() - timedelta(days=random.randint(0, 7))

                # Generate control-specific evidence data
                evidence_data = generate_evidence_data(control.control_id, asset)

                evidence = Evidence(
                    asset_id=asset.id,
                    control_id=control.id,
                    evidence_type=f"{control.control_id}_Check",
                    evidence_data=evidence_data,
                    evidence_hash=ScoringEngine.calculate_evidence_hash(evidence_data),
                    collected_at=collected_at,
                    collection_method=random.choice([CollectionMethod.AGENT, CollectionMethod.API]),
                    is_valid=True,
                    validation_errors=None
                )

                session.add(evidence)
                evidence_count += 1

    await session.commit()
    print(f"Created {evidence_count} demo evidence items")


def generate_evidence_data(control_id: str, asset: Asset) -> dict:
    """Generate realistic evidence data based on control type"""

    if control_id == "E8-AC":  # Application Control
        return {
            "application_control": {
                "enabled": random.choice([True, False]),
                "rules_count": random.randint(10, 50),
                "logging_enabled": True
            }
        }

    elif control_id == "E8-PA":  # Patch Applications
        return {
            "patch_compliance": {
                "missing_patches_count": random.randint(0, 15),
                "within_14_days_percent": random.randint(75, 100),
                "last_patch_date": (datetime.utcnow() - timedelta(days=random.randint(1, 30))).isoformat()
            }
        }

    elif control_id == "E8-MS":  # Macro Settings
        return {
            "macros_disabled": random.choice([True, True, False]),  # 2/3 probability True
            "internet_macros_blocked": random.choice([True, False]),
            "trusted_locations_configured": True
        }

    elif control_id == "E8-UAH":  # User Application Hardening
        return {
            "flash_blocked": True,
            "java_disabled": random.choice([True, False]),
            "ads_blocked": True,
            "pdf_javascript_disabled": random.choice([True, False])
        }

    elif control_id == "E8-RAP":  # Restrict Admin Privileges
        return {
            "admin_accounts_count": random.randint(2, 10),
            "separation_of_duties": True,
            "admin_internet_restricted": random.choice([True, False])
        }

    elif control_id == "E8-POS":  # Patch OS
        return {
            "os_patch_age_days": random.randint(1, 45),
            "os_version_supported": True,
            "critical_patches_missing": random.randint(0, 3)
        }

    elif control_id == "E8-MFA":  # MFA
        return {
            "mfa_online_services": random.choice([True, False]),
            "mfa_remote_access": True,
            "mfa_privileged_actions": random.choice([True, False])
        }

    elif control_id == "E8-RB":  # Backups
        return {
            "backup_schedule_configured": True,
            "backup_retention_days": random.randint(30, 90),
            "last_backup_days_ago": random.randint(0, 7),
            "offline_backups": random.choice([True, False])
        }

    return {"status": "checked"}


async def seed_demo_assessments(session: AsyncSession, assets: list, controls: list):
    """Create demo assessment runs"""
    print("Creating demo assessment runs...")

    # Create 3 historical assessment runs
    for i in range(3):
        run_date = datetime.utcnow() - timedelta(days=30 - (i * 10))

        assessment = AssessmentRun(
            run_type=RunType.SCHEDULED,
            status=RunStatus.COMPLETED,
            started_at=run_date,
            completed_at=run_date + timedelta(minutes=random.randint(10, 30)),
            total_assets=len(assets),
            total_controls=len(controls),
            overall_maturity_score=random.uniform(1.5, 2.5),
            results={"summary": f"Assessment run {i+1} completed successfully"}
        )

        session.add(assessment)
        await session.flush()

        # Create results for each control
        for control in controls:
            for asset in assets[:3]:  # Results for first 3 assets
                maturity_level = random.randint(1, 3)
                score = random.uniform(60, 95)

                result = AssessmentResult(
                    assessment_run_id=assessment.id,
                    control_id=control.id,
                    asset_id=asset.id,
                    maturity_level=maturity_level,
                    score=score,
                    passed_checks=random.randint(2, 5),
                    total_checks=5,
                    evidence_count=random.randint(1, 3),
                    findings={"status": f"Level {maturity_level} achieved"},
                    timestamp=run_date
                )

                session.add(result)

    await session.commit()
    print("Created demo assessment runs with results")


async def main():
    """Main seeding function"""
    print("=" * 60)
    print("EEMCARS Demo Data Seeding")
    print("=" * 60)

    async with AsyncSessionLocal() as session:
        # Get existing controls
        from sqlalchemy import select
        result = await session.execute(select(Control))
        controls = list(result.scalars().all())

        if not controls:
            print("ERROR: No controls found in database. Run schema.sql first.")
            return

        print(f"Found {len(controls)} controls in database")

        # Seed data
        assets = await seed_demo_assets(session)
        await seed_demo_evidence(session, assets, controls)
        await seed_demo_assessments(session, assets, controls)

        print("=" * 60)
        print("✅ Demo data seeding completed successfully!")
        print("=" * 60)
        print("\nDemo credentials:")
        print("  Username: admin | Password: DemoUser123!")
        print("  Username: secops | Password: DemoUser123!")
        print("\nAccess the dashboard at: http://localhost:3000")


if __name__ == "__main__":
    asyncio.run(main())
