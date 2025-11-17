"""
Controls endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from uuid import UUID

from app.db.database import get_db
from app.models.control import Control, MaturityRequirement
from app.scoring.engine import ScoringEngine

router = APIRouter()


@router.get("/")
async def list_controls(db: AsyncSession = Depends(get_db)):
    """List all Essential Eight controls"""
    stmt = select(Control).order_by(Control.control_id)
    result = await db.execute(stmt)
    controls = result.scalars().all()

    return {
        "controls": [
            {
                "id": str(c.id),
                "control_id": c.control_id,
                "name": c.name,
                "description": c.description,
                "pillar": c.pillar.value,
                "acsc_reference": c.acsc_reference
            }
            for c in controls
        ],
        "total": len(controls)
    }


@router.get("/{control_id}")
async def get_control(control_id: str, db: AsyncSession = Depends(get_db)):
    """Get specific control details"""
    stmt = select(Control).where(Control.control_id == control_id)
    result = await db.execute(stmt)
    control = result.scalar_one_or_none()

    if not control:
        raise HTTPException(status_code=404, detail="Control not found")

    # Get requirements
    req_stmt = select(MaturityRequirement).where(
        MaturityRequirement.control_id == control.id
    ).order_by(MaturityRequirement.maturity_level)
    req_result = await db.execute(req_stmt)
    requirements = req_result.scalars().all()

    return {
        "id": str(control.id),
        "control_id": control.control_id,
        "name": control.name,
        "description": control.description,
        "pillar": control.pillar.value,
        "acsc_reference": control.acsc_reference,
        "requirements": [
            {
                "maturity_level": r.maturity_level,
                "requirement_text": r.requirement_text,
                "validation_criteria": r.validation_criteria,
                "remediation_guidance": r.remediation_guidance
            }
            for r in requirements
        ]
    }


@router.post("/{control_id}/score")
async def score_control(
    control_id: str,
    asset_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Score a control for a specific asset"""
    engine = ScoringEngine(db)

    try:
        result = await engine.score_control(control_id, str(asset_id))
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scoring error: {str(e)}")


@router.get("/pillars/summary")
async def get_pillars_summary(db: AsyncSession = Depends(get_db)):
    """Get summary of all pillars"""
    stmt = select(Control).order_by(Control.pillar)
    result = await db.execute(stmt)
    controls = result.scalars().all()

    pillars = {}
    for control in controls:
        pillar_name = control.pillar.value
        if pillar_name not in pillars:
            pillars[pillar_name] = {
                "name": pillar_name,
                "controls": [],
                "control_count": 0
            }
        pillars[pillar_name]["controls"].append({
            "control_id": control.control_id,
            "name": control.name
        })
        pillars[pillar_name]["control_count"] += 1

    return {
        "pillars": list(pillars.values()),
        "total_pillars": len(pillars)
    }
