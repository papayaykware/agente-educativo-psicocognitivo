from fastapi import APIRouter
from dkt.predictor import predict_mastery

router = APIRouter()

@router.get("/mastery/{student_id}")
def mastery(student_id: str):
    mastery_vector = predict_mastery(student_id)
    return {"student_id": student_id, "mastery": mastery_vector}
