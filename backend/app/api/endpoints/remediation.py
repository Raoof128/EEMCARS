"""
Remediation endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from uuid import UUID

from app.db.database import get_db
from app.models.remediation import RemediationTask, TaskType, TaskPriority, TaskStatus

router = APIRouter()


class RemediationTaskCreate(BaseModel):
    control_id: UUID
    asset_id: UUID | None = None
    task_type: str
    title: str
    description: str
    priority: str = "Medium"
    playbook_path: str | None = None
    script_content: str | None = None


@router.post("/generate")
async def generate_remediation_tasks(
    control_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Auto-generate remediation tasks for a control"""
    # This would analyze assessment results and generate appropriate tasks
    return {
        "message": "Remediation tasks generated",
        "tasks_created": 0
    }


@router.post("/tasks")
async def create_remediation_task(
    task: RemediationTaskCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new remediation task"""
    new_task = RemediationTask(
        control_id=task.control_id,
        asset_id=task.asset_id,
        task_type=TaskType[task.task_type.upper()],
        title=task.title,
        description=task.description,
        priority=TaskPriority[task.priority.upper()],
        status=TaskStatus.OPEN,
        playbook_path=task.playbook_path,
        script_content=task.script_content
    )

    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)

    return {
        "id": str(new_task.id),
        "title": new_task.title,
        "status": new_task.status.value,
        "priority": new_task.priority.value,
        "created_at": new_task.created_at.isoformat()
    }


@router.get("/tasks")
async def list_remediation_tasks(
    status: str = None,
    limit: int = 50,
    db: AsyncSession = Depends(get_db)
):
    """List remediation tasks"""
    stmt = select(RemediationTask)

    if status:
        stmt = stmt.where(RemediationTask.status == TaskStatus[status.upper()])

    stmt = stmt.order_by(
        RemediationTask.priority,
        RemediationTask.created_at.desc()
    ).limit(limit)

    result = await db.execute(stmt)
    tasks = result.scalars().all()

    return {
        "tasks": [
            {
                "id": str(t.id),
                "title": t.title,
                "description": t.description,
                "task_type": t.task_type.value,
                "priority": t.priority.value,
                "status": t.status.value,
                "created_at": t.created_at.isoformat()
            }
            for t in tasks
        ],
        "total": len(tasks)
    }


@router.post("/tasks/{task_id}/execute")
async def execute_remediation_task(
    task_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Execute a remediation task"""
    stmt = select(RemediationTask).where(RemediationTask.id == task_id)
    result = await db.execute(stmt)
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # In production, this would trigger Ansible/PowerShell/Bash execution
    task.status = TaskStatus.IN_PROGRESS
    await db.commit()

    return {
        "id": str(task.id),
        "status": task.status.value,
        "message": "Task execution started"
    }
