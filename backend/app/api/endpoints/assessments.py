"""
Assessment endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

from app.db.database import get_db
from app.models.assessment import AssessmentRun, RunType, RunStatus
from app.scoring.engine import ScoringEngine

router = APIRouter()


class AssessmentRunCreate(BaseModel):
    run_type: str = "OnDemand"
    asset_ids: list[UUID] = []
    control_ids: list[str] = []


async def run_assessment_task(run_id: UUID, db: AsyncSession):
    """Background task to run assessment"""
    # This would be implemented to actually run the assessment
    pass


@router.post("/run")
async def trigger_assessment(
    assessment: AssessmentRunCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """Trigger a full Essential Eight assessment"""
    new_run = AssessmentRun(
        run_type=RunType[assessment.run_type.upper()],
        status=RunStatus.RUNNING,
        total_assets=len(assessment.asset_ids),
        total_controls=len(assessment.control_ids) if assessment.control_ids else 8
    )

    db.add(new_run)
    await db.commit()
    await db.refresh(new_run)

    # Add background task
    # background_tasks.add_task(run_assessment_task, new_run.id, db)

    return {
        "assessment_run_id": str(new_run.id),
        "status": new_run.status.value,
        "started_at": new_run.started_at.isoformat(),
        "message": "Assessment started"
    }


@router.get("/{run_id}")
async def get_assessment_run(
    run_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Get assessment run details"""
    stmt = select(AssessmentRun).where(AssessmentRun.id == run_id)
    result = await db.execute(stmt)
    run = result.scalar_one_or_none()

    if not run:
        raise HTTPException(status_code=404, detail="Assessment run not found")

    return {
        "id": str(run.id),
        "run_type": run.run_type.value,
        "status": run.status.value,
        "started_at": run.started_at.isoformat(),
        "completed_at": run.completed_at.isoformat() if run.completed_at else None,
        "total_assets": run.total_assets,
        "total_controls": run.total_controls,
        "overall_maturity_score": float(run.overall_maturity_score) if run.overall_maturity_score else None,
        "results": run.results
    }


@router.get("/")
async def list_assessment_runs(
    limit: int = 20,
    db: AsyncSession = Depends(get_db)
):
    """List recent assessment runs"""
    stmt = select(AssessmentRun).order_by(
        AssessmentRun.started_at.desc()
    ).limit(limit)

    result = await db.execute(stmt)
    runs = result.scalars().all()

    return {
        "runs": [
            {
                "id": str(r.id),
                "run_type": r.run_type.value,
                "status": r.status.value,
                "started_at": r.started_at.isoformat(),
                "completed_at": r.completed_at.isoformat() if r.completed_at else None,
                "overall_maturity_score": float(r.overall_maturity_score) if r.overall_maturity_score else None
            }
            for r in runs
        ],
        "total": len(runs)
    }
