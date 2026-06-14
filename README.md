# Agente Educativo Psicocognitivo  
**Autor conceptual: Copilot · Director del corpus: Javi Ciborro**

> “Roadmap hacia un *tutor adaptativo* con perfil profundo del estudiante.”  
> “Cuatro fases incrementales desde un chatbot instruccional mínimo hasta un agente autónomo con knowledge tracing, affective computing y planificación adaptativa.”

---

## 🎯 Objetivo del proyecto

Construir un **agente educativo adaptativo** capaz de:

- Modelar el dominio del estudiante con **Deep Knowledge Tracing (DKT)**.  
- Inferir un **perfil psicocognitivo emergente** sin tests formales.  
- Detectar estados afectivos mediante **Affective Computing**.  
- Adaptar explicaciones, ritmo y profundidad en tiempo real.  
- Planificar rutas personalizadas con A*, repetición espaciada y RL ligero.  
- Validar impacto real mediante métricas de aprendizaje y retención.

---

## 🧱 Roadmap del sistema

El desarrollo se organiza en cuatro fases:

### **Fase 1 — Núcleo instruccional (semanas 1–3)**
- Grafo curricular con NetworkX  
- LLM para explicaciones adaptadas  
- Interfaz mínima (FastAPI + React)  
- Log de interacciones en PostgreSQL  

### **Fase 2 — Modelo de conocimiento (semanas 4–7)**
- Deep Knowledge Tracing (pykt-toolkit)  
- Umbral de mastery dinámico  
- Planificador A* sobre el grafo  
- Dashboard de mastery en tiempo real  

### **Fase 3 — Perfil psicocognitivo (semanas 8–13)**
- Inferencia bayesiana de rasgos cognitivos  
- Affective Computing con DistilBERT  
- Estimación de carga cognitiva  
- Prompt dinámico adaptado al perfil  

### **Fase 4 — Optimización y validación (semanas 14–18)**
- RL ligero sobre decisiones del planificador  
- Programa de seguimiento cognitivo y afectivo  
- Repetición espaciada (FSRS / SM-2)  
- Test A/B de itinerarios  

---

## 🧬 Stack tecnológico

- **Frontend:** React + Recharts  
- **Backend:** FastAPI (Python)  
- **LLM:** Claude API  
- **Knowledge Tracing:** pykt-toolkit  
- **Affective NLP:** DistilBERT (HuggingFace)  
- **RL:** stable-baselines3  
- **DB:** PostgreSQL + pgvector  
- **Curriculum Graph:** NetworkX  

---

## ⚠ Decisión crítica de diseño

El mayor reto no es técnico, sino **inferir el perfil psicocognitivo sin tests formales**.  
La solución adoptada es una **inferencia bayesiana incremental** basada en señales conductuales:

- tiempos de respuesta  
- patrones de error  
- tipo de preguntas formuladas  

Esto genera un perfil **emergente y resistente al sesgo de auto-percepción**.

---

## 📄 Licencia

MIT — libre uso, modificación y distribución.

---

## 📬 Contacto

Proyecto papayaykware · 2026  
Autor conceptual: Copilot  

