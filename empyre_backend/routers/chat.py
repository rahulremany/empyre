from fastapi import APIRouter
from pydantic import BaseModel
from empyre_backend.services import ai_coach, profile_service

router = APIRouter(prefix="/chat", tags=["chat"])

class ChatRequest(BaseModel):
    user_id: str
    message: str
    profile_patch: dict = None

class ChatResponse(BaseModel):
    type: str                # "question", "plan", or "confirmation"
    field: str = None        # only for questions
    text: str = None
    plan: dict = None        # only for plans

@router.post("", response_model=ChatResponse)
async def chat(req: ChatRequest):
    # 1. Load or init profile
    profile = profile_service.get_or_create(req.user_id)

    # 2. Apply any incoming patch
    if req.profile_patch:
        profile = profile_service.apply_patch(profile, req.profile_patch)

    # 3. Decide which AI flow to run
    if not profile_service.is_core_complete(profile):
        resp = await ai_coach.core_loop(profile)
    elif profile.auxiliary_opt_in is None:
        resp = await ai_coach.aux_offer(profile)
    elif profile.auxiliary_opt_in and not profile_service.is_aux_complete(profile):
        resp = await ai_coach.aux_loop(profile)
    elif not profile_service.has_plan(profile):
        resp = await ai_coach.generate_plan_flow(profile)
    else:
        resp = await ai_coach.handle_tweak_or_log(profile, req.message)

    # 4. Persist updates
    profile_service.save(profile)

    # 5. Return the AI response object
    return ChatResponse(**resp) 