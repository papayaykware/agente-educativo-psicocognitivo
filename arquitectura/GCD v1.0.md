# 🧠 Gemelo Cognitivo Dinámico (GCD v1.0)  
### Sistema Operativo Cognitivo del Alumno (SOCA)

---

## 🏷️ Badges

`https://img.shields.io/badge/Python-3.10+-blue`  
`https://img.shields.io/badge/Status-Active-success`  
`https://img.shields.io/badge/Architecture-GCD_v1.0-purple`  
`https://img.shields.io/badge/License-MIT-lightgrey`  
`https://img.shields.io/badge/DB-SQLite-green`

---

## 🧭 Índice Lateral (estilo GitBook)

- [Visión General](#visión-general)
- [Principio Fundamental](#principio-fundamental)
- [Arquitectura General](#arquitectura-general)
- [Modelo de Datos](#modelo-de-datos)
- [Variables Psicocognitivas](#variables-psicocognitivas)
- [Sistema de Evidencias](#sistema-de-evidencias)
- [Motor de Actualización](#motor-de-actualización)
- [Esquema SQLite](#esquema-sqlite)
- [Predictor de Riesgo](#predictor-de-riesgo)
- [Conexión con el Tutor](#conexión-con-el-tutor)
- [Preparación para TAE v2.0](#preparación-para-tae-v20)
- [Estructura del Repositorio](#estructura-del-repositorio)
- [Notebooks Reproducibles](#notebooks-reproducibles)
- [Referencias y DOI](#referencias-y-doi)
- [Siguientes Pasos](#siguientes-pasos)

---

# 📘 Visión General

El **Gemelo Cognitivo Dinámico (GCD v1.0)** es el **núcleo científico** del Agente Educativo Psicocognitivo.  
No es un chatbot.  
No es un tutor.  
Es un **Sistema Operativo Cognitivo del Alumno (SOCA)**.

> 💡 **Idea clave:**  
> El GCD no almacena respuestas, sino **estados evolutivos del aprendizaje**.

---

# 🔑 Principio Fundamental

El estado del alumno es una **función del tiempo**:

\[
Alumno(t) = Conocimiento + Atención + Motivación + Persistencia + Metacognición + Estilo\ Cognitivo + Historial
\]

Y por tanto:

\[
GCD(t+1) \neq GCD(t)
\]

El modelo **evoluciona continuamente**.

---

# 🏗️ Arquitectura General

```
┌──────────────────────┐
│ Interacción Alumno   │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Captura de Evidencias│
└──────────┬───────────┘
           │
           ▼
┌──────────────────────────┐
│ Cognitive Twin Engine    │
└──────────┬───────────────┘
           │
           ├────────► JSON
           │
           ├────────► SQLite
           │
           ▼
┌──────────────────────┐
│ Tutor Adaptativo     │
└──────────────────────┘
```

---

# 🧬 Modelo de Datos

### `student_profile.json`

```json
{
  "student_id": "001",

  "demographics": {
    "nombre": "Alumno",
    "edad": 32
  },

  "cognitive_state": {
    "comprension": 0.72,
    "retencion": 0.65,
    "atencion": 0.81,
    "motivacion": 0.88,
    "persistencia": 0.77,
    "metacognicion": 0.58
  },

  "learning_style": {
    "visual": 0.45,
    "textual": 0.82,
    "practico": 0.76,
    "reflexivo": 0.69
  },

  "risk_scores": {
    "abandono": 0.12,
    "frustracion": 0.18,
    "sobrecarga": 0.25
  },

  "last_update": "2026-06-15"
}
```

---

# 🧩 Variables Psicocognitivas

> ⚠️ **Solo 8 dimensiones.**  
> Más variables → menos robustez.

<details>
<summary><strong>Click para expandir las 8 dimensiones</strong></summary>

### 1. Comprensión  
Indicadores: aciertos, explicaciones, transferencia.

### 2. Retención  
Indicadores: recuerdo diferido, spaced repetition.

### 3. Atención  
Indicadores: latencia, interrupciones, cambios de contexto.

### 4. Motivación  
Indicadores: frecuencia, voluntariedad, profundidad.

### 5. Persistencia  
Indicadores: reintentos, revisiones voluntarias.

### 6. Metacognición  
Indicadores: autorreflexiones explícitas.

### 7. Flexibilidad Cognitiva  
Indicadores: cambio de estrategia, reformulación.

### 8. Creatividad Inferencial  
Indicadores: respuestas novedosas, asociaciones inesperadas.

</details>

---

# 📊 Sistema de Evidencias

| Variable | Evidencia |
|---------|-----------|
| Comprensión | % aciertos |
| Retención | recuerdo diferido |
| Atención | latencia |
| Motivación | frecuencia |
| Persistencia | reintentos |
| Metacognición | autorreflexiones |
| Flexibilidad | cambios de estrategia |
| Creatividad | excepciones detectadas |

---

# 🔄 Motor de Actualización

\[
nuevo = 0.8 \cdot actual + 0.2 \cdot evidencia
\]

- Estable  
- Suave  
- Evita oscilaciones  

---

# 🗄️ Esquema SQLite

### Tabla `students`

```sql
CREATE TABLE students (
  id INTEGER PRIMARY KEY,
  name TEXT,

  comprension REAL,
  retencion REAL,
  atencion REAL,
  motivacion REAL,
  persistencia REAL,
  metacognicion REAL,
  flexibilidad REAL,
  creatividad REAL,

  riesgo_abandono REAL,
  last_update TEXT
);
```

### Tabla `interactions`

```sql
CREATE TABLE interactions (
  id INTEGER PRIMARY KEY,
  student_id INTEGER,
  timestamp TEXT,
  input TEXT,
  response TEXT,
  score REAL,
  event_type TEXT
);
```

---

# 🚨 Predictor de Riesgo

\[
abandono = \frac{(1 - motivacion) + (1 - persistencia) + frustracion}{3}
\]

- **0.0 → bajo riesgo**  
- **1.0 → abandono inminente**

---

# 🤖 Conexión con el Tutor

Antes de generar respuesta:

```python
student_profile = load_profile(student_id)
```

El tutor recibe:

```json
{
  "comprension": 0.41,
  "motivacion": 0.83,
  "persistencia": 0.32
}
```

### Adaptación automática

- Comprensión baja → ejemplos + analogías  
- Metacognición alta → preguntas reflexivas  
- Persistencia baja → microobjetivos + refuerzo  

---

# 🧪 Preparación para TAE v2.0

```json
{
  "exception_events": [
    {
      "timestamp": "...",
      "concept": "algoritmos",
      "novelty_score": 0.91,
      "description": "respuesta inesperada"
    }
  ]
}
```

---

# 📁 Estructura del Repositorio

```
backend/
├── cognitive_twin/
│   ├── twin_engine.py
│   ├── metrics.py
│   ├── updater.py
│   ├── predictors.py
│   └── exceptions.py
├── database/
│   ├── sqlite_manager.py
│   └── schema.sql
├── tutor/
│   ├── prompt_builder.py
│   ├── adaptation.py
│   └── tutor_engine.py

data/
└── student_profiles/

tests/
docs/
```

---

# 🧪 Notebooks Reproducibles

- Notebook DKT  
- Affective Classifier  
- Cognitive Load

---

# 📚 Referencias y DOI

- Deep Knowledge Tracing — DOI: `10.48550/arXiv.1506.05908`  
- Affective Computing — DOI: `10.1145/382043.382336`  
- Cognitive Modeling in Education — DOI: `10.1007/978-3-319-93566-9_1`  

---
