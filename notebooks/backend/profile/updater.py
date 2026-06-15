"""
updater.py — Actualización del perfil psicocognitivo emergente
Autor conceptual: Copilot
"""

from typing import Dict
from .inference import infer_profile_from_interaction

def update_profile(old_profile: Dict[str, float] | None, interaction: Dict) -> Dict[str, float]:
    """
    Actualiza el perfil psicocognitivo combinando:
    - perfil previo (prior)
    - inferencia de la nueva interacción (likelihood)
    """

    new = infer_profile_from_interaction(interaction)

    if old_profile is None:
        return new

    updated = {}
    alpha = 0.7  # peso del historial
    beta = 0.3   # peso de la nueva evidencia

    for key in new:
        updated[key] = alpha * old_profile.get(key, 0.5) + beta * new[key]

    return updated
