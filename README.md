# Empyre AI Fitness Coach

**🚀 Live Demo:** _(coming soon)_  
**📂 Repo:** https://github.com/yourusername/empyre-ai-coach  
**🗓️ Status:** In development (Jul 2025 – Present)

---

## 🎯 Project Overview

Empyre mimics a world-class personal trainer by:

- **Chat-First Onboarding**  
  Asking only the next most relevant question—tailored to each user’s knowledge level—until we have just enough data to build a plan.

- **AI-Powered Plan Generation**  
  Calls the OpenAI API (GPT-4o-mini) to compute TDEE/macros, craft workout splits (JSON), and generate meal plans—all behind guardrails:  
  - Max 40% calorie deficit (never below BMR)  
  - Protein ≥1.2 g/kg, fats ≥0.25 g/kg, carbs fill the rest  
  - 1–25 reps, 1–6 sets, volume caps tied to user schedule

- **Dynamic Tweaks & Logging**  
  Users message “machine broke” or “swap pull day” and the AI patches their plan JSON on the fly.

- **Roman Gamification**  
  Earn “Laurels” for every check-in, level up from **Novitius → Gladiator**, and—once a Centurion—opt into a bracketed “Arena” leaderboard.

---

## 🔧 Tech Stack

- **Backend:** Python • FastAPI • Uvicorn  
- **Data Validation:** Pydantic  
- **AI Integration:** OpenAI ChatCompletion API (GPT-4 & GPT-4o-mini)  
- **Development:** `venv`, `pip`, GitHub  
- **Testing:** In-memory profile stubs & smoke tests

---

## ⚙️ Installation

git clone git@github.com:yourusername/empyre-ai-coach.git
cd empyre-ai-coach

python3 -m venv empyre_venv
source empyre_venv/bin/activate

pip install -r requirements.txt

echo "OPENAI_API_KEY=sk-<YOUR_KEY>" > .env

uvicorn empyre_backend.utils.main:app --reload

---

## 📂 Repository Structure

```
empyre-ai-coach/
├── empyre_backend/
│   ├── routers/
│   │   └── chat.py
│   ├── services/
│   │   ├── ai_coach.py
│   │   └── profile_service.py
│   └── utils/
│       └── main.py
├── test_plan_gen.py
├── requirements.txt
└── README.md
