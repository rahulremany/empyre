# AI coach service

import json
from typing import Union
from openai import OpenAI
from empyre_backend.utils.helpers import get_openai_key

# Initialize your OpenAI client
client = OpenAI(api_key=get_openai_key())

async def extract_answer(field: str, message: str) -> str:
    """Extract structured answer from user message for a specific field"""
    system_prompt = f"""
You are an AI assistant that extracts structured answers from user messages.

Field: {field}
User message: {message}

Extract the relevant answer for the field. Return ONLY the extracted value as a string, nothing else.

Examples:
- Field: "initial_goal", Message: "I want to build muscle" → "build muscle"
- Field: "knowledge_level", Message: "I'm a beginner" → "beginner"
- Field: "experience_years", Message: "I've been working out for 2 years" → "2"
- Field: "training_days_per_week", Message: "I can train 4 days a week" → "4"
- Field: "session_length_min", Message: "I have 45 minutes per session" → "45"
- Field: "equipment_access", Message: "I have a full gym" → "full gym"

Return the extracted value only.
"""
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Extract the answer for field '{field}' from: {message}"}
        ],
        temperature=0.1,
    )
    
    return response.choices[0].message.content.strip()

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
    system_prompt = """
v1.0.core_loop — You are Empyre, the AI fitness coach. You help users by asking one profile question at a time until all core fields are collected.
Core fields (in order): 
  1. initial_goal
  2. knowledge_level
  3. experience_years
  4. training_days_per_week
  5. session_length_min
  6. equipment_access

When called, you will receive:
  • profile_json: the current sparse JSON of the user's profile
  • knowledge_level (if already set) to tailor wording

Your job:
  1. Inspect profile_json and find the first missing core field.
  2. Ask exactly one clear, friendly question to collect that field, using language appropriate to the user's knowledge_level.
  3. Do NOT repeat fields already answered.
  4. Return your question as a JSON object:
     {
       "type":"question",
       "field":"<missing_field>",
       "text":"<your question here>"
     }
"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": json.dumps({"profile_json": profile, "knowledge_level": profile.get("knowledge_level")})}
        ],
        temperature=0.7,
    )
    return json.loads(response.choices[0].message.content)

async def aux_offer(profile: dict) -> dict:
    system_prompt = """
v1.0.aux_offer — You are Empyre, the AI coach. The user has completed all core fields. Now invite them to add optional details to enhance personalization.

When called, you will receive:
  • profile_json: the user's complete core profile JSON

Your job:
  1. Craft a **unique, personalized** yes/no question—just like a human coach—tailored to this specific user's journey so far.
  2. Emphasize that these optional details will enable even more precise, customized workouts and meal plans.
  3. Make it clear this step is optional and skipping will move directly to plan generation.
  4. Return exactly one JSON object:
     {
       "type":"decision",
       "field":"auxiliary_opt_in",
       "text":"<your personalized yes/no prompt>"
     }
"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": json.dumps({"profile_json": profile})}
        ],
        temperature=0.7,
    )
    return json.loads(response.choices[0].message.content)

async def aux_loop(profile: dict) -> dict:
    system_prompt = """
v1.0.aux_loop — You are Empyre, the AI coach. The user opted into optional details and we want to collect dynamic, personalized auxiliary fields that will enhance their specific fitness journey.

When called, you will receive:
  • profile_json: the current JSON with core + any answered auxiliary fields
  • auxiliary_opt_in: true

Your job:
  1. Analyze the user's profile (goals, experience, knowledge level, etc.) and determine what additional information would be most valuable for THEIR specific situation.
  2. Consider fields like: injury history, supplements, food preferences, allergies, favorite exercises, sleep patterns, stress levels, recovery capacity, specific body parts to focus on, dietary restrictions, training preferences, schedule constraints, etc.
  3. Ask ONE personalized question about the most relevant field for this specific user.
  4. Each user should get different questions based on their unique profile - no two users should have identical auxiliary field collection.
  5. Return as JSON:
     {
       "type":"question",
       "field":"<dynamic_field_name>",
       "text":"<your personalized question here>"
     }
  6. If the user has already answered several auxiliary questions, you may propose a custom field that could further refine their plan.
  7. Be creative and adaptive - think like a human coach who tailors their approach to each individual.
"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": json.dumps({
                "profile_json": profile,
                "auxiliary_opt_in": True
            })}
        ],
        temperature=0.7,
    )
    return json.loads(response.choices[0].message.content)

async def generate_plan_flow(profile: dict) -> dict:
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
  "split": {
    "type": "<string>",
    "days": {
      "Day 1": [ { "exercise": "<name>", "sets": <int>, "reps": <int> }, … ]
    }
  },
  "meals": {
    "target_macros": { "protein_g": <number>, "carbs_g": <number>, "fats_g": <number> },
    "sample_day": { "Meal 1": "<description>", …, "Meal 4": "<description>" }
  },
  "notes": "<optional summary or disclaimer>"
}
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": json.dumps({"profile_json": profile})}
        ],
        temperature=0.7,
    )
    content = response.choices[0].message.content
    plan = json.loads(content)
    # store on profile so has_plan() returns True
    profile["plan"] = plan
    return {"type": "plan", "plan": plan, "text": "Here's your personalized plan!"}

async def handle_tweak_or_log(profile: dict, message: str) -> dict:
    """Handle plan tweaks and workout logging after plan is generated"""
    system_prompt = """
v1.0.tweak_log — You are Empyre, the AI fitness coach. The user has a complete plan and is now requesting modifications or logging workouts.

When called, you will receive:
  • profile_json: the user's complete profile with plan
  • message: user's request for tweak or log

Your job:
  1. Determine if this is a plan tweak request or workout logging
  2. For tweaks: Suggest modifications to their plan based on their request
  3. For logging: Acknowledge the workout and provide encouragement
  4. Return as JSON:
     {
       "type": "confirmation",
       "text": "<your response>",
       "plan_update": { /* optional plan modifications */ }
     }
  5. Keep the Roman legion theme in your responses
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": json.dumps({
                "profile_json": profile,
                "message": message
            })}
        ],
        temperature=0.7,
    )
    return json.loads(response.choices[0].message.content) 