from fastapi import APIRouter
from affective.classifier import classify_text

router = APIRouter()

@router.post("/classify")
def classify(payload: dict):
    text = payload.get("text", "")
    state = classify_text(text)
    return {"text": text, "affective_state": state}
