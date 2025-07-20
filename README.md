Empyre AI Fitness Coach
🚀 Live Demo: (coming soon)
📂 Repo: https://github.com/yourusername/empyre-ai-coach
🗓️ Status: In development (Jul 2025 – Present)

🎯 Project Overview
Empyre is a chat-first, AI-driven fitness coach that guides users from Novitius (rookie) to Gladiator (peak physique) through fully personalized workout and meal plans—and a Roman-themed gamification system that rewards real-world progress.

Chat-First UX: Single /chat endpoint powers onboarding, dynamic Q&A, plan generation, tweaks, and check-ins.

AI-Personalization: Leverages the OpenAI API to compute TDEE/macros, craft workouts, and adapt questions based on user knowledge level.

Roman Gamification: Earn “Laurels,” rise through ranks (Novitius → Miles → Centurion → … → Gladiator), and opt into bracketed leaderboards once advanced.

Safety & Reliability: Guardrails enforce healthy calorie deficits, rep/volume caps, retry logic, and fallback strategies to ensure safe, coherent plans.

🚩 Key Features
Dynamic Onboarding

Core vs. auxiliary fields collected via AI-driven prompts

Adaptive question phrasing for Beginner/Intermediate/Advanced lifters

Personalized Plans

Workout split JSON + meal plan JSON, complete with macros

Real-time plan tweaks and logging through the chat interface

Gamification & Progression

Automated rank calculation via Physique Index (TDEE, fullness, symmetry)

“Arena” leaderboard opt-in at Centurion+ rank for fair, bracketed competition

Robust AI Guardrails

Dynamic TDEE & macro formulas (max 40% deficit)

Rep limits (1–25), set limits (1–6), session volume caps

Fallback retries and minimal default routines if AI hiccups

🏗️ Architecture & Tech Stack
Backend:

FastAPI for REST endpoints

Uvicorn as ASGI server

Pydantic models for request/response validation

AI Integration:

OpenAI ChatCompletion API (GPT-4 and GPT-4o-mini)

Versioned system prompts stored in services/ai_coach.py

Data Layer (Dev Stub):

In‐memory profile_service for rapid prototyping

Future plans: PostgreSQL or MongoDB + Redis for session caching

Development:

Python 3.12, venv isolation

Modular service layers (profile, ai_coach, routers)

GitHub repo with CI-ready structure

🚀 Getting Started
Clone & enter repo

bash
Copy
Edit
git clone git@github.com:yourusername/empyre-ai-coach.git
cd empyre-ai-coach
Create & activate virtualenv

bash
Copy
Edit
python3 -m venv empyre_venv
source empyre_venv/bin/activate
Install dependencies

bash
Copy
Edit
pip install -r requirements.txt
Set your OpenAI key

bash
Copy
Edit
echo "OPENAI_API_KEY=sk-<YOUR_KEY>" > .env
Run the server

bash
Copy
Edit
uvicorn empyre_backend.utils.main:app --reload
Test the chat flow

bash
Copy
Edit
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"user_id":"test","message":"Hello"}'
