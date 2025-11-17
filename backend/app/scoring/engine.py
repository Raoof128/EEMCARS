"""
Essential Eight Scoring Engine
Implements maturity level scoring (0-3) for all eight pillars
"""
from typing import List, Dict, Any, Tuple
from datetime import datetime, timedelta
import hashlib
import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Control, MaturityRequirement, Evidence, Asset
from app.scoring.validators import EvidenceValidator
from app.scoring.maturity import MaturityCalculator


class ScoringEngine:
    """
    Core scoring engine for Essential Eight maturity assessment
    """

    def __init__(self, db_session: AsyncSession):
        self.db = db_session
        self.validator = EvidenceValidator()
        self.calculator = MaturityCalculator()

    async def score_control(
        self,
        control_id: str,
        asset_id: str,
        evidence_window_hours: int = 72
    ) -> Dict[str, Any]:
        """
        Score a specific control for an asset

        Args:
            control_id: Control identifier (e.g., 'E8-AC')
            asset_id: Asset UUID
            evidence_window_hours: Time window to consider evidence (default 72 hours)

        Returns:
            Scoring result with maturity level, score, and findings
        """
        # Fetch control and its requirements
        control = await self._get_control(control_id)
        if not control:
            raise ValueError(f"Control {control_id} not found")

        # Fetch asset
        asset = await self._get_asset(asset_id)
        if not asset:
            raise ValueError(f"Asset {asset_id} not found")

        # Fetch recent evidence
        evidence_cutoff = datetime.utcnow() - timedelta(hours=evidence_window_hours)
        evidence_list = await self._get_evidence(control.id, asset_id, evidence_cutoff)

        # Get maturity requirements sorted by level
        requirements = sorted(control.requirements, key=lambda r: r.maturity_level)

        # Score each maturity level
        maturity_scores = {}
        for requirement in requirements:
            level_score = await self._score_maturity_level(
                requirement,
                evidence_list,
                asset
            )
            maturity_scores[requirement.maturity_level] = level_score

        # Determine achieved maturity level
        achieved_level = self._determine_maturity_level(maturity_scores)

        # Calculate overall score
        overall_score = self.calculator.calculate_overall_score(
            maturity_scores,
            achieved_level,
            evidence_list
        )

        # Compile findings
        findings = self._compile_findings(maturity_scores, evidence_list)

        return {
            "control_id": control.id,
            "control_code": control.control_id,
            "control_name": control.name,
            "pillar": control.pillar.value,
            "asset_id": asset_id,
            "asset_name": asset.hostname,
            "maturity_level": achieved_level,
            "score": round(overall_score, 2),
            "passed_checks": sum(1 for ls in maturity_scores.values() if ls["passed"]),
            "total_checks": len(maturity_scores),
            "evidence_count": len(evidence_list),
            "maturity_scores": maturity_scores,
            "findings": findings,
            "timestamp": datetime.utcnow().isoformat()
        }

    async def _score_maturity_level(
        self,
        requirement: MaturityRequirement,
        evidence_list: List[Evidence],
        asset: Asset
    ) -> Dict[str, Any]:
        """
        Score a specific maturity level based on evidence
        """
        validation_criteria = requirement.validation_criteria or {}
        checks = validation_criteria.get("checks", [])

        if not checks:
            # No specific checks defined, basic validation
            return {
                "level": requirement.maturity_level,
                "passed": len(evidence_list) > 0,
                "score": 50.0 if evidence_list else 0.0,
                "details": "No specific validation criteria defined",
                "missing_checks": []
            }

        # Validate each check against evidence
        check_results = {}
        for check_name in checks:
            result = await self._validate_check(
                check_name,
                evidence_list,
                asset,
                requirement
            )
            check_results[check_name] = result

        passed_checks = sum(1 for r in check_results.values() if r["passed"])
        total_checks = len(checks)
        passed = passed_checks == total_checks
        score = (passed_checks / total_checks * 100) if total_checks > 0 else 0

        missing = [name for name, r in check_results.items() if not r["passed"]]

        return {
            "level": requirement.maturity_level,
            "passed": passed,
            "score": round(score, 2),
            "passed_checks": passed_checks,
            "total_checks": total_checks,
            "check_results": check_results,
            "missing_checks": missing,
            "requirement_text": requirement.requirement_text
        }

    async def _validate_check(
        self,
        check_name: str,
        evidence_list: List[Evidence],
        asset: Asset,
        requirement: MaturityRequirement
    ) -> Dict[str, Any]:
        """
        Validate a specific check against available evidence
        """
        # Map check names to validation logic
        validation_func = self.validator.get_validator(check_name)

        if validation_func:
            return await validation_func(evidence_list, asset, requirement)

        # Default validation: check if any evidence mentions this check
        for evidence in evidence_list:
            if check_name in str(evidence.evidence_data).lower():
                return {
                    "passed": True,
                    "message": f"Evidence found for {check_name}",
                    "evidence_id": str(evidence.id)
                }

        return {
            "passed": False,
            "message": f"No evidence found for {check_name}",
            "evidence_id": None
        }

    def _determine_maturity_level(self, maturity_scores: Dict[int, Dict]) -> int:
        """
        Determine the highest achieved maturity level
        All lower levels must also pass
        """
        if not maturity_scores:
            return 0

        achieved_level = 0
        for level in sorted(maturity_scores.keys()):
            if maturity_scores[level]["passed"]:
                achieved_level = level
            else:
                break  # Lower level failed, can't achieve higher levels

        return achieved_level

    def _compile_findings(
        self,
        maturity_scores: Dict[int, Dict],
        evidence_list: List[Evidence]
    ) -> Dict[str, Any]:
        """
        Compile findings and recommendations
        """
        findings = {
            "summary": [],
            "gaps": [],
            "evidence_quality": self._assess_evidence_quality(evidence_list),
            "recommendations": []
        }

        for level, score_data in sorted(maturity_scores.items()):
            if score_data["passed"]:
                findings["summary"].append(
                    f"Maturity Level {level}: PASSED ({score_data['score']}%)"
                )
            else:
                findings["summary"].append(
                    f"Maturity Level {level}: FAILED ({score_data['score']}%)"
                )
                findings["gaps"].append({
                    "level": level,
                    "missing_checks": score_data.get("missing_checks", []),
                    "requirement": score_data.get("requirement_text", "")
                })

        # Generate recommendations based on gaps
        if findings["gaps"]:
            next_level = min(gap["level"] for gap in findings["gaps"])
            findings["recommendations"].append(
                f"Focus on achieving Maturity Level {next_level}"
            )
            for gap in findings["gaps"]:
                if gap["level"] == next_level:
                    for check in gap["missing_checks"]:
                        findings["recommendations"].append(
                            f"Implement: {check.replace('_', ' ').title()}"
                        )

        return findings

    def _assess_evidence_quality(self, evidence_list: List[Evidence]) -> Dict[str, Any]:
        """
        Assess the quality and completeness of evidence
        """
        if not evidence_list:
            return {
                "score": 0,
                "status": "No Evidence",
                "issues": ["No evidence collected"]
            }

        total_score = 0
        issues = []

        # Check recency
        recent_cutoff = datetime.utcnow() - timedelta(hours=24)
        recent_evidence = [e for e in evidence_list if e.collected_at >= recent_cutoff]
        recency_score = (len(recent_evidence) / len(evidence_list)) * 100
        total_score += recency_score * 0.3

        if recency_score < 50:
            issues.append("Evidence is outdated (>24 hours)")

        # Check validity
        valid_evidence = [e for e in evidence_list if e.is_valid]
        validity_score = (len(valid_evidence) / len(evidence_list)) * 100
        total_score += validity_score * 0.4

        if validity_score < 100:
            issues.append(f"{len(evidence_list) - len(valid_evidence)} evidence items have validation errors")

        # Check collection methods diversity
        methods = set(e.collection_method for e in evidence_list if e.collection_method)
        diversity_score = min(len(methods) * 25, 100)  # Max 4 methods
        total_score += diversity_score * 0.3

        if len(methods) < 2:
            issues.append("Evidence from limited sources")

        return {
            "score": round(total_score, 2),
            "status": "Excellent" if total_score >= 80 else "Good" if total_score >= 60 else "Fair" if total_score >= 40 else "Poor",
            "recency_score": round(recency_score, 2),
            "validity_score": round(validity_score, 2),
            "diversity_score": round(diversity_score, 2),
            "issues": issues
        }

    async def _get_control(self, control_id: str) -> Control:
        """Fetch control with requirements"""
        stmt = select(Control).where(Control.control_id == control_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def _get_asset(self, asset_id: str) -> Asset:
        """Fetch asset"""
        stmt = select(Asset).where(Asset.id == asset_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def _get_evidence(
        self,
        control_id: str,
        asset_id: str,
        cutoff_time: datetime
    ) -> List[Evidence]:
        """Fetch recent evidence for control and asset"""
        stmt = select(Evidence).where(
            Evidence.control_id == control_id,
            Evidence.asset_id == asset_id,
            Evidence.collected_at >= cutoff_time
        ).order_by(Evidence.collected_at.desc())

        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    @staticmethod
    def calculate_evidence_hash(evidence_data: Dict[str, Any]) -> str:
        """Calculate SHA-256 hash of evidence data for integrity"""
        json_str = json.dumps(evidence_data, sort_keys=True)
        return hashlib.sha256(json_str.encode()).hexdigest()
