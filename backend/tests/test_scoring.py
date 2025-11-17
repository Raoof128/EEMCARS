"""
Tests for the scoring engine.
"""
import pytest
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession

from app.scoring.engine import ScoringEngine
from app.db.models import Control, Asset, Evidence, MaturityRequirement


@pytest.mark.asyncio
class TestScoringEngine:
    """Test the Essential Eight scoring engine."""

    @pytest.fixture
    async def scoring_engine(self, db: AsyncSession):
        """Create a scoring engine instance."""
        return ScoringEngine(db)

    @pytest.fixture
    async def test_control(self, db: AsyncSession) -> Control:
        """Create a test control."""
        control = Control(
            control_id="E8-AC-L2-REQ1",
            pillar="application_control",
            name="Application Whitelisting",
            description="Implement application whitelisting",
            maturity_level=2,
        )
        db.add(control)
        await db.commit()
        await db.refresh(control)
        return control

    @pytest.fixture
    async def test_asset(self, db: AsyncSession) -> Asset:
        """Create a test asset."""
        asset = Asset(
            name="TEST-ASSET-001",
            type="workstation",
            os="Windows 10",
            ip_address="10.0.1.100",
            status="active",
        )
        db.add(asset)
        await db.commit()
        await db.refresh(asset)
        return asset

    @pytest.fixture
    async def test_requirement(self, db: AsyncSession, test_control: Control) -> MaturityRequirement:
        """Create a test maturity requirement."""
        requirement = MaturityRequirement(
            control_id=test_control.id,
            maturity_level=2,
            requirement="Application whitelisting enabled",
            validation_criteria={
                "checks": ["applocker_enabled", "enforcement_mode"]
            },
        )
        db.add(requirement)
        await db.commit()
        await db.refresh(requirement)
        return requirement

    async def test_score_control_compliant(
        self,
        scoring_engine: ScoringEngine,
        test_control: Control,
        test_asset: Asset,
        db: AsyncSession,
    ):
        """Test scoring a compliant control."""
        # Create compliant evidence
        evidence = Evidence(
            control_id=test_control.id,
            asset_id=test_asset.id,
            source="defender_atp",
            collected_at=datetime.utcnow(),
            data={
                "applocker_enabled": True,
                "enforcement_mode": "Enabled",
            },
            validation_status="validated",
        )
        db.add(evidence)
        await db.commit()

        # Score the control
        result = await scoring_engine.score_control(
            control_id=test_control.control_id,
            asset_id=test_asset.id,
        )

        assert result is not None
        assert result["control_id"] == test_control.control_id
        assert result["achieved_level"] >= 2
        assert result["overall_score"] > 0.8

    async def test_score_control_non_compliant(
        self,
        scoring_engine: ScoringEngine,
        test_control: Control,
        test_asset: Asset,
        db: AsyncSession,
    ):
        """Test scoring a non-compliant control."""
        # Create non-compliant evidence
        evidence = Evidence(
            control_id=test_control.id,
            asset_id=test_asset.id,
            source="defender_atp",
            collected_at=datetime.utcnow(),
            data={
                "applocker_enabled": False,
                "enforcement_mode": "Disabled",
            },
            validation_status="validated",
        )
        db.add(evidence)
        await db.commit()

        # Score the control
        result = await scoring_engine.score_control(
            control_id=test_control.control_id,
            asset_id=test_asset.id,
        )

        assert result is not None
        assert result["achieved_level"] < 2
        assert result["overall_score"] < 0.5

    async def test_score_control_no_evidence(
        self,
        scoring_engine: ScoringEngine,
        test_control: Control,
        test_asset: Asset,
    ):
        """Test scoring a control with no evidence."""
        result = await scoring_engine.score_control(
            control_id=test_control.control_id,
            asset_id=test_asset.id,
        )

        assert result is not None
        assert result["achieved_level"] == 0
        assert result["overall_score"] == 0.0
        assert "no_evidence" in result["reasons"]

    async def test_score_control_stale_evidence(
        self,
        scoring_engine: ScoringEngine,
        test_control: Control,
        test_asset: Asset,
        db: AsyncSession,
    ):
        """Test scoring with stale evidence (outside time window)."""
        # Create old evidence
        old_date = datetime.utcnow() - timedelta(days=30)
        evidence = Evidence(
            control_id=test_control.id,
            asset_id=test_asset.id,
            source="defender_atp",
            collected_at=old_date,
            data={
                "applocker_enabled": True,
                "enforcement_mode": "Enabled",
            },
            validation_status="validated",
        )
        db.add(evidence)
        await db.commit()

        # Score with 72-hour window (should not find the old evidence)
        result = await scoring_engine.score_control(
            control_id=test_control.control_id,
            asset_id=test_asset.id,
            evidence_window_hours=72,
        )

        assert result is not None
        # Should treat as no evidence (stale)
        assert result["achieved_level"] == 0

    async def test_determine_maturity_level(self, scoring_engine: ScoringEngine):
        """Test maturity level determination logic."""
        # All requirements met
        scores = {
            0: 1.0,
            1: 1.0,
            2: 1.0,
        }
        level = scoring_engine._determine_maturity_level(scores)
        assert level == 2

        # Only level 0 and 1 met
        scores = {
            0: 1.0,
            1: 1.0,
            2: 0.5,  # Not fully met
        }
        level = scoring_engine._determine_maturity_level(scores)
        assert level == 1

        # None met
        scores = {
            0: 0.3,
            1: 0.2,
            2: 0.1,
        }
        level = scoring_engine._determine_maturity_level(scores)
        assert level == 0

    async def test_calculate_overall_score(self, scoring_engine: ScoringEngine):
        """Test overall score calculation."""
        maturity_scores = {
            0: 1.0,
            1: 0.8,
            2: 0.6,
        }

        score = scoring_engine.calculator.calculate_overall_score(
            maturity_scores=maturity_scores,
            achieved_level=1,
            evidence_list=[],
        )

        assert 0.0 <= score <= 1.0
        assert score > 0.6  # Should be influenced by good lower-level scores

    async def test_score_pillar(
        self,
        scoring_engine: ScoringEngine,
        test_control: Control,
        test_asset: Asset,
        db: AsyncSession,
    ):
        """Test scoring an entire pillar."""
        # Create evidence
        evidence = Evidence(
            control_id=test_control.id,
            asset_id=test_asset.id,
            source="defender_atp",
            collected_at=datetime.utcnow(),
            data={
                "applocker_enabled": True,
                "enforcement_mode": "Enabled",
            },
            validation_status="validated",
        )
        db.add(evidence)
        await db.commit()

        # Score the pillar
        result = await scoring_engine.score_pillar(
            pillar="application_control",
            asset_id=test_asset.id,
        )

        assert result is not None
        assert result["pillar"] == "application_control"
        assert "maturity_level" in result
        assert "overall_score" in result
        assert "controls" in result

    async def test_score_all_pillars(
        self,
        scoring_engine: ScoringEngine,
        test_asset: Asset,
    ):
        """Test scoring all Essential Eight pillars."""
        result = await scoring_engine.score_all_pillars(asset_id=test_asset.id)

        assert result is not None
        assert len(result) == 8  # All 8 Essential Eight pillars

        pillar_names = [p["pillar"] for p in result]
        expected_pillars = [
            "application_control",
            "patch_applications",
            "office_macros",
            "user_application_hardening",
            "restrict_admin_privileges",
            "patch_os",
            "multi_factor_authentication",
            "regular_backups",
        ]

        for expected in expected_pillars:
            assert expected in pillar_names
