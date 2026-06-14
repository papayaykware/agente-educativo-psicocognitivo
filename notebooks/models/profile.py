from pydantic import BaseModel

class CognitiveProfile(BaseModel):
    working_memory: float
    ambiguity_tolerance: float
    visual_vs_analytical: float
