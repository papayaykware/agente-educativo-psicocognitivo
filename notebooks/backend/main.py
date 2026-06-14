from fastapi import FastAPI
from api.routes_students import router as students_router
from api.routes_curriculum import router as curriculum_router
from api.routes_dkt import router as dkt_router
from api.routes_affective import router as affective_router
from api.routes_tutor import router as tutor_router
app.include_router(tutor_router, prefix="/tutor")


app = FastAPI(title="Agente Educativo Psicocognitivo")

app.include_router(students_router, prefix="/students")
app.include_router(curriculum_router, prefix="/curriculum")
app.include_router(dkt_router, prefix="/dkt")
app.include_router(affective_router, prefix="/affective")

@app.get("/")
def root():
    return {"status": "ok", "message": "Agente Educativo Psicocognitivo activo"}
