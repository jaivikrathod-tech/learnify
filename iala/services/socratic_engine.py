import json
from models.schemas import SocraticResponse
from services.knowledge_graph import kg
from services.vector_store import vector_store

class SocraticEngine:
    """
    Core service that handles the Instructional Loop (Explain -> Probe -> Evaluate).
    For Phase 1 MVP, this simulates the LangGraph/LangChain logic and structured output.
    """
    
    SYSTEM_PROMPT = """
    You are an Intelligent Adaptive Learning Assistant, acting strictly as a "Socratic Mentor".
    Your goal is not just to give answers, but to guide the student to the answer through questioning and exploration.
    
    You operate in three states:
    1. Instruction: Deliver content concisely.
    2. Assessment: Challenge the user with a probe or question.
    3. Remediation: Address misconceptions found in State 2.
    
    Always return your response as a structured JSON object matching the SocraticResponse schema.
    """

    def _simulate_llm_call(self, prompt: str, user_input: str, concept: str, current_mastery: float) -> SocraticResponse:
        """
        Simulates the LLM call that would use LangChain and return structured output.
        In a real implementation, this would use `langchain_core.prompts` and a Gemini model
        with `with_structured_output(SocraticResponse)`.
        """
        # Simple rule-based simulation of Socratic reasoning based on user input length/keywords
        content = kg.get_content(concept)
        context = vector_store.search(user_input)
        
        if "don't know" in user_input.lower() or len(user_input) < 10:
            # Remediation state
            return SocraticResponse(
                state="Remediation",
                message=f"That's okay! Let's break it down. We were discussing {concept}. Remember: {content}. What part of that seems confusing?",
                assessed_mastery=max(0.0, current_mastery - 0.1),
                next_action="Probe further"
            )
        elif "is it" in user_input.lower() or "?" in user_input:
            # Instruction / Assessment state based on context
            return SocraticResponse(
                state="Instruction",
                message=f"Good question. Based on our verified materials: {context}. How do you think this applies to {concept}?",
                assessed_mastery=current_mastery + 0.05,
                next_action="Wait for user evaluation"
            )
        else:
            # Assessment state (assume user tried to answer)
            return SocraticResponse(
                state="Assessment",
                message=f"Interesting perspective on {concept}. If that's the case, what would happen if the opposite were true?",
                assessed_mastery=min(1.0, current_mastery + 0.2),
                next_action="Evaluate deep understanding"
            )

    def process_turn(self, user_id: str, concept: str, user_input: str, current_mastery: float) -> SocraticResponse:
        """
        Main entry point for the Socratic Engine to process a turn in the loop.
        """
        prompt = f"User: {user_id}\nConcept: {concept}\nCurrent Mastery: {current_mastery}\nSystem: {self.SYSTEM_PROMPT}"
        response = self._simulate_llm_call(prompt, user_input, concept, current_mastery)
        return response

# Singleton instance
engine = SocraticEngine()
