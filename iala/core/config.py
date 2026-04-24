import os

class Config:
    PROJECT_NAME = "Intelligent Adaptive Learning Assistant (IALA)"
    VERSION = "0.1.0"
    
    # SQLite is used for MVP Phase 1 & 2
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///./iala.db")
    
    # Placeholder for LLM API keys
    LLM_API_KEY = os.getenv("LLM_API_KEY", "dummy-key-for-mvp")

settings = Config()
