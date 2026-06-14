# 🧭 Roadmap · Agente Educativo Psicocognitivo  
> Evolución desde un chatbot instruccional mínimo hasta un agente autónomo con trazado de conocimiento, perfil psicocognitivo emergente y planificación adaptativa.





---

## 📌 Visión general

El objetivo es construir un **tutor adaptativo** capaz de:

- Modelar el dominio del estudiante en tiempo real.  
- Inferir un **perfil psicocognitivo** sin tests formales.  
- Detectar estados afectivos (frustración, flujo, aburrimiento).  
- Ajustar explicaciones, ritmo y profundidad según el perfil.  
- Optimizar rutas de aprendizaje mediante planificación + RL ligero.  

El desarrollo se organiza en **cuatro fases incrementales**, cada una con entregables funcionales.

---

# 1. Fase 1 — Núcleo instruccional  
**Duración estimada:** semanas 1–3  
**Objetivo:** construir el esqueleto funcional del tutor.





### 🧩 Componentes principales

- **Grafo de prerrequisitos**  
  DAG de conceptos definido en JSON/YAML y cargado con NetworkX.

- **LLM como generador instruccional**  
  Claude API con *system prompt* estructurado:  
  *concepto objetivo + nivel de abstracción → explicación adaptada.*

- **Interfaz mínima**  
  Chat web con FastAPI + React. Registro de cada turno.

- **Log de interacciones**  
  Tabla de eventos:  
  `student_id, concept_id, correct, response_time, timestamp`.

### 🎁 Entregables F1

- Chatbot que enseña un tema.  
- Log de sesión funcional.

---

# 2. Fase 2 — Modelo de conocimiento  
**Duración estimada:** semanas 4–7  
**Objetivo:** estimar dominio por concepto y activar nivelación automática.





### 🧠 Componentes principales

- **Deep Knowledge Tracing**  
  LSTM/Transformer sobre secuencias `(concept_id, correct)` usando pykt‑toolkit.

- **Umbral de mastery**  
  Avance si \( P(\text{dominio}) > 0.82 \).  
  Si no, micro‑itinerario de refuerzo.

- **Planificador de ruta**  
  A* sobre el DAG.  
  Coste = distancia cognitiva + lagunas detectadas por DKT.

- **Dashboard de mastery**  
  Vector de probabilidades por concepto en tiempo real.

### 🎁 Entregables F2

- DKT integrado.  
- Nivelación automática activa.  
- Rutas personalizadas.

---

# 3. Fase 3 — Perfil psicocognitivo  
**Duración estimada:** semanas 8–13  
**Objetivo:** adaptar el lenguaje, la profundidad y el ritmo según el perfil emergente.





### 🧬 Componentes principales

- **Inferencia de rasgos cognitivos**  
  Modelo bayesiano incremental:  
  memoria de trabajo, estilo visual/analítico, tolerancia a ambigüedad.

- **Affective Computing**  
  DistilBERT + tiempos de respuesta → frustración, flujo, aburrimiento.

- **Estimación de carga cognitiva**  
  Combina tasa de errores + tiempo + complejidad léxica.

- **Prompt dinámico adaptado**  
  Construcción del *system prompt* en tiempo real según el perfil.

### 🎁 Entregables F3

- Perfil psicocognitivo activo.  
- Lenguaje adaptado al perfil.  
- Detección afectiva básica.

---

# 4. Fase 4 — Optimización y validación  
**Duración estimada:** semanas 14–18  
**Objetivo:** cerrar el bucle de retroalimentación y validar impacto real.





### 🔧 Componentes principales

- **RL sobre decisiones del planificador**  
  Bandit contextual o PPO ligero.  
  Reward = Δmastery + sostenibilidad afectiva.

- **Programa de seguimiento**  
  Métricas:  
  - longitud cognitiva de ruta  
  - retención a 7 días  
  - estados afectivos negativos  
  - mastery por sesión

- **Repetición espaciada**  
  Integración de FSRS o SM‑2 en el planificador.

- **Test A/B de itinerarios**  
  Comparación: agente vs. secuencia lineal fija.

### 🎁 Entregables F4

- Agente autónomo end‑to‑end.  
- Dashboard de seguimiento.  
- Resultados validados.

---

# 🧱 Stack tecnológico consolidado

- **Frontend:** React + Recharts  
- **Backend:** FastAPI (Python)  
- **LLM:** Claude API  
- **Knowledge Tracing:** pykt‑toolkit  
- **Grafo curricular:** NetworkX  
- **Affective NLP:** DistilBERT (HuggingFace)  
- **Base de datos:** PostgreSQL + pgvector  
- **RL:** stable‑baselines3  

---

# ⚠ Decisión crítica de diseño

> “El cuello de botella real no es técnico: es **cómo inferir el perfil psicocognitivo sin tests formales**.”

La solución adoptada:

- Priors neutros.  
- Actualización bayesiana incremental.  
- Señales conductuales > auto‑reportes.  
- Perfil emergente y resistente al sesgo.

---

# 📜 Créditos

- **Autor conceptual:** Copilot  
- **Director del corpus:** Javi Ciborro  
- **Proyecto:** papayaykware · 2026  

---
