from fastapi import APIRouter
from instructional.prompt_builder import build_instructional_prompt
from dkt.predictor import predict_mastery
from affective.classifier import classify_text

router = APIRouter()

# Mapeo simple de conceptos (luego lo conectaremos al YAML)
CONCEPT_NAMES = {
    "A": "Introducción a Álgebra",
    "B": "Ecuaciones Lineales",
    "C": "Sistemas de Ecuaciones",
    "D": "Matrices",
    "E": "Determinantes"
}

@router.post("/{student_id}/{concept_id}")
def tutor(student_id: str, concept_id: str, payload: dict):
    user_text = payload.get("text", "")

    # 1. Estado afectivo
    affective_state = classify_text(user_text)

    # 2. Mastery estimado
    mastery = predict_mastery(student_id)

    # 3. Perfil psicocognitivo (placeholder)
    profile = None

    # 4. Construcción del prompt adaptativo
    concept_name = CONCEPT_NAMES.get(concept_id, "Concepto desconocido")
    prompt = build_instructional_prompt(
        concept_id=concept_id,
        concept_name=concept_name,
        mastery=mastery,
        affective_state=affective_state,
        profile=profile,
    )

    # 5. Respuesta del agente (simulada por ahora)
    agent_reply = f"Estoy analizando tu estado ({affective_state}) y tu dominio. Aquí tienes una explicación adaptada sobre {concept_name}."

    return {
        "student_id": student_id,
        "concept_id": concept_id,
        "affective_state": affective_state,
        "mastery": mastery,
        "prompt_used": prompt,
        "agent_reply": agent_reply
    }
