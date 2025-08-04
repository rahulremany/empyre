from fastapi import FastAPI
from empyre_backend.routers.chat import router as chat_router
from empyre_backend.db import init_db

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    await init_db()

# Include routers
app.include_router(chat_router) 