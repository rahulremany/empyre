from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from empyre_backend.routers.chat import router as chat_router
from empyre_backend.routers.laurels import router as laurels_router
from empyre_backend.routers.progress import router as progress_router
from empyre_backend.db import init_db

app = FastAPI(title="Empyre API", description="AI-powered fitness coaching platform")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    await init_db()

# Include routers
app.include_router(chat_router)
app.include_router(laurels_router)
app.include_router(progress_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 