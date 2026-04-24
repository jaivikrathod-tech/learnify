from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class StudentModel(BaseModel):
    """
    Pydantic schema representing the user's current learning profile.
    """
    mastery_level: float = Field(default=0.0, ge=0.0, le=1.0, description="Mastery Level: 0.0 to 1.0 per concept")
    engagement_score: float = Field(default=1.0, ge=0.0, le=1.0, description="Engagement Score: Detection of frustration (0.0) or high engagement (1.0)")
    learning_style: str = Field(default="mixed", description="Prefers visual, code-heavy, or theoretical explanations")

class SessionStartRequest(BaseModel):
    user_id: str
    target_topic: str

class SessionStartResponse(BaseModel):
    session_id: str
    message: str
    concept: str

class SessionRespondRequest(BaseModel):
    user_id: str
    session_id: str
    concept: str
    user_input: str

class SocraticResponse(BaseModel):
    """
    Expected structured (JSON) AI response from the Socratic Engine.
    """
    state: str = Field(..., description="The current state: 'Instruction', 'Assessment', or 'Remediation'")
    message: str = Field(..., description="The response text provided to the user")
    assessed_mastery: float = Field(default=0.0, description="The LLM's assessment of the user's mastery (0.0-1.0) based on the input")
    next_action: str = Field(..., description="What the agent plans to do next (e.g., 'Probe further', 'Move to next concept')")

class SessionRespondResponse(BaseModel):
    concept: str
    agent_response: SocraticResponse
    student_profile: StudentModel
