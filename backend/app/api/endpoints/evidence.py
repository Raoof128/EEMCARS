"""
Evidence endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime
from uuid import UUID

from app.db.database import get_db
from app.models.evidence import Evidence
from app.scoring.engine import ScoringEngine

router = APIRouter()


class EvidenceCreate(BaseModel):
    asset_id: UUID
    control_id: UUID
    evidence_type: str
    evidence_data: Dict[str, Any]
    collection_method: str = "Manual"


@router.post("/")
async def create_evidence(
    evidence: EvidenceCreate,
    db: AsyncSession = Depends(get_db)
):
    """Ingest new evidence"""
    evidence_hash = ScoringEngine.calculate_evidence_hash(evidence.evidence_data)

    new_evidence = Evidence(
        asset_id=evidence.asset_id,
        control_id=evidence.control_id,
        evidence_type=evidence.evidence_type,
        evidence_data=evidence.evidence_data,
        evidence_hash=evidence_hash,
        collection_method=evidence.collection_method,
        is_valid=True
    )

    db.add(new_evidence)
    await db.commit()
    await db.refresh(new_evidence)

    return {
        "id": str(new_evidence.id),
        "asset_id": str(new_evidence.asset_id),
        "control_id": str(new_evidence.control_id),
        "evidence_type": new_evidence.evidence_type,
        "evidence_hash": new_evidence.evidence_hash,
        "collected_at": new_evidence.collected_at.isoformat(),
        "status": "created"
    }


@router.get("/")
async def list_evidence(
    asset_id: UUID = None,
    control_id: UUID = None,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """List evidence with optional filtering"""
    stmt = select(Evidence)

    if asset_id:
        stmt = stmt.where(Evidence.asset_id == asset_id)
    if control_id:
        stmt = stmt.where(Evidence.control_id == control_id)

    stmt = stmt.order_by(Evidence.collected_at.desc()).limit(limit)

    result = await db.execute(stmt)
    evidence_list = result.scalars().all()

    return {
        "evidence": [
            {
                "id": str(e.id),
                "asset_id": str(e.asset_id),
                "control_id": str(e.control_id),
                "evidence_type": e.evidence_type,
                "collected_at": e.collected_at.isoformat(),
                "is_valid": e.is_valid,
                "collection_method": e.collection_method
            }
            for e in evidence_list
        ],
        "total": len(evidence_list)
    }
