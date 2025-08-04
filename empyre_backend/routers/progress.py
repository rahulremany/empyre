from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from empyre_backend.db import get_db, ProgressLog
from typing import List, Dict, Any
from datetime import datetime

router = APIRouter(prefix="/progress", tags=["progress"])

class ProgressLogRequest(BaseModel):
    user_id: str
    log_type: str  # "workout", "measurement", "goal"
    log_data: Dict[str, Any]

class ProgressLogResponse(BaseModel):
    id: int
    user_id: str
    log_type: str
    log_data: Dict[str, Any]
    created_at: datetime

@router.post("", response_model=ProgressLogResponse)
async def log_progress(req: ProgressLogRequest, db: AsyncSession = Depends(get_db)):
    """Log progress (workout, measurements, etc.)"""
    progress_log = ProgressLog(
        user_id=req.user_id,
        log_type=req.log_type,
        log_data=req.log_data
    )
    db.add(progress_log)
    await db.commit()
    await db.refresh(progress_log)
    return progress_log

@router.get("/{user_id}", response_model=List[ProgressLogResponse])
async def get_progress(user_id: str, db: AsyncSession = Depends(get_db)):
    """Get all progress logs for a user"""
    result = await db.execute(select(ProgressLog).where(ProgressLog.user_id == user_id).order_by(ProgressLog.created_at.desc()))
    logs = result.scalars().all()
    return logs 