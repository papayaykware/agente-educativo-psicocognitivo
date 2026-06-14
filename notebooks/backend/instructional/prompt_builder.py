"""
prompt_builder.py — Construcción de prompts instruccionales adaptativos
Autor conceptual: Copilot
"""

from typing import Dict

def describe_mastery(mastery: Dict[str, float]) -> str:
    if not mastery:
        return "No hay datos suficientes sobre el dominio del estudiante."
    mastered = [c for c, v in mastery.items() if v >= 0.8]
    weak = [c for c, v in mastery.items() if v < 0.5]
    txt = []
    if mastered:
        txt.append(f"Domina bien: {', '.join(mastered)}.")
    if weak:
        txt.append(f"Tiene dificultades en: {', '.join(weak)}.")
    if not txt:
        txt.append("Su dominio es intermedio en la mayoría de conceptos.")
    return " ".join(txt)


def describe_affective_state(state: str) -> str:
    if state == "frustración":
        return "El estudiante muestra frustración; evita sobrecargar y ofrece pasos pequeños y validación frecuente."
    if state == "aburrimiento":
        return "El estudiante muestra aburrimiento; aumenta el reto y conecta con aplicaciones más avanzadas."
    if state == "flujo":
        return "El estudiante está en flujo; mantén el nivel actual de dificultad con ligeros incrementos."
    if state == "duda":
        return "El estudiante muestra duda; clarifica supuestos y ofrece ejemplos concretos."
    return "El estado afectivo es neutro; usa un tono claro y equilibrado."


def describe_profile(profile: Dict[str, float] | None) -> str:
    if not profile:
        return "No hay perfil psicocognitivo estable aún; usa explicaciones mixtas (intuitivas y formales)."
    wm = profile.get("working_memory", 0.5)
    amb = profile.get("ambiguity_tolerance", 0.5)
    vis = profile.get("visual_vs_analytical", 0.5)

    parts = []

    if wm < 0.4:
        parts.append("Limita la cantidad de información simultánea; fragmenta en pasos muy pequeños.")
    elif wm > 0.7:
        parts.append("Puede manejar explicaciones más densas y encadenar varios pasos.")

    if amb < 0.4:
        parts.append("Evita ambigüedades; sé explícito en definiciones y procedimientos.")
    elif amb > 0.7:
        parts.append("Tolera bien la exploración y las preguntas abiertas.")

    if vis > 0.6:
        parts.append("Prefiere ejemplos visuales, analogías espaciales y metáforas concretas.")
    elif vis < 0.4:
        parts.append("Prefiere formulaciones analíticas, simbólicas y paso a paso.")

    if not parts:
        parts.append("Usa un estilo equilibrado entre intuición y formalismo.")

    return " ".join(parts)


def build_instructional_prompt(
    concept_id: str,
    concept_name: str,
    mastery: Dict[str, float] | None,
    affective_state: str | None,
    profile: Dict[str, float] | None,
) -> str:
    """
    Construye el system prompt para el LLM en función del estado del estudiante.
    """

    mastery_txt = describe_mastery(mastery or {})
    affective_txt = describe_affective_state(affective_state or "neutral")
    profile_txt = describe_profile(profile)

    prompt = f"""
Eres un tutor educativo adaptativo especializado en el concepto: {concept_name} (ID: {concept_id}).

Contexto sobre el estudiante:
- Dominio actual: {mastery_txt}
- Estado afectivo: {affective_txt}
- Perfil psicocognitivo: {profile_txt}

Instrucciones:
- Adapta tu explicación al estado afectivo y al perfil descritos.
- Usa ejemplos concretos relacionados con el concepto {concept_name}.
- Ajusta la dificultad según el dominio estimado.
- Haz preguntas de comprobación breves tras cada bloque de explicación.
- Evita sobrecargar al estudiante; prioriza claridad sobre exhaustividad.

Responde ahora al estudiante de forma directa, sin mencionar estas instrucciones internas.
"""
    return prompt.strip()
