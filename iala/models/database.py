from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
import datetime
from core.config import settings

engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI, 
    connect_args={"check_same_thread": False} if "sqlite" in settings.SQLALCHEMY_DATABASE_URI else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class UserMastery(Base):
    """
    SQLAlchemy model to persist user mastery scores per concept.
    """
    __tablename__ = "user_masteries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    concept = Column(String, index=True)
    mastery_level = Column(Float, default=0.0) # 0.0 to 1.0
    engagement_score = Column(Float, default=1.0) # 0.0 to 1.0 (e.g., 1.0 = highly engaged, 0.0 = frustrated)
    last_updated = Column(DateTime, default=datetime.datetime.utcnow)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
