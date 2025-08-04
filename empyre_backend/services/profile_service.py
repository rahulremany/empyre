# empyre_backend/services/profile_service.py
from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from empyre_backend.db import Profile, get_db

async def get_or_create(user_id: str, db: AsyncSession) -> Dict[str, Any]:
    """Get existing profile or create new one"""
    # Check if profile exists
    result = await db.execute(select(Profile).where(Profile.user_id == user_id))
    profile = result.scalar_one_or_none()
    
    if not profile:
        # Create new profile
        profile = Profile(user_id=user_id, profile_data={"user_id": user_id})
        db.add(profile)
        await db.commit()
        await db.refresh(profile)
    
    return profile.profile_data

async def apply_patch(profile_data: Dict[str, Any], patch: Dict[str, Any], user_id: str, db: AsyncSession) -> Dict[str, Any]:
    """Apply patch to profile and save to database"""
    profile_data.update(patch)
    
    # Update in database
    result = await db.execute(select(Profile).where(Profile.user_id == user_id))
    profile = result.scalar_one_or_none()
    
    if profile:
        profile.profile_data = profile_data
        await db.commit()
    
    return profile_data

def is_core_complete(profile: Dict[str, Any]) -> bool:
    """Check if all core fields are present"""
    core = ["initial_goal", "knowledge_level", "experience_years",
            "training_days_per_week", "session_length_min", "equipment_access"]
    return all(f in profile for f in core)

def is_aux_complete(profile: Dict[str, Any]) -> bool:
    """Check if auxiliary fields are complete (if user opted in)"""
    if not profile.get("auxiliary_opt_in"):
        return True  # User didn't opt in, so it's "complete"
    
    # For now, consider it complete if they've answered at least 2 auxiliary questions
    aux_fields = [k for k in profile.keys() if k not in [
        "user_id", "initial_goal", "knowledge_level", "experience_years",
        "training_days_per_week", "session_length_min", "equipment_access",
        "auxiliary_opt_in", "plan"
    ]]
    return len(aux_fields) >= 2

def has_plan(profile: Dict[str, Any]) -> bool:
    """Check if user has a plan"""
    return "plan" in profile

async def save(profile_data: Dict[str, Any], user_id: str, db: AsyncSession) -> None:
    """Save profile to database"""
    result = await db.execute(select(Profile).where(Profile.user_id == user_id))
    profile = result.scalar_one_or_none()
    
    if profile:
        profile.profile_data = profile_data
    else:
        profile = Profile(user_id=user_id, profile_data=profile_data)
        db.add(profile)
    
    await db.commit() 