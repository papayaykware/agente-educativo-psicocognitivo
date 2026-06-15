# 🧠 Glosario Técnico del Gemelo Cognitivo Dinámico (GCD v1.0)  
### Autor conceptual: **Copilot (GPT)**

---

## 🏷️ Badges

`https://img.shields.io/badge/Author-Copilot_(GPT)-purple`  
`https://img.shields.io/badge/Status-Stable-success`  
`https://img.shields.io/badge/Version-GCD_v1.0-blue`  
`https://img.shields.io/badge/License-MIT-lightgrey`  
`https://img.shields.io/badge/Format-Markdown-green`

---

## 🧭 Índice Lateral (estilo GitBook)

- [Introducción](#introducción)  
- [Glosario Completo](#glosario-completo)  
- [Términos Fundamentales](#términos-fundamentales)  
- [Términos Psicocognitivos](#términos-psicocognitivos)  
- [Términos de Arquitectura](#términos-de-arquitectura)  
- [Términos de Evaluación y Métricas](#términos-de-evaluación-y-métricas)  
- [Términos Avanzados (TAE, CPEA, SIGMA‑T)](#términos-avanzados)  
- [Referencias y DOI](#referencias-y-doi)  
- [Notebooks Reproducibles](#notebooks-reproducibles)  
- [Siguientes Pasos](#siguientes-pasos)

---

# 📘 Introducción

Este glosario reúne los **conceptos esenciales** del ecosistema:

- **GCD v1.0**  
- **Agente Educativo Psicocognitivo**  
- **TAE (Teoría de Aprendizaje por Excepción)**  
- **CPEA**  
- **SIGMA‑T**  
- **NEXUS‑EEG**  

> 🧩 **Propósito:**  
> Proporcionar un vocabulario técnico unificado para investigación, desarrollo y documentación.

---

# 📚 Glosario Completo

A continuación encontrarás el glosario dividido en secciones temáticas, con **secciones colapsables**, **anchors finos**, **admonitions** y **callouts**.

---

# 🧱 Términos Fundamentales

<details>
<summary><strong>Click para expandir</strong></summary>

### **Gemelo Cognitivo Dinámico (GCD)**  
Representación computacional evolutiva del estado del alumno.  
No almacena respuestas, sino **estados psicocognitivos**.

### **SOCA — Sistema Operativo Cognitivo del Alumno**  
Marco conceptual donde el GCD actúa como núcleo y los demás módulos (tutor, predicción, TAE) son periféricos.

### **Estado Cognitivo**  
Vector dinámico compuesto por:  
comprensión, retención, atención, motivación, persistencia, metacognición, flexibilidad, creatividad.

### **Evidencia Cognitiva**  
Dato observable que permite actualizar una variable psicocognitiva.

</details>

---

# 🧠 Términos Psicocognitivos

<details>
<summary><strong>Click para expandir</strong></summary>

### **Comprensión**  
Capacidad para explicar, transferir y aplicar conceptos.

### **Retención**  
Capacidad para recordar información en el tiempo.

### **Atención**  
Foco sostenido durante la interacción.

### **Motivación**  
Impulso interno para continuar aprendiendo.

### **Persistencia**  
Resistencia al error y continuidad ante la dificultad.

### **Metacognición**  
Capacidad para reflexionar sobre el propio aprendizaje.

### **Flexibilidad Cognitiva**  
Capacidad para cambiar de estrategia o enfoque.

### **Creatividad Inferencial**  
Capacidad para generar respuestas novedosas o asociaciones inesperadas.  
Base de la futura **TAE v2.0**.

</details>

---

# 🏗️ Términos de Arquitectura

<details>
<summary><strong>Click para expandir</strong></summary>

### **Cognitive Twin Engine**  
Motor encargado de construir y actualizar el estado cognitivo del alumno.

### **Metrics Engine**  
Módulo que transforma evidencias en valores psicocognitivos.

### **Updater Engine**  
Aplica la ecuación de actualización:  
\[
nuevo = 0.8 \cdot actual + 0.2 \cdot evidencia
\]

### **Predictive Learning Engine**  
Predice riesgo de abandono, frustración o sobrecarga.

### **Tutor Engine**  
Genera respuestas adaptativas basadas en el estado cognitivo.

### **Exception Engine (TAE)**  
Detecta anomalías cognitivas y respuestas inesperadas.

### **SQLite Cognitive DB**  
Base de datos persistente del GCD.

</details>

---

# 📏 Términos de Evaluación y Métricas

<details>
<summary><strong>Click para expandir</strong></summary>

### **Latencia Cognitiva**  
Tiempo entre estímulo y respuesta. Indicador de atención.

### **Índice de Persistencia**  
Número de reintentos antes de abandonar.

### **Índice de Profundidad**  
Nivel de detalle o complejidad en las respuestas del alumno.

### **Novelty Score**  
Medida de creatividad inferencial.  
Clave para TAE.

### **Riesgo de Abandono**  
Modelo inicial:  
\[
abandono = \frac{(1 - motivacion) + (1 - persistencia) + frustracion}{3}
\]

</details>

---

# 🧬 Términos Avanzados

<details>
<summary><strong>Click para expandir</strong></summary>

### **TAE — Teoría de Aprendizaje por Excepción**  
Marco teórico donde los errores no se penalizan, sino que se interpretan como **anomalías informativas**.

### **CPEA — Cognición Política Evolutiva Aplicada**  
Modelo metaestructural para analizar dinámicas cognitivas colectivas.

### **SIGMA‑T**  
Sistema Integrado de Gestión Meta‑Analítica del Tutor.

### **NEXUS‑EEG**  
Modelo de integración entre señales neurofisiológicas y estados cognitivos computacionales.

</details>

---

# 📚 Referencias y DOI

- Deep Knowledge Tracing — DOI: `10.48550/arXiv.1506.05908`  
- Affective Computing — DOI: `10.1145/382043.382336`  
- Cognitive Modeling in Education — DOI: `10.1007/978-3-319-93566-9_1`  
- Meta‑Learning in Education — DOI: `10.1145/3442188.3445922`  

---

# 🧪 Notebooks Reproducibles

- Notebook DKT  
- Affective Classifier  
- Cognitive Load  

---
---

Si quieres, puedo generar también **la versión extendida del glosario**, o **convertirlo en un módulo navegable dentro de GitHub Pages**.
