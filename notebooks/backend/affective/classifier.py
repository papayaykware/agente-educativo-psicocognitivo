"""
classifier.py — Clasificador afectivo heurístico
Autor conceptual: Copilot
"""

import re

FRUSTRATION_PATTERNS = [
    r"no entiendo",
    r"no sé",
    r"esto es difícil",
    r"me frustra",
    r"no puedo",
    r"no logro",
    r"no sale",
]

BOREDOM_PATTERNS = [
    r"aburrido",
    r"esto es fácil",
    r"muy simple",
    r"no me interesa",
]

FLOW_PATTERNS = [
    r"creo que lo tengo",
    r"entiendo",
    r"esto tiene sentido",
    r"voy bien",
]

DOUBT_PATTERNS = [
    r"¿",
    r"\?",
    r"quizá",
    r"tal vez",
    r"no estoy seguro",
]

def classify_text(text: str) -> str:
    """
    Clasificador afectivo ligero basado en patrones.
    Devuelve: frustración, aburrimiento, duda, flujo o neutral.
    """

    t = text.lower()

    for p in FRUSTRATION_PATTERNS:
        if re.search(p, t):
            return "frustración"

    for p in BOREDOM_PATTERNS:
        if re.search(p, t):
            return "aburrimiento"

    for p in FLOW_PATTERNS:
        if re.search(p, t):
            return "flujo"

    for p in DOUBT_PATTERNS:
        if re.search(p, t):
            return "duda"

    return "neutral"
