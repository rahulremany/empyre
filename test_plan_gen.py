import json
from empyre_backend.services.ai_coach import generate_plan

# Sample complete profile JSON
profile = {
    "user_id": "test_user",
    "initial_goal": "Get shredded",
    "knowledge_level": "Intermediate",
    "experience_years": 3,
    "training_days_per_week": 5,
    "session_length_min": 60,
    "equipment_access": "Full gym",
    "supplements": ["creatine", "whey"],
    "food_preferences": ["chicken", "rice", "broccoli"],
    "injuries": None,
    "physique_description": "Lean with some muscle",
    "anatomy_focus": "Shoulders"
}

# Call the plan generator and capture the raw response
raw = generate_plan(profile, raw=True)
print("RAW AI RESPONSE:")
print(raw)

# Try to parse it
try:
    parsed = json.loads(raw)
    print("PARSED JSON:")
    print(json.dumps(parsed, indent=2))
except Exception as e:
    print("JSON parse error:", e) 