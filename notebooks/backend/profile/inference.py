"""
inference.py — Inferencia del perfil psicocognitivo emergente
Autor conceptual: Copilot
"""

from typing import Dict

def infer_working_memory(interaction: Dict) -> float:
    """
    Inferencia heurística de memoria de trabajo.
    Basado en:
    - tiempo de respuesta
    - longitud del mensaje
    - número de pasos requeridos
    """
    rt = interaction.get("response_time", 3.0)
    msg_len = len(interaction.get("text", ""))

    score = 0.7 - 0.05 * (rt - 3) - 0.0005 * msg_len
    return max(0.1, min(0.9, score))


def infer_ambiguity_tolerance(interaction: Dict) -> float:
    """
    Basado en:
    - presencia de expresiones de duda
    - preguntas abiertas
    - tolerancia a explicaciones incompletas
    """
    text = interaction.get("text", "").lower()

    if "¿" in text or "?" in text or "no estoy seguro" in text:
        return 0.4
    if "creo que" in text or "quizá" in text:
        return 0.5
    return 0.6


def infer_visual_vs_analytical(interaction: Dict) -> float:
    """
    Basado en:
    - preferencia por ejemplos visuales
    - uso de lenguaje espacial
    - uso de lenguaje simbólico
    """
    text = interaction.get("text", "").lower()

    visual_cues = ["ver", "imaginar", "gráfico", "diagrama"]
    analytical_cues = ["ecuación", "paso", "variable", "resolver"]

    v = sum(1 for w in visual_cues if w in text)
    a = sum(1 for w in analytical_cues if w in text)

    if v > a:
        return 0.75
    if a > v:
        return 0.35
    return 0.55


def infer_profile_from_interaction(interaction: Dict) -> Dict[str, float]:
    """
    Devuelve un perfil psicocognitivo inferido a partir de una sola interacción.
    """
    return {
        "working_memory": infer_working_memory(interaction),
        "ambiguity_tolerance": infer_ambiguity_tolerance(interaction),
        "visual_vs_analytical": infer_visual_vs_analytical(interaction)
    }
