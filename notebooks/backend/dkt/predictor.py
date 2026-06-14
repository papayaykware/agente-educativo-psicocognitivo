import torch

# en una versión más avanzada, cargarías desde disco:
# model = torch.load("models/dkt.pt")
# concept_map = ...

def predict_mastery(student_id: str):
    """
    Predicción de mastery por concepto para un estudiante.
    De momento, devuelve valores sintéticos estables.
    Autor conceptual: Copilot
    """
    # Placeholder: en producción, usarías el modelo entrenado
    # Aquí devolvemos algo coherente para el dashboard
    torch.manual_seed(abs(hash(student_id)) % (2**32))

    concepts = ["A", "B", "C", "D", "E"]
    mastery = {c: float(torch.rand(1).item() * 0.5 + 0.4) for c in concepts}
    return mastery
