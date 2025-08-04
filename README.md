# Empyre - AI-Powered Fitness Coach

A chat-first, AI-driven fitness coaching platform that replicates the experience of a world-class personal trainer with a motivating Roman legion narrative.

## 🏛️ Features

### Core Functionality
- **Dynamic Q&A Onboarding**: AI asks personalized questions to build user profiles
- **Personalized Plan Generation**: Complete workout splits and meal plans
- **Real-Time Tweaks & Logging**: Modify plans and log workouts
- **Roman-Themed Gamification**: Earn Laurels and progress through ranks
- **Database Persistence**: All data stored in PostgreSQL

### AI Capabilities
- **Progressive Conversations**: AI remembers context and builds profiles step-by-step
- **Smart Answer Extraction**: Automatically extracts structured data from natural language
- **Personalized Responses**: No two users get identical questioning
- **Health Guardrails**: Ensures safe, effective fitness plans

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL
- OpenAI API key

### Installation

1. **Clone and setup environment:**
```bash
git clone <repository>
cd EMPYRE
python3 -m venv empyre_venv
source empyre_venv/bin/activate  # On Windows: empyre_venv\Scripts\activate
pip install -r requirements.txt
```

2. **Setup database:**
```bash
# Create PostgreSQL database and user
psql postgres
CREATE DATABASE empyre;
CREATE USER app WITH PASSWORD 'JayZeeXx123';
GRANT ALL PRIVILEGES ON DATABASE empyre TO app;
\q

# Run migrations
alembic upgrade head
```

3. **Configure environment:**
```bash
# Copy and edit .env file
cp .env.example .env
# Add your OpenAI API key to .env
```

4. **Start the server:**
```bash
uvicorn empyre_backend.main:app --reload
```

## 📡 API Endpoints

### Chat Interface
- `POST /chat` - Main conversation endpoint
- `GET /docs` - Interactive API documentation

### Gamification
- `GET /laurels/{user_id}` - Get user's laurels
- `POST /laurels/{user_id}/award` - Award laurels

### Progress Tracking
- `POST /progress` - Log workouts/progress
- `GET /progress/{user_id}` - Get user's progress history

## 💬 Usage Example

### Start a conversation:
```json
POST /chat
{
  "user_id": "demo_user",
  "message": "Hi I want to get stronger"
}
```

### Response flow:
1. AI asks for fitness goal
2. AI asks for knowledge level
3. AI asks for experience years
4. AI asks for training days per week
5. AI asks for session length
6. AI asks for equipment access
7. AI offers optional auxiliary questions
8. AI generates complete personalized plan

## 🏗️ Architecture

### Backend Stack
- **FastAPI**: Modern async Python web framework
- **SQLAlchemy**: Async ORM for database operations
- **PostgreSQL**: Primary database with JSON support
- **OpenAI GPT-4/GPT-4o-mini**: AI conversation and plan generation
- **Alembic**: Database migrations

### Frontend Stack
- **Next.js 15**: React framework with App Router
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first styling
- **Framer Motion**: Smooth animations
- **Lucide React**: Icon library

### Database Schema
- `users`: User accounts
- `profiles`: User fitness profiles (JSON)
- `plans`: Generated workout/meal plans (JSON)
- `progress_logs`: Workout and progress tracking
- `laurels`: Gamification achievements

## 🎯 Core Features Status

- ✅ **Dynamic Onboarding**: Complete
- ✅ **Plan Generation**: Complete
- ✅ **Conversation Flow**: Complete
- ✅ **Database Persistence**: Complete
- ✅ **Gamification System**: Complete
- ✅ **Progress Tracking**: Complete
- ✅ **Roman Theming**: Complete
- ✅ **Frontend Interface**: Complete
- ✅ **Real-time Chat**: Complete

## 🔮 Future Enhancements

- **Form Analysis**: Real-time exercise form coaching
- **Mobile App**: React Native frontend
- **Social Features**: Arena leaderboard
- **Advanced Analytics**: Progress visualization
- **Integration**: Wearable device sync

## 📝 License

MIT License - see LICENSE file for details

---

**Empyre** - Where every warrior finds their path to glory! 🏛️⚔️
