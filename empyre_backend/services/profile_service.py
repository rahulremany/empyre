# empyre_backend/services/profile_service.py
from typing import Dict, Any

# In-memory store for now
_STORE: Dict[str, Dict[str, Any]] = {}

def get_or_create(user_id: str) -> Dict[str, Any]:
    if user_id not in _STORE:
        _STORE[user_id] = {"user_id": user_id}
    return _STORE[user_id]

def apply_patch(profile: Dict[str, Any], patch: Dict[str, Any]) -> Dict[str, Any]:
    profile.update(patch)
    return profile

def is_core_complete(profile: Dict[str, Any]) -> bool:
    core = ["initial_goal", "knowledge_level", "experience_years",
            "training_days_per_week", "session_length_min", "equipment_access"]
    return all(f in profile for f in core)

def is_aux_complete(profile: Dict[str, Any]) -> bool:
    aux = ["supplements", "food_preferences", "injuries",
           "physique_description", "anatomy_focus"]
    return all(f in profile for f in aux if profile.get("auxiliary_opt_in"))

def has_plan(profile: Dict[str, Any]) -> bool:
    return "plan" in profile

def save(profile: Dict[str, Any]) -> None:
    _STORE[profile["user_id"]] = profile 