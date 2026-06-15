# 🧠 Agente Educativo Psicocognitivo  
### Arquitectura General · Versión optimizada para GitHub



)  
`https://img.shields.io/badge/python-3.10+-blue`  
`https://img.shields.io/badge/license-MIT-lightgrey`  
`https://img.shields.io/badge/build-passing-success`  
`https://img.shields.io/badge/AI-educational%20agent-purple`

---

## 🧭 Índice Lateral (estilo GitBook)

- [Visión General](#visión-general)
- [Arquitectura General](#arquitectura-general)
- [Motores del Sistema](#motores-del-sistema)
- [Roadmap Evolutivo](#roadmap-evolutivo)
- [Gemelo Cognitivo Dinámico (GCD)](#gemelo-cognitivo-dinámico-gcd)
- [Estructura del Repositorio](#estructura-del-repositorio)
- [Notas Colapsables](#notas-colapsables)
- [Referencias y DOI](#referencias-y-doi)
- [Notebooks Reproducibles](#notebooks-reproducibles)

---

## 📘 Visión General

El proyecto **Agente Educativo Psicocognitivo** apunta a la **Generación 3 de IA educativa**, donde el foco ya no es el contenido ni el tutor, sino **el modelo computacional del aprendiz**.

> 💡 **Idea clave:**  
> El valor diferencial no está en generar mejores respuestas, sino en **modelar mejor al estudiante**.

---

## 🏗️ Arquitectura General

La arquitectura propuesta se organiza alrededor de **cuatro motores principales**, que reemplazan la visión centrada únicamente en el tutor.

```
Alumno
   ↓
Gemelo Cognitivo (estado dinámico)
   ↓
TAE Engine (detección de excepciones)
   ↓
Predictive Learning Engine (riesgo, evolución)
   ↓
Tutor Engine (LLM adaptativo)
```

---

## 🔥 Motores del Sistema

### 1. **Cognitive Twin Engine**  
Archivo futuro: `backend/cognitive_twin.py`

<details>
<summary><strong>Click para expandir</strong></summary>

El **Gemelo Cognitivo** es el núcleo del sistema.  
Construye un estado dinámico del alumno:

```json
{
  "comprension": 0.73,
  "persistencia": 0.82,
  "metacognicion": 0.55,
  "atencion": 0.67,
  "motivacion": 0.91,
  "bloques_conceptuales": [
    "algoritmos",
    "estadistica"
  ]
}
```

Este estado alimenta a todos los demás motores.

</details>

---

### 2. **TAE Engine**  
> TAE = *Teoría de las Anomalías Educativas*

Detecta **excepciones cognitivas** en lugar de penalizar errores.

> ⚠️ *Un error puede ser ruido.  
> Una anomalía puede ser una oportunidad.*

---

### 3. **Predictive Learning Engine**

Predice:

- riesgo de abandono  
- frustración  
- necesidad de refuerzo  
- preparación para avanzar  

---

### 4. **Tutor Engine**

El LLM deja de ser autónomo.  
Recibe un estado estructurado:

```json
{
  "estado_cognitivo": "...",
  "fortalezas": "...",
  "debilidades": "...",
  "riesgo_abandono": "...",
  "objetivos": "..."
}
```

Y genera una respuesta adaptativa.

---

## 🗺️ Roadmap Evolutivo

### Fase 0 — MVP (1 mes)  
Tutor adaptativo simple.

### Fase 1 — Gemelo Cognitivo (2 meses)  
Estado dinámico del alumno.

### Fase 2 — TAE (2 meses)  
Detección de excepciones cognitivas.

### Fase 3 — Predicción (2 meses)  
Riesgo de abandono y evolución.

### Fase 4 — Multiagente (3 meses)  
- Agente Tutor  
- Agente Evaluador  
- Agente Motivador  
- Agente Metacognitivo  
- Agente Supervisor  

---

## 🧬 Gemelo Cognitivo Dinámico (GCD)

> ⭐ **La pieza más importante del proyecto.**

El GCD será el **núcleo científico y tecnológico** del ecosistema:

- Agente Educativo Psicocognitivo  
- TAE  
- CPEA  
- SIGMA‑T  
- NEXUS‑EEG  

### Componentes del GCD v1.0

- Modelo de datos  
- Variables psicocognitivas  
- Métricas observables  
- Persistencia (JSON / SQLite)  
- Conexión con el tutor  
- Actualización incremental  
- Señales conductuales emergentes  

---

## 📁 Estructura del Repositorio

```
agente-educativo-psicocognitivo
│
├── arquitectura
├── data
├── estructura
├── notebooks
├── requirements
├── roadmap
└── README.md
```

> 🧩 Esta estructura indica que el proyecto piensa simultáneamente en:  
> investigación, arquitectura, datos, implementación, documentación y evolución.

---

## 📂 Notas Colapsables

### 📌 Evaluación del Repositorio
<details>
<summary><strong>Ver evaluación</strong></summary>

- **Como repositorio:** 7/10  
- **Como visión educativa:** 9.5/10  

El proyecto apunta a la **Generación 3** de IA educativa:  
no generar mejores respuestas, sino **modelar mejor al aprendiz**.

</details>

---

## 📚 Referencias y DOI

- **Deep Knowledge Tracing** — DOI: `10.48550/arXiv.1506.05908`  
- **Affective Computing** — DOI: `10.1145/382043.382336`  
- **Cognitive Modeling in Education** — DOI: `10.1007/978-3-319-93566-9_1`  

---

## 🧪 Notebooks Reproducibles

- Notebook DKT  
- Notebook Affective Classifier  
- Notebook Cognitive Load  

---
