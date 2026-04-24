from fastapi import FastAPI
from core.config import settings
from api.routes import router as session_router
from models.database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Intelligent Adaptive Learning Assistant (IALA) Core Infrastructure"
)

# Include routers
app.include_router(session_router)

@app.get("/")
def read_root():
    return {"message": f"Welcome to {settings.PROJECT_NAME}"}
