"""
Dashboard endpoints
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime, timedelta

from app.db.database import get_db
from app.models.control import Control
from app.models.assessment import AssessmentResult
from app.models.drift import DriftEvent
from app.models.remediation import RemediationTask, TaskStatus
from app.models.asset import Asset

router = APIRouter()


@router.get("/summary")
async def get_dashboard_summary(db: AsyncSession = Depends(get_db)):
    """Get overall dashboard summary"""

    # Get total assets
    assets_stmt = select(func.count(Asset.id)).where(Asset.is_active == True)
    assets_result = await db.execute(assets_stmt)
    total_assets = assets_result.scalar()

    # Get total controls
    controls_stmt = select(func.count(Control.id))
    controls_result = await db.execute(controls_stmt)
    total_controls = controls_result.scalar()

    # Get recent assessment results
    recent_cutoff = datetime.utcnow() - timedelta(hours=24)
    recent_results_stmt = select(AssessmentResult).where(
        AssessmentResult.timestamp >= recent_cutoff
    ).order_by(AssessmentResult.timestamp.desc()).limit(100)
    results = await db.execute(recent_results_stmt)
    recent_results = list(results.scalars().all())

    # Calculate overall maturity
    if recent_results:
        maturity_levels = [r.maturity_level for r in recent_results if r.maturity_level is not None]
        overall_maturity = min(maturity_levels) if maturity_levels else 0
        avg_score = sum(float(r.score) for r in recent_results if r.score) / len(recent_results)
    else:
        overall_maturity = 0
        avg_score = 0

    # Get drift events (last 7 days)
    drift_cutoff = datetime.utcnow() - timedelta(days=7)
    drift_stmt = select(func.count(DriftEvent.id)).where(
        DriftEvent.detected_at >= drift_cutoff,
        DriftEvent.acknowledged == False
    )
    drift_result = await db.execute(drift_stmt)
    drift_count = drift_result.scalar()

    # Get open remediation tasks
    tasks_stmt = select(func.count(RemediationTask.id)).where(
        RemediationTask.status == TaskStatus.OPEN
    )
    tasks_result = await db.execute(tasks_stmt)
    open_tasks = tasks_result.scalar()

    # Maturity by pillar
    controls_stmt = select(Control)
    controls_result = await db.execute(controls_stmt)
    controls = list(controls_result.scalars().all())

    pillars_maturity = {}
    for control in controls:
        pillar = control.pillar.value
        if pillar not in pillars_maturity:
            pillars_maturity[pillar] = {
                "name": pillar,
                "maturity_level": 0,
                "score": 0,
                "status": "Not Assessed"
            }

    return {
        "overall_maturity_level": overall_maturity,
        "average_score": round(avg_score, 2),
        "total_assets": total_assets,
        "total_controls": total_controls,
        "drift_events": drift_count,
        "open_remediation_tasks": open_tasks,
        "pillars": list(pillars_maturity.values()),
        "last_updated": datetime.utcnow().isoformat()
    }


@router.get("/maturity-heatmap")
async def get_maturity_heatmap(db: AsyncSession = Depends(get_db)):
    """Get Essential Eight maturity heatmap"""

    controls_stmt = select(Control).order_by(Control.pillar, Control.control_id)
    controls_result = await db.execute(controls_stmt)
    controls = list(controls_result.scalars().all())

    heatmap = []
    for control in controls:
        # Get latest assessment result for this control
        latest_result_stmt = select(AssessmentResult).where(
            AssessmentResult.control_id == control.id
        ).order_by(AssessmentResult.timestamp.desc()).limit(1)

        result = await db.execute(latest_result_stmt)
        latest_result = result.scalar_one_or_none()

        heatmap.append({
            "control_id": control.control_id,
            "control_name": control.name,
            "pillar": control.pillar.value,
            "maturity_level": latest_result.maturity_level if latest_result else 0,
            "score": float(latest_result.score) if latest_result and latest_result.score else 0,
            "last_assessed": latest_result.timestamp.isoformat() if latest_result else None
        })

    return {
        "heatmap": heatmap,
        "total_controls": len(heatmap)
    }


@router.get("/trends")
async def get_trends(days: int = 30, db: AsyncSession = Depends(get_db)):
    """Get maturity trends over time"""

    cutoff = datetime.utcnow() - timedelta(days=days)

    stmt = select(AssessmentResult).where(
        AssessmentResult.timestamp >= cutoff
    ).order_by(AssessmentResult.timestamp)

    result = await db.execute(stmt)
    results = list(result.scalars().all())

    # Group by date
    daily_scores = {}
    for r in results:
        date_key = r.timestamp.date().isoformat()
        if date_key not in daily_scores:
            daily_scores[date_key] = []
        if r.score:
            daily_scores[date_key].append(float(r.score))

    trends = [
        {
            "date": date,
            "average_score": round(sum(scores) / len(scores), 2) if scores else 0,
            "assessment_count": len(scores)
        }
        for date, scores in sorted(daily_scores.items())
    ]

    return {
        "trends": trends,
        "days": days,
        "total_data_points": len(trends)
    }
