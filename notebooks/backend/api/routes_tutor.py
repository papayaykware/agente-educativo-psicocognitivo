from instructional.llm_client import LLMClient

@router.post("/{student_id}/{concept_id}")
def tutor(student_id: str, concept_id: str, payload: dict):
    user_text = payload.get("text", "")

    affective_state = classify_text(user_text)
    mastery = predict_mastery(student_id)
    profile = None

    concept_name = CONCEPT_NAMES.get(concept_id, "Concepto desconocido")

    prompt = build_instructional_prompt(
        concept_id=concept_id,
        concept_name=concept_name,
        mastery=mastery,
        affective_state=affective_state,
        profile=profile,
    )

    llm = LLMClient()
    agent_reply = llm.generate(prompt, user_text)

    return {
        "student_id": student_id,
        "concept_id": concept_id,
        "affective_state": affective_state,
        "mastery": mastery,
        "agent_reply": agent_reply
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

from profile.updater import update_profile

# Cargar perfil previo (más adelante: desde DB)
profile = None

# Actualizar perfil con la interacción actual
interaction = {
    "text": user_text,
    "response_time": payload.get("response_time", 3.0)
}

profile = update_profile(profile, interaction)

from fastapi import APIRouter
from tutor.pipeline import run_tutor_pipeline

router = APIRouter()

# almacenamiento en memoria (placeholder)
PROFILE_STORE = {}

def load_profile(student_id: str):
    return PROFILE_STORE.get(student_id)

def save_profile(student_id: str, profile):
    PROFILE_STORE[student_id] = profile

@router.post("/{student_id}/{concept_id}")
def tutor(student_id: str, concept_id: str, payload: dict):
    user_text = payload.get("text", "")
    extra = {
        "response_time": payload.get("response_time", 3.0),
        "concept_name": payload.get("concept_name", f"Concepto {concept_id}")
    }

    result = run_tutor_pipeline(
        student_id=student_id,
        concept_id=concept_id,
        user_text=user_text,
        extra=extra,
        load_profile_fn=load_profile,
        save_profile_fn=save_profile,
    )

    return result

