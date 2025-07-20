from fastapi import FastAPI
from empyre_backend.routers.chat import router as chat_router

app = FastAPI()

# Include routers
app.include_router(chat_router) 