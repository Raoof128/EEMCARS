"""
Maturity calculation and weighting logic
"""
from typing import Dict, Any, List
from datetime import datetime, timedelta
from app.models import Evidence


class MaturityCalculator:
    """
    Calculates overall maturity scores with weighting and temporal decay
    """

    def __init__(
        self,
        evidence_weight: float = 0.3,
        validation_weight: float = 0.5,
        temporal_weight: float = 0.2
    ):
        self.evidence_weight = evidence_weight
        self.validation_weight = validation_weight
        self.temporal_weight = temporal_weight

    def calculate_overall_score(
        self,
        maturity_scores: Dict[int, Dict],
        achieved_level: int,
        evidence_list: List[Evidence]
    ) -> float:
        """
        Calculate overall score considering multiple factors

        Args:
            maturity_scores: Scores for each maturity level
            achieved_level: Highest achieved maturity level
            evidence_list: Available evidence

        Returns:
            Overall score (0-100)
        """
        if not maturity_scores:
            return 0.0

        # Base score from maturity level achievement
        base_score = achieved_level * 25  # Level 0=0, L1=25, L2=50, L3=75

        # Evidence completeness score
        evidence_score = self._calculate_evidence_score(evidence_list)

        # Validation quality score
        validation_score = self._calculate_validation_score(maturity_scores)

        # Temporal freshness score
        temporal_score = self._calculate_temporal_score(evidence_list)

        # Weighted total
        overall_score = (
            base_score * 0.4 +
            evidence_score * self.evidence_weight +
            validation_score * self.validation_weight +
            temporal_score * self.temporal_weight
        )

        return min(100.0, max(0.0, overall_score))

    def _calculate_evidence_score(self, evidence_list: List[Evidence]) -> float:
        """
        Score based on evidence completeness and quality
        """
        if not evidence_list:
            return 0.0

        # More evidence is better, up to a threshold
        evidence_count_score = min(len(evidence_list) * 10, 50)

        # Valid evidence is better
        valid_count = sum(1 for e in evidence_list if e.is_valid)
        validity_score = (valid_count / len(evidence_list)) * 50 if evidence_list else 0

        return evidence_count_score + validity_score

    def _calculate_validation_score(self, maturity_scores: Dict[int, Dict]) -> float:
        """
        Score based on validation pass rates
        """
        if not maturity_scores:
            return 0.0

        total_score = 0
        for level, score_data in maturity_scores.items():
            total_score += score_data.get("score", 0)

        return total_score / len(maturity_scores) if maturity_scores else 0

    def _calculate_temporal_score(self, evidence_list: List[Evidence]) -> float:
        """
        Score based on evidence freshness (temporal decay)
        """
        if not evidence_list:
            return 0.0

        now = datetime.utcnow()
        scores = []

        for evidence in evidence_list:
            age_hours = (now - evidence.collected_at).total_seconds() / 3600

            # Decay function: 100% at 0 hours, 50% at 24 hours, 0% at 72 hours
            if age_hours <= 24:
                score = 100
            elif age_hours <= 72:
                score = 100 - ((age_hours - 24) / 48 * 50)
            else:
                score = max(0, 50 - ((age_hours - 72) / 168 * 50))  # Gradual decay to 0 over 7 days

            scores.append(score)

        return sum(scores) / len(scores) if scores else 0

    def calculate_trend(
        self,
        historical_scores: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Calculate maturity trend over time

        Args:
            historical_scores: List of {timestamp, score, maturity_level}

        Returns:
            Trend analysis with direction and velocity
        """
        if len(historical_scores) < 2:
            return {
                "trend": "insufficient_data",
                "direction": "unknown",
                "velocity": 0,
                "confidence": "low"
            }

        # Sort by timestamp
        sorted_scores = sorted(historical_scores, key=lambda x: x["timestamp"])

        # Calculate trend
        first_score = sorted_scores[0]["score"]
        last_score = sorted_scores[-1]["score"]
        delta = last_score - first_score

        # Calculate velocity (change per day)
        time_delta = sorted_scores[-1]["timestamp"] - sorted_scores[0]["timestamp"]
        days = max(time_delta.total_seconds() / 86400, 1)
        velocity = delta / days

        # Determine trend direction
        if delta > 5:
            direction = "improving"
        elif delta < -5:
            direction = "degrading"
        else:
            direction = "stable"

        # Calculate confidence based on data points
        confidence = "high" if len(sorted_scores) >= 10 else "medium" if len(sorted_scores) >= 5 else "low"

        return {
            "trend": direction,
            "direction": direction,
            "velocity": round(velocity, 2),
            "total_change": round(delta, 2),
            "days_span": int(days),
            "data_points": len(sorted_scores),
            "confidence": confidence,
            "first_score": round(first_score, 2),
            "last_score": round(last_score, 2)
        }

    def calculate_pillar_aggregate(
        self,
        pillar_scores: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Calculate aggregate score across all Essential Eight pillars

        Args:
            pillar_scores: List of scores for each pillar

        Returns:
            Aggregate metrics and overall maturity level
        """
        if not pillar_scores:
            return {
                "overall_maturity_level": 0,
                "average_score": 0,
                "maturity_distribution": {},
                "pillars_at_target": 0,
                "total_pillars": 0
            }

        # Calculate overall maturity level (minimum across all pillars)
        maturity_levels = [p.get("maturity_level", 0) for p in pillar_scores]
        overall_maturity = min(maturity_levels) if maturity_levels else 0

        # Calculate average score
        scores = [p.get("score", 0) for p in pillar_scores]
        average_score = sum(scores) / len(scores) if scores else 0

        # Maturity distribution
        distribution = {}
        for level in range(4):
            distribution[f"level_{level}"] = maturity_levels.count(level)

        # Pillars at maturity level 3 (target)
        pillars_at_target = maturity_levels.count(3)

        return {
            "overall_maturity_level": overall_maturity,
            "average_score": round(average_score, 2),
            "maturity_distribution": distribution,
            "pillars_at_target": pillars_at_target,
            "total_pillars": len(pillar_scores),
            "target_completion_percent": round((pillars_at_target / len(pillar_scores)) * 100, 2) if pillar_scores else 0
        }
