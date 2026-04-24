from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid

from models.schemas import (
    SessionStartRequest, 
    SessionStartResponse,
    SessionRespondRequest,
    SessionRespondResponse,
    StudentModel
)
from models.database import get_db, UserMastery
from services.knowledge_graph import kg
from services.socratic_engine import engine

router = APIRouter(prefix="/session", tags=["session"])

@router.post("/start", response_model=SessionStartResponse)
def start_session(request: SessionStartRequest, db: Session = Depends(get_db)):
    """
    Initialize a learning path for the user based on the target topic.
    """
    concept = request.target_topic
    
    # Check if concept exists in KG
    if concept not in kg.graph:
        raise HTTPException(status_code=404, detail="Concept not found in Knowledge Graph.")
    
    # Get user mastery from DB
    masteries = db.query(UserMastery).filter(UserMastery.user_id == request.user_id).all()
    mastered_concepts = [m.concept for m in masteries if m.mastery_level > 0.8]
    
    # Check prerequisites
    if not kg.check_prerequisites_met(concept, mastered_concepts):
        prereqs = kg.get_prerequisites(concept)
        missing = [p for p in prereqs if p not in mastered_concepts]
        raise HTTPException(status_code=400, detail=f"Prerequisites not met. Missing: {missing}")

    session_id = str(uuid.uuid4())
    content = kg.get_content(concept)
    message = f"Welcome to the session on {concept}. Let's begin: {content}. What are your initial thoughts on this?"
    
    return SessionStartResponse(
        session_id=session_id,
        message=message,
        concept=concept
    )

@router.post("/respond", response_model=SessionRespondResponse)
def respond_session(request: SessionRespondRequest, db: Session = Depends(get_db)):
    """
    Process user input, update mastery, and return the next instruction/probe.
    """
    # Fetch or create user mastery for this concept
    mastery_record = db.query(UserMastery).filter(
        UserMastery.user_id == request.user_id,
        UserMastery.concept == request.concept
    ).first()
    
    if not mastery_record:
        mastery_record = UserMastery(user_id=request.user_id, concept=request.concept, mastery_level=0.0)
        db.add(mastery_record)
        db.commit()
        db.refresh(mastery_record)
        
    current_mastery = mastery_record.mastery_level

    # Pass to Socratic Engine
    socratic_response = engine.process_turn(
        user_id=request.user_id,
        concept=request.concept,
        user_input=request.user_input,
        current_mastery=current_mastery
    )
    
    # Update mastery based on engine assessment
    mastery_record.mastery_level = socratic_response.assessed_mastery
    db.commit()
    db.refresh(mastery_record)
    
    student_profile = StudentModel(
        mastery_level=mastery_record.mastery_level,
        engagement_score=mastery_record.engagement_score
    )
    
    return SessionRespondResponse(
        concept=request.concept,
        agent_response=socratic_response,
        student_profile=student_profile
    )
