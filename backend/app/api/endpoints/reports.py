"""
Reports endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

from app.db.database import get_db
from app.models.report import Report, ReportType, ReportFormat

router = APIRouter()


class ReportGenerate(BaseModel):
    report_type: str
    format: str = "PDF"
    assessment_run_id: UUID | None = None
    parameters: dict = {}


@router.post("/exec")
async def generate_executive_report(
    report: ReportGenerate,
    db: AsyncSession = Depends(get_db)
):
    """Generate executive PDF report"""

    new_report = Report(
        report_type=ReportType[report.report_type.upper()],
        format=ReportFormat[report.format.upper()],
        assessment_run_id=report.assessment_run_id,
        parameters=report.parameters,
        file_path="/tmp/reports/exec_report.pdf",
        file_hash="placeholder_hash"
    )

    db.add(new_report)
    await db.commit()
    await db.refresh(new_report)

    return {
        "report_id": str(new_report.id),
        "report_type": new_report.report_type.value,
        "format": new_report.format.value,
        "generated_at": new_report.generated_at.isoformat(),
        "download_url": f"/api/v1/reports/{new_report.id}/download"
    }


@router.get("/{report_id}")
async def get_report(
    report_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Get report details"""
    stmt = select(Report).where(Report.id == report_id)
    result = await db.execute(stmt)
    report = result.scalar_one_or_none()

    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    return {
        "id": str(report.id),
        "report_type": report.report_type.value,
        "format": report.format.value,
        "generated_at": report.generated_at.isoformat(),
        "file_path": report.file_path
    }


@router.get("/{report_id}/download")
async def download_report(
    report_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Download report file"""
    stmt = select(Report).where(Report.id == report_id)
    result = await db.execute(stmt)
    report = result.scalar_one_or_none()

    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    # In production, this would read the actual file
    return {
        "message": "Report download would be triggered here",
        "file_path": report.file_path
    }
