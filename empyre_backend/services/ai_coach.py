# AI coach service

import json
from typing import Union
from openai import OpenAI
from empyre_backend.utils.helpers import get_openai_key

# Initialize your OpenAI client
client = OpenAI(api_key=get_openai_key())

def generate_plan(profile_json: dict, raw: bool = False) -> Union[dict, str]:
    """
    v1.0.plan_gen — You are Empyre, the AI fitness coach. Based on this user profile, generate a complete
    workout split and meal plan in JSON, adhering to all dynamic guardrails:

    1. Caloric deficit ≤ 40% of TDEE (never below BMR).
    2. Protein ≥1.2 g/kg, fats ≥0.25 g/kg, carbs fill remaining calories.
    3. Reps per set: 1–25 (burn sets up to 25 only if user asked).
    4. Sets per exercise: 1–6.
    5. Weekly training volume ≤ training_days_per_week × 2.5 hours.
    6. At least one compound per major muscle group.
    7. If BMI <17 or >40, or serious injury reported, include a medical disclaimer.
    """
    system_prompt = """
v1.0.plan_gen — You are Empyre, the AI fitness coach. Based on this user profile, generate a complete workout split and meal plan in JSON, adhering to all dynamic guardrails:

1. Caloric deficit ≤ 40% of TDEE (never below BMR).
2. Protein ≥1.2 g/kg, fats ≥0.25 g/kg, carbs fill remaining calories.
3. Reps per set: 1–25 (burn sets up to 25 only if user asked).
4. Sets per exercise: 1–6.
5. Weekly training volume ≤ training_days_per_week × 2.5 hours.
6. At least one compound per major muscle group.
7. If BMI <17 or >40, or serious injury reported, include a medical disclaimer.

Output only valid JSON matching this schema:
{
  "split": { "type": "<string>", "days": { "Day 1": [ { "exercise": "<name>", "sets": <int>, "reps": <int> }, … ] } },
  "meals": { "target_macros": { "protein_g": <number>, "carbs_g": <number>, "fats_g": <number> }, "sample_day": { "Meal 1": "<description>", …, "Meal 4": "<description>" } },
  "notes": "<optional summary or disclaimer>"
}
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system",  "content": system_prompt},
            {"role": "user",    "content": f"Profile: {json.dumps(profile_json)}\nGenerate plan now."}
        ],
        temperature=0.7,
    )
    content = response.choices[0].message.content
    if raw:
        return content
    try:
        return json.loads(content)
    except Exception:
        return {"error": "Invalid AI response"} 

import asyncio

async def core_loop(profile: dict) -> dict:
    # Ask for the first missing core field
    return {"type":"question", "field":"initial_goal", "text":"🏛️ Ave, warrior—what do you seek from Empyre today?"}

async def aux_offer(profile: dict) -> dict:
    return {
        "type":"decision",
        "field":"auxiliary_opt_in",
        "text":"Would you like to answer a few more optional questions to make your plan even more precise? (Yes/No)"
    }

async def aux_loop(profile: dict) -> dict:
    # A simple stub: ask for 'supplements'
    return {"type":"question", "field":"supplements", "text":"Which supplements do you use regularly?"}

async def generate_plan_flow(profile: dict) -> dict:
    # Stub a fake plan
    fake_plan = {"split": {"type":"Full Body", "days":{}}, "meals": {"target_macros":{}, "sample_day":{}}}
    # store on profile so has_plan() returns True
    profile["plan"] = fake_plan
    return {"type":"plan", "plan": fake_plan, "text":"Here’s a starter plan for you — more to come!"}

async def handle_tweak_or_log(profile: dict, message: str) -> dict:
    return {"type":"confirmation", "text":"Got it! I’ve recorded that tweak/log for you."} 