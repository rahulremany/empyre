from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from empyre_backend.db import get_db, Laurel
from typing import List
from datetime import datetime

router = APIRouter(prefix="/laurels", tags=["laurels"])

class LaurelResponse(BaseModel):
    id: int
    user_id: str
    laurel_type: str
    points: int
    description: str
    created_at: datetime

    class Config:
        from_attributes = True

@router.get("/{user_id}", response_model=List[LaurelResponse])
async def get_laurels(user_id: str, db: AsyncSession = Depends(get_db)):
    """Get all laurels for a user"""
    result = await db.execute(select(Laurel).where(Laurel.user_id == user_id))
    laurels = result.scalars().all()
    return laurels

@router.post("/{user_id}/award")
async def award_laurel(
    user_id: str, 
    laurel_type: str = Query(..., description="Type of laurel"),
    points: int = Query(10, description="Points awarded"),
    description: str = Query("", description="Description of the achievement"),
    db: AsyncSession = Depends(get_db)
):
    """Award a laurel to a user"""
    laurel = Laurel(
        user_id=user_id,
        laurel_type=laurel_type,
        points=points,
        description=description
    )
    db.add(laurel)
    await db.commit()
    await db.refresh(laurel)
    return {"message": "Laurel awarded!", "laurel": laurel} 