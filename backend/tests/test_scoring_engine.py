"""
Unit tests for Essential Eight Scoring Engine
"""
import pytest
from unittest.mock import Mock, AsyncMock
from datetime import datetime, timedelta
from uuid import uuid4

from app.scoring.engine import ScoringEngine
from app.scoring.validators import EvidenceValidator
from app.scoring.maturity import MaturityCalculator
from app.models.control import Control, MaturityRequirement, ControlPillar
from app.models.evidence import Evidence, CollectionMethod
from app.models.asset import Asset, AssetType, AssetCriticality


class TestScoringEngine:
    """Test cases for ScoringEngine"""

    @pytest.fixture
    def mock_db_session(self):
        """Create a mock database session"""
        return AsyncMock()

    @pytest.fixture
    def sample_control(self):
        """Create a sample control"""
        control = Control(
            id=uuid4(),
            control_id="E8-AC",
            name="Application Control",
            description="Test control",
            pillar=ControlPillar.APPLICATION_CONTROL,
            acsc_reference="ACSC-E8-AC"
        )

        # Add requirements
        control.requirements = [
            MaturityRequirement(
                id=uuid4(),
                control_id=control.id,
                maturity_level=1,
                requirement_text="Level 1 requirement",
                validation_criteria={"checks": ["whitelisting_enabled"]}
            ),
            MaturityRequirement(
                id=uuid4(),
                control_id=control.id,
                maturity_level=2,
                requirement_text="Level 2 requirement",
                validation_criteria={"checks": ["servers_protected", "validated_rules"]}
            ),
        ]

        return control

    @pytest.fixture
    def sample_asset(self):
        """Create a sample asset"""
        return Asset(
            id=uuid4(),
            hostname="TEST-WIN-001",
            ip_address="10.0.1.10",
            asset_type=AssetType.WINDOWS,
            operating_system="Windows 11",
            os_version="22H2",
            department="IT",
            criticality=AssetCriticality.HIGH,
            is_active=True,
            last_seen=datetime.utcnow()
        )

    @pytest.fixture
    def sample_evidence(self, sample_control, sample_asset):
        """Create sample evidence"""
        evidence_data = {
            "application_control": {
                "enabled": True,
                "rules_count": 25,
                "logging_enabled": True
            }
        }

        return [
            Evidence(
                id=uuid4(),
                asset_id=sample_asset.id,
                control_id=sample_control.id,
                evidence_type="ApplicationControl",
                evidence_data=evidence_data,
                evidence_hash=ScoringEngine.calculate_evidence_hash(evidence_data),
                collected_at=datetime.utcnow(),
                collection_method=CollectionMethod.AGENT,
                is_valid=True
            )
        ]

    def test_calculate_evidence_hash(self):
        """Test evidence hash calculation"""
        evidence_data = {"test": "data", "nested": {"key": "value"}}
        hash1 = ScoringEngine.calculate_evidence_hash(evidence_data)
        hash2 = ScoringEngine.calculate_evidence_hash(evidence_data)

        # Same data should produce same hash
        assert hash1 == hash2
        assert len(hash1) == 64  # SHA-256 produces 64 character hex

    def test_determine_maturity_level_all_passed(self):
        """Test maturity level determination when all levels pass"""
        maturity_scores = {
            1: {"passed": True, "score": 100},
            2: {"passed": True, "score": 95},
            3: {"passed": True, "score": 90}
        }

        engine = ScoringEngine(Mock())
        level = engine._determine_maturity_level(maturity_scores)

        assert level == 3

    def test_determine_maturity_level_partial(self):
        """Test maturity level when only lower levels pass"""
        maturity_scores = {
            1: {"passed": True, "score": 100},
            2: {"passed": True, "score": 95},
            3: {"passed": False, "score": 45}
        }

        engine = ScoringEngine(Mock())
        level = engine._determine_maturity_level(maturity_scores)

        assert level == 2

    def test_determine_maturity_level_none_passed(self):
        """Test maturity level when no levels pass"""
        maturity_scores = {
            1: {"passed": False, "score": 40},
            2: {"passed": False, "score": 30},
            3: {"passed": False, "score": 20}
        }

        engine = ScoringEngine(Mock())
        level = engine._determine_maturity_level(maturity_scores)

        assert level == 0

    def test_assess_evidence_quality_excellent(self, sample_evidence):
        """Test evidence quality assessment - excellent"""
        engine = ScoringEngine(Mock())
        quality = engine._assess_evidence_quality(sample_evidence)

        assert quality["score"] > 0
        assert "status" in quality
        assert isinstance(quality["issues"], list)

    def test_assess_evidence_quality_no_evidence(self):
        """Test evidence quality with no evidence"""
        engine = ScoringEngine(Mock())
        quality = engine._assess_evidence_quality([])

        assert quality["score"] == 0
        assert quality["status"] == "No Evidence"
        assert len(quality["issues"]) > 0


class TestMaturityCalculator:
    """Test cases for MaturityCalculator"""

    def test_calculate_overall_score_level_3(self):
        """Test overall score calculation for Level 3"""
        calculator = MaturityCalculator()

        maturity_scores = {
            1: {"passed": True, "score": 100},
            2: {"passed": True, "score": 95},
            3: {"passed": True, "score": 90}
        }

        evidence = [
            Mock(
                is_valid=True,
                collected_at=datetime.utcnow() - timedelta(hours=1)
            )
            for _ in range(5)
        ]

        score = calculator.calculate_overall_score(maturity_scores, 3, evidence)

        assert 0 <= score <= 100
        assert score > 80  # Level 3 with good evidence should score high

    def test_calculate_overall_score_no_evidence(self):
        """Test score with no evidence"""
        calculator = MaturityCalculator()

        maturity_scores = {1: {"passed": False, "score": 0}}

        score = calculator.calculate_overall_score(maturity_scores, 0, [])

        assert score == 0

    def test_calculate_trend_improving(self):
        """Test trend calculation - improving"""
        calculator = MaturityCalculator()

        historical = [
            {"timestamp": datetime.utcnow() - timedelta(days=30), "score": 60},
            {"timestamp": datetime.utcnow() - timedelta(days=20), "score": 70},
            {"timestamp": datetime.utcnow() - timedelta(days=10), "score": 80},
            {"timestamp": datetime.utcnow(), "score": 90},
        ]

        trend = calculator.calculate_trend(historical)

        assert trend["direction"] == "improving"
        assert trend["velocity"] > 0
        assert trend["total_change"] == 30

    def test_calculate_trend_degrading(self):
        """Test trend calculation - degrading"""
        calculator = MaturityCalculator()

        historical = [
            {"timestamp": datetime.utcnow() - timedelta(days=30), "score": 90},
            {"timestamp": datetime.utcnow() - timedelta(days=20), "score": 80},
            {"timestamp": datetime.utcnow() - timedelta(days=10), "score": 70},
            {"timestamp": datetime.utcnow(), "score": 60},
        ]

        trend = calculator.calculate_trend(historical)

        assert trend["direction"] == "degrading"
        assert trend["velocity"] < 0

    def test_calculate_pillar_aggregate(self):
        """Test aggregate pillar calculation"""
        calculator = MaturityCalculator()

        pillar_scores = [
            {"maturity_level": 3, "score": 95},
            {"maturity_level": 2, "score": 85},
            {"maturity_level": 3, "score": 90},
            {"maturity_level": 2, "score": 80},
        ]

        aggregate = calculator.calculate_pillar_aggregate(pillar_scores)

        assert aggregate["overall_maturity_level"] == 2  # Minimum
        assert aggregate["total_pillars"] == 4
        assert aggregate["pillars_at_target"] == 2  # Two at level 3
        assert 0 <= aggregate["average_score"] <= 100


class TestEvidenceValidator:
    """Test cases for EvidenceValidator"""

    def test_validator_registration(self):
        """Test that validators are properly registered"""
        validator = EvidenceValidator()

        # Check key validators exist
        assert "whitelisting_enabled" in validator.validators
        assert "mfa_online_services" in validator.validators
        assert "backup_schedule" in validator.validators

    @pytest.mark.asyncio
    async def test_validate_whitelisting_enabled_pass(self):
        """Test whitelisting validation - pass"""
        validator = EvidenceValidator()

        evidence = [
            Mock(
                evidence_data={
                    "application_control": {
                        "enabled": True,
                        "rules_count": 25
                    }
                },
                id=uuid4()
            )
        ]

        result = await validator._validate_whitelisting_enabled(
            evidence, Mock(), Mock()
        )

        assert result["passed"] is True
        assert "evidence_id" in result

    @pytest.mark.asyncio
    async def test_validate_whitelisting_enabled_fail(self):
        """Test whitelisting validation - fail"""
        validator = EvidenceValidator()

        evidence = [
            Mock(
                evidence_data={"other_data": "value"},
                id=uuid4()
            )
        ]

        result = await validator._validate_whitelisting_enabled(
            evidence, Mock(), Mock()
        )

        assert result["passed"] is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
