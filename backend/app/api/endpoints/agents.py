"""
Agents endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

from app.db.database import get_db
from app.models.agent import Agent, AgentStatus

router = APIRouter()


class AgentRegister(BaseModel):
    agent_id: str
    asset_id: UUID
    agent_version: str
    platform: str
    capabilities: dict = {}


class AgentHeartbeat(BaseModel):
    agent_id: str
    status: str = "Active"


@router.post("/register")
async def register_agent(
    agent: AgentRegister,
    db: AsyncSession = Depends(get_db)
):
    """Register a new agent"""

    # Check if agent already exists
    stmt = select(Agent).where(Agent.agent_id == agent.agent_id)
    result = await db.execute(stmt)
    existing_agent = result.scalar_one_or_none()

    if existing_agent:
        # Update existing agent
        existing_agent.last_heartbeat = datetime.utcnow()
        existing_agent.status = AgentStatus.ACTIVE
        existing_agent.agent_version = agent.agent_version
        await db.commit()

        return {
            "agent_id": existing_agent.agent_id,
            "status": "updated"
        }

    new_agent = Agent(
        agent_id=agent.agent_id,
        asset_id=agent.asset_id,
        agent_version=agent.agent_version,
        platform=agent.platform,
        status=AgentStatus.ACTIVE,
        last_heartbeat=datetime.utcnow(),
        capabilities=agent.capabilities
    )

    db.add(new_agent)
    await db.commit()
    await db.refresh(new_agent)

    return {
        "agent_id": new_agent.agent_id,
        "status": "registered",
        "registered_at": new_agent.registered_at.isoformat()
    }


@router.post("/heartbeat")
async def agent_heartbeat(
    heartbeat: AgentHeartbeat,
    db: AsyncSession = Depends(get_db)
):
    """Agent heartbeat"""
    stmt = select(Agent).where(Agent.agent_id == heartbeat.agent_id)
    result = await db.execute(stmt)
    agent = result.scalar_one_or_none()

    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    agent.last_heartbeat = datetime.utcnow()
    agent.status = AgentStatus[heartbeat.status.upper()]
    await db.commit()

    return {
        "agent_id": agent.agent_id,
        "status": "acknowledged",
        "last_heartbeat": agent.last_heartbeat.isoformat()
    }


@router.get("/")
async def list_agents(
    status: str = None,
    db: AsyncSession = Depends(get_db)
):
    """List all agents"""
    stmt = select(Agent)

    if status:
        stmt = stmt.where(Agent.status == AgentStatus[status.upper()])

    stmt = stmt.order_by(Agent.last_heartbeat.desc())

    result = await db.execute(stmt)
    agents = result.scalars().all()

    return {
        "agents": [
            {
                "agent_id": a.agent_id,
                "asset_id": str(a.asset_id),
                "platform": a.platform,
                "agent_version": a.agent_version,
                "status": a.status.value,
                "last_heartbeat": a.last_heartbeat.isoformat() if a.last_heartbeat else None,
                "registered_at": a.registered_at.isoformat()
            }
            for a in agents
        ],
        "total": len(agents)
    }
