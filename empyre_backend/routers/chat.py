from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from empyre_backend.services import ai_coach, profile_service
from empyre_backend.db import get_db

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
async def chat(req: ChatRequest, db: AsyncSession = Depends(get_db)):
    # 1. Load or init profile
    profile = await profile_service.get_or_create(req.user_id, db)

    # 2. Apply any incoming patch (for manual updates)
    if req.profile_patch:
        profile = await profile_service.apply_patch(profile, req.profile_patch, req.user_id, db)

    # 3. If we have a pending question, try to extract the answer from the message
    if profile.get("pending_question") and req.message:
        # Handle auxiliary opt-in specially
        if profile.get("pending_question") == "auxiliary_opt_in":
            if "yes" in req.message.lower() or "sure" in req.message.lower() or "ok" in req.message.lower():
                profile["auxiliary_opt_in"] = True
            else:
                profile["auxiliary_opt_in"] = False
            profile.pop("pending_question", None)
        else:
            # Extract answer from user's message for other fields
            answer = await ai_coach.extract_answer(profile.get("pending_question"), req.message)
            if answer:
                profile[profile.get("pending_question")] = answer
                profile.pop("pending_question", None)  # Clear the pending question

    # 4. Decide which AI flow to run
    if not profile_service.is_core_complete(profile):
        resp = await ai_coach.core_loop(profile)
        # Mark the field as pending for next response
        if resp.get("type") == "question":
            profile["pending_question"] = resp.get("field")
    elif profile.get("auxiliary_opt_in") is None:
        resp = await ai_coach.aux_offer(profile)
        # Mark auxiliary_opt_in as pending
        profile["pending_question"] = "auxiliary_opt_in"
    elif profile.get("auxiliary_opt_in") and not profile_service.is_aux_complete(profile):
        resp = await ai_coach.aux_loop(profile)
        # Mark the field as pending for next response
        if resp.get("type") == "question":
            profile["pending_question"] = resp.get("field")
    elif not profile_service.has_plan(profile):
        resp = await ai_coach.generate_plan_flow(profile)
    else:
        resp = await ai_coach.handle_tweak_or_log(profile, req.message)

    # 5. Persist updates
    await profile_service.save(profile, req.user_id, db)

    # 6. Return the AI response object
    return ChatResponse(**resp) 