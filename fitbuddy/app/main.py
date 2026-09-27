from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import router
from app.database import init_db

app = FastAPI(title="FitBuddy - AI Fitness Plan Generator")

# Initialize database tables on startup
init_db()

# Mount static files directory (for background images like gym.jpg)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routing configurations
app.include_router(router)