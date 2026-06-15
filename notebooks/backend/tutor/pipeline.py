"""
pipeline.py — Pipeline unificado del tutor adaptativo
Autor conceptual: Copilot
"""

from typing import Dict, Any

from dkt.predictor import predict_mastery
from affective.classifier import classify_text
from profile.updater import update_profile
from instructional.prompt_builder import build_instructional_prompt
from instructional.llm_client import LLMClient


# En esta versión, el "almacenamiento" del perfil es externo (DB o cache).
# Aquí definimos la interfaz esperada.


def run_tutor_pipeline(
    student_id: str,
    concept_id: str,
    user_text: str,
    extra: Dict[str, Any] | None,
    load_profile_fn,
    save_profile_fn,
) -> Dict[str, Any]:
    """
    Ejecuta el pipeline completo del tutor adaptativo.

    Parámetros:
    - student_id: ID del estudiante
    - concept_id: concepto objetivo
    - user_text: mensaje del estudiante
    - extra: dict opcional con metadatos (response_time, etc.)
    - load_profile_fn: función(student_id) -> perfil o None
    - save_profile_fn: función(student_id, perfil) -> None
    """

    extra = extra or {}

    # 1. Cargar perfil previo
    old_profile = load_profile_fn(student_id)

    # 2. Actualizar perfil con la nueva interacción
    interaction = {
        "text": user_text,
        "response_time": extra.get("response_time", 3.0)
    }
    new_profile = update_profile(old_profile, interaction)
    save_profile_fn(student_id, new_profile)

    # 3. Estado afectivo
    affective_state = classify_text(user_text)

    # 4. Mastery estimado
    mastery = predict_mastery(student_id)

    # 5. Construir prompt instruccional
    concept_name = extra.get("concept_name", f"Concepto {concept_id}")
    prompt = build_instructional_prompt(
        concept_id=concept_id,
        concept_name=concept_name,
        mastery=mastery,
        affective_state=affective_state,
        profile=new_profile,
    )

    # 6. Llamar al LLM
    llm = LLMClient()
    agent_reply = llm.generate(prompt, user_text)

    # 7. Devolver todo el contexto relevante
    return {
        "student_id": student_id,
        "concept_id": concept_id,
        "agent_reply": agent_reply,
        "affective_state": affective_state,
        "mastery": mastery,
        "profile": new_profile,
        "prompt_used": prompt
    }
