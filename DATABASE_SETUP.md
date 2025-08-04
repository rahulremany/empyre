# Database Setup Guide for Empyre

## 🗄️ Database Integration Complete!

Your Empyre app now has full PostgreSQL database integration with:
- ✅ SQLAlchemy async ORM
- ✅ Alembic migrations
- ✅ User profiles, plans, progress logs, and laurels tables
- ✅ Automatic database initialization on startup

## 📋 What You Need to Do:

### **A) Install PostgreSQL**

**Option 1: Homebrew (Recommended)**
```bash
brew install postgresql@15
brew services start postgresql@15
```

**Option 2: Download from postgresql.org**
- Visit https://www.postgresql.org/download/macosx/
- Download and install PostgreSQL

### **B) Create Database & User**

1. **Connect to PostgreSQL:**
```bash
psql postgres
```

2. **Create database and user:**
```sql
CREATE DATABASE empyre_db;
CREATE USER postgres WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE empyre_db TO postgres;
\q
```

### **C) Run Database Migrations**

1. **Initialize Alembic:**
```bash
alembic init alembic
```

2. **Create initial migration:**
```bash
alembic revision --autogenerate -m "Initial migration"
```

3. **Apply migration:**
```bash
alembic upgrade head
```

### **D) Monitor Your Database**

**Option 1: Command Line**
```bash
# Connect to database
psql -U postgres -d empyre_db

# View tables
\dt

# View data
SELECT * FROM profiles;
SELECT * FROM plans;
SELECT * FROM progress_logs;
SELECT * FROM laurels;

# Exit
\q
```

**Option 2: GUI Tools (Recommended)**
- **pgAdmin** (Free): https://www.pgadmin.org/
- **TablePlus** (Paid, but excellent): https://tableplus.com/
- **DBeaver** (Free): https://dbeaver.io/

### **E) Environment Variables**

Add to your `.env` file:
```bash
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost/empyre_db
```

## 🚀 Start Your App

```bash
# Install dependencies (already done)
pip install -r requirements.txt

# Start the server
uvicorn empyre_backend.utils.main:app --reload
```

## 📊 Database Schema

Your database now has these tables:

1. **users** - User authentication and basic info
2. **profiles** - Flexible JSON storage for user profiles
3. **plans** - Generated workout and meal plans
4. **progress_logs** - Workout logs and achievements
5. **laurels** - Gamification points and achievements

## 🔧 Troubleshooting

**If you get connection errors:**
1. Make sure PostgreSQL is running: `brew services list`
2. Check your database URL in `.env`
3. Verify database exists: `psql -U postgres -l`

**If migrations fail:**
1. Delete the `alembic/versions/` folder
2. Run `alembic revision --autogenerate -m "Initial migration"`
3. Run `alembic upgrade head`

## 🎯 Next Steps

Once your database is running:
1. Test the chat endpoint: `curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"user_id":"test","message":"Hello"}'`
2. Check the database to see user data being stored
3. Start building the frontend!

Your app now has persistent data storage! 🎉 