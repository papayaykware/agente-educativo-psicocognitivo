# 🧪 GCD Experimental Validation v0.1

<div align="center">

![Status](https://img.shields.io/badge/Status-Draft-yellow?style=for-the-badge)
![Milestone](https://img.shields.io/badge/Milestone-Validation%20v0.1-blue?style=for-the-badge)
![Date](https://img.shields.io/badge/Date-2026--01--19-green?style=for-the-badge)

</div>

---

<details open>
<summary><b>📚 Tabla de Contenidos</b></summary>
<br>

- [1. Propósito y Alcance](#1-propósito-y-alcance)
- [2. Hipótesis de Validación](#2-hipótesis-de-validación)
  - [GCD-001: Efecto Adaptativo en Progresión de Aprendizaje](#gcd-001-efecto-adaptativo-en-progresión-de-aprendizaje)
  - [GCD-002: Persistencia como Predictor de Abandono](#gcd-002-persistencia-como-predictor-de-abandono)
  - [GCD-003: Metacognición y Consolidación Conceptual](#gcd-003-metacognición-y-consolidación-conceptual)
  - [GCD-004: Flexibilidad Cognitiva y Transferencia](#gcd-004-flexibilidad-cognitiva-y-transferencia)
- [3. Variables y Operacionalización](#3-variables-y-operacionalización)
- [4. Métricas y Criterios de Éxito](#4-métricas-y-criterios-de-éxito)
- [5. Protocolos Experimentales](#5-protocolos-experimentales)
- [6. Criterios de Falsación](#6-criterios-de-falsación)
- [7. Plan de Análisis](#7-plan-de-análisis)
- [8. Cronograma y Entregables](#8-cronograma-y-entregables)
- [9. Referencias](#9-referencias)

</details>

---

## 1. Propósito y Alcance

### Pregunta Central

> **¿Las variables psicocognitivas del GCD tienen capacidad predictiva?**

Esta pregunta es el eje de este hito. La respuesta determinará si el modelo GCD tiene valor científico o si necesita una revisión fundamental.

### Contexto

El sistema GCD (General Cognitive Dynamics) propone un modelo de tutoría adaptativa basado en variables psicocognitivas: **atención, motivación, persistencia, metacognición, flexibilidad cognitiva y excepciones cognitivas**. Hasta ahora, el sistema ha sido capaz de *describir* estas variables y *generar* adaptaciones. Sin embargo, su verdadero valor científico radica en su **capacidad predictiva**: ¿puede el GCD predecir resultados de aprendizaje a partir de estas variables?

### Objetivos

1. **Validar** la capacidad predictiva de las variables psicocognitivas del GCD.
2. **Establecer** criterios de éxito y falsación para cada hipótesis.
3. **Generar** evidencia empírica que justifique la continuación (o revisión) del desarrollo del GCD.

### Alcance

Este hito se centra exclusivamente en la **validación experimental** del GCD v1.0. No se desarrollarán nuevas funcionalidades; el foco está en **medir, analizar y concluir**.

---

## 2. Hipótesis de Validación

### GCD-001: Efecto Adaptativo en Progresión de Aprendizaje

| Aspecto | Descripción |
|---------|-------------|
| **Hipótesis** | La adaptación basada en GCD mejora la progresión de aprendizaje frente a un tutor estático. |
| **Variable Independiente** | Tipo de tutor: **GCD Adaptativo** vs **Control Estático**. |
| **Variable Dependiente** | **Progresión de aprendizaje**: pendiente de la curva de conocimiento (velocidad de aprendizaje). |
| **Métrica Principal** | Coeficiente `b` del modelo exponencial `knowledge = a * (1 - exp(-b * session))`. |
| **Criterio de Éxito** | Diferencia significativa (p < 0.05) entre grupos en `b`, con un tamaño del efecto ≥ 0.40 (Cohen's d). |
| **Criterio de Falsación** | Si p ≥ 0.05 o d < 0.20, la hipótesis se considera falsada. |

---

### GCD-002: Persistencia como Predictor de Abandono

| Aspecto | Descripción |
|---------|-------------|
| **Hipótesis** | La persistencia predice mejor el abandono que el rendimiento académico. |
| **Variable Independiente** | **Persistencia**: ratio `(tiempo_total / sesiones_activas) / intentos_fallidos`. **Rendimiento**: promedio de calificaciones. |
| **Variable Dependiente** | **Abandono**: binario (completa vs abandona). |
| **Métrica Principal** | Odds Ratio (OR) ajustado por otras covariables (atención, motivación). |
| **Criterio de Éxito** | OR de persistencia ≥ 1.5 y significativo (p < 0.05), y OR de persistencia > OR de rendimiento en un modelo multivariante. |
| **Criterio de Falsación** | Si OR de persistencia no es significativo, o si OR de rendimiento > OR de persistencia. |

---

### GCD-003: Metacognición y Consolidación Conceptual

| Aspecto | Descripción |
|---------|-------------|
| **Hipótesis** | La metacognición acelera la consolidación conceptual. |
| **Variable Independiente** | **Metacognición**: puntuación en el cuestionario MAI (Metacognitive Awareness Inventory). |
| **Variable Dependiente** | **Consolidación conceptual**: retención a 30 días (diferencia entre post-test y retención a 30 días). |
| **Métrica Principal** | Correlación de Pearson entre metacognición y consolidación. |
| **Criterio de Éxito** | Correlación positiva significativa (r ≥ 0.30, p < 0.05). |
| **Criterio de Falsación** | Si r < 0.20 o p ≥ 0.05. |

---

### GCD-004: Flexibilidad Cognitiva y Transferencia

| Aspecto | Descripción |
|---------|-------------|
| **Hipótesis** | La flexibilidad cognitiva mejora la transferencia de conocimiento. |
| **Variable Independiente** | **Flexibilidad cognitiva**: medida mediante una tarea de cambio de set (ej. Wisconsin Card Sorting Test adaptado). |
| **Variable Dependiente** | **Transferencia**: puntuación en problemas análogos no vistos (nuevos contextos). |
| **Métrica Principal** | Correlación entre flexibilidad cognitiva y transferencia. |
| **Criterio de Éxito** | Correlación positiva significativa (r ≥ 0.25, p < 0.05). |
| **Criterio de Falsación** | Si r < 0.15 o p ≥ 0.05. |

---

## 3. Variables y Operacionalización

### Variables Independientes

| Variable | Operacionalización | Instrumento | Escala |
|----------|---------------------|-------------|--------|
| **Tipo de tutor** | GCD vs Control | Asignación aleatoria | Categórica |
| **Persistencia** | `(tiempo_total / sesiones_activas) / intentos_fallidos` | Logs del sistema | 0–1 |
| **Rendimiento** | Media de calificaciones en pruebas sumativas | Tests semanales | 0–10 |
| **Metacognición** | Puntuación total en MAI | Cuestionario MAI | 0–100 |
| **Flexibilidad cognitiva** | Número de errores perseverativos en WCST | WCST adaptado | Entero |

### Variables Dependientes

| Variable | Operacionalización | Instrumento | Escala |
|----------|---------------------|-------------|--------|
| **Progresión** | Coeficiente `b` de curva de aprendizaje | Modelo exponencial | 0–5 |
| **Abandono** | Completa (0) vs Abandona (1) | Registro de asistencia | Binaria |
| **Consolidación** | `retención_30d - post_test` | Tests de seguimiento | 0–1 |
| **Transferencia** | % de aciertos en problemas análogos | Test de transferencia | 0–1 |

### Variables de Control

- Edad (años)
- Nivel educativo (categorías)
- Motivación inicial (escala Likert)
- Conocimiento previo (pre-test)

---

## 4. Métricas y Criterios de Éxito

### Métricas Primarias

| Hipótesis | Métrica | Umbral de Éxito |
|-----------|---------|-----------------|
| GCD-001 | Cohen's d (progresión) | d ≥ 0.40 |
| GCD-002 | Odds Ratio (persistencia) | OR ≥ 1.5, p < 0.05 |
| GCD-003 | Correlación Pearson | r ≥ 0.30, p < 0.05 |
| GCD-004 | Correlación Pearson | r ≥ 0.25, p < 0.05 |

### Métricas Secundarias

- **Tamaño del efecto** (Cohen's d, η², V de Cramer).
- **Intervalos de confianza** al 95%.
- **AUC** de modelos predictivos (para abandono).
- **R²** para modelos de regresión.

### Criterios de Éxito Global

Para considerar que el GCD tiene valor predictivo, se deben cumplir **al menos 3 de las 4** hipótesis. Si solo 2 o menos son exitosas, el modelo se considera no validado y se necesita revisión.

---

## 5. Protocolos Experimentales

### 5.1. Diseño

- **Tipo**: Ensayo controlado aleatorizado (ECA), con asignación 1:1.
- **Cegamiento**: Evaluadores ciegos al grupo.
- **Duración**: 8 semanas de intervención + seguimiento a 30 días.

### 5.2. Participantes

- **N**: 120 (60 por grupo).
- **Edad**: 18–35 años.
- **Nivel educativo**: Universitario o superior.
- **Criterios de exclusión**: Trastornos cognitivos, participación en otros estudios.

### 5.3. Instrumentos

- **MAI** (Metacognitive Awareness Inventory) – Schraw & Dennison (1994).
- **WCST** (Wisconsin Card Sorting Test) – adaptado para entorno digital.
- **Pruebas de conocimiento**: diseñadas por expertos.
- **Test de transferencia**: problemas análogos no vistos.
- **Sistema GCD**: registra logs de interacción.

### 5.4. Procedimiento

1. **Screening** (semana -1): verificar criterios de inclusión.
2. **Pre-test** (semana 0): MAI, WCST, conocimiento previo.
3. **Intervención** (semanas 1–8): 2 sesiones semanales de 90 min.
4. **Post-test** (semana 9): conocimiento, transferencia.
5. **Seguimiento** (semana 13): retención a 30 días.

### 5.5. Análisis Planificado

- **GCD-001**: ANOVA mixto (grupo × tiempo) para progresión.
- **GCD-002**: Regresión logística (persistencia, rendimiento, covariables).
- **GCD-003**: Correlación de Pearson (metacognición, consolidación).
- **GCD-004**: Correlación de Pearson (flexibilidad, transferencia).

Todos los análisis ajustarán por covariables (edad, nivel educativo, conocimiento previo) mediante ANCOVA o regresión múltiple.

---

## 6. Criterios de Falsación

### Falsación de GCD-001

- **Condición**: No se encuentra diferencia significativa entre GCD y Control en velocidad de aprendizaje (p ≥ 0.05).
- **Interpretación**: La adaptación basada en GCD no mejora la progresión. Se debe revisar el mecanismo de adaptación.

### Falsación de GCD-002

- **Condición**: La persistencia no es un predictor significativo de abandono (p ≥ 0.05), o el rendimiento predice mejor (OR_rendimiento > OR_persistencia).
- **Interpretación**: La persistencia no es la variable clave para el abandono. Se debe explorar otras variables.

### Falsación de GCD-003

- **Condición**: No hay correlación significativa entre metacognición y consolidación (r < 0.20, p ≥ 0.05).
- **Interpretación**: La metacognición no acelera la consolidación; se debe reconsiderar el rol de esta variable.

### Falsación de GCD-004

- **Condición**: No hay correlación significativa entre flexibilidad cognitiva y transferencia (r < 0.15, p ≥ 0.05).
- **Interpretación**: La flexibilidad cognitiva no mejora la transferencia; el modelo GCD debe incluir otros mecanismos.

### Falsación Global

Si **2 o más** hipótesis son falsadas, el modelo GCD v1.0 no se considera validado y se requiere un rediseño.

---

## 7. Plan de Análisis

### 7.1. Software

- **R** v4.3 (tidyverse, lme4, survival, brms)
- **Python** v3.10 (pandas, statsmodels, scikit-learn)
- **Jupyter Notebooks** para reproducibilidad

### 7.2. Análisis por Hipótesis

| Hipótesis | Prueba | Covariables | Tamaño del Efecto |
|-----------|--------|-------------|-------------------|
| GCD-001 | ANOVA mixto | Edad, pre-test | Cohen's d, η² |
| GCD-002 | Regresión logística | Atención, motivación | OR, AUC |
| GCD-003 | Correlación parcial | Edad, nivel educativo | r (Pearson) |
| GCD-004 | Correlación parcial | Edad, nivel educativo | r (Pearson) |

### 7.3. Análisis de Sensibilidad

- **Bootstrapping**: 5000 iteraciones para intervalos de confianza robustos.
- **Imputación de datos faltantes**: MICE (Multiple Imputation by Chained Equations).
- **Análisis por intención de tratar** (ITT).

---

## 8. Cronograma y Entregables

### Cronograma (Estimado)

| Fase | Duración | Fechas |
|------|----------|--------|
| Pre-registro (OSF) | 1 semana | 20–27 Ene 2026 |
| Reclutamiento | 3 semanas | 27 Ene – 17 Feb |
| Pre-test | 1 semana | 17–24 Feb |
| Intervención | 8 semanas | 24 Feb – 20 Abr |
| Post-test | 1 semana | 20–27 Abr |
| Seguimiento (30d) | 1 semana | 27 May |
| Análisis | 4 semanas | Jun 2026 |

### Entregables

1. **Pre-registro** en OSF (DOI).
2. **Datos anonimizados** en formato CSV.
3. **Scripts de análisis** (R y Python) en el repositorio.
4. **Informe de resultados** (HTML + PDF) con conclusiones.
5. **Borrador de artículo** para publicación.

---

## 9. Referencias

1. Schraw, G., & Dennison, R. S. (1994). Assessing metacognitive awareness. *Contemporary Educational Psychology*, 19(4), 460-475.
2. Heaton, R. K. (1981). *Wisconsin Card Sorting Test manual*. Psychological Assessment Resources.
3. Cohen, J. (1988). *Statistical Power Analysis for the Behavioral Sciences* (2nd ed.). LEA.
4. VanLehn, K. (2011). The relative effectiveness of human tutoring, intelligent tutoring systems, and other tutoring systems. *Educational Psychologist*, 46(4), 197-221.
5. Pintrich, P. R. (2000). The role of metacognition in self-regulated learning. *Issues in Education*, 6(1-2), 107-114.

---

<div align="center">

**[⬆ Volver Arriba](#-gcd-experimental-validation-v01)**

---

*Última actualización: 19 Enero 2026*  
*Versión: 0.1.0*  
*Estado: Borrador para Revisión*

</div>
