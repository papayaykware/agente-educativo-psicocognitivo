from pydantic import BaseModel

class Interaction(BaseModel):
    student_id: str
    concept_id: str
    correct: bool
    response_time: float
