# 🧪 Experimental Framework v1.0

<div align="center">

![Status](https://img.shields.io/badge/Status-Draft-yellow?style=for-the-badge)
![Version](https://img.shields.io/badge/Version-1.0.0-blue?style=for-the-badge)
![DOI](https://img.shields.io/badge/DOI-Pending-orange?style=for-the-badge)
[![OSF](https://img.shields.io/badge/OSF-Registration-0066cc?style=for-the-badge&logo=osf)](https://osf.io)

</div>

---

<details open>
<summary><b>📚 Tabla de Contenidos</b></summary>
<br>

- [1. Propósito y Alcance](#1-propósito-y-alcance)
- [2. Hipótesis de Investigación](#2-hipótesis-de-investigación)
  - [H1: Efecto del Tutor Adaptativo GCD](#h1-efecto-del-tutor-adaptativo-gcd)
  - [H2: Predictores de Abandono](#h2-predictores-de-abandono)
  - [H3: Aceleración Metacognitiva](#h3-aceleración-metacognitiva)
  - [H4: Excepciones Cognitivas y Creatividad](#h4-excepciones-cognitivas-y-creatividad)
- [3. Diseño Experimental](#3-diseño-experimental)
  - [3.1. Tipo de Diseño](#31-tipo-de-diseño)
  - [3.2. Asignación y Cegamiento](#32-asignación-y-cegamiento)
  - [3.3. Condiciones Experimentales](#33-condiciones-experimentales)
  - [3.4. Poder Estadístico y Tamaño Muestral](#34-poder-estadístico-y-tamaño-muestral)
- [4. Procedimiento](#4-procedimiento)
  - [4.1. Reclutamiento y Screening](#41-reclutamiento-y-screening)
  - [4.2. Pre-test](#42-pre-test)
  - [4.3. Intervención](#43-intervención)
  - [4.4. Post-test y Seguimiento](#44-post-test-y-seguimiento)
- [5. Métricas y Variables](#5-métricas-y-variables)
  - [5.1. Variables Primarias](#51-variables-primarias)
  - [5.2. Variables Secundarias y de Proceso](#52-variables-secundarias-y-de-proceso)
- [6. Plan de Análisis Estadístico](#6-plan-de-análisis-estadístico)
  - [6.1. Análisis por Hipótesis](#61-análisis-por-hipótesis)
  - [6.2. Ajustes por Comparaciones Múltiples](#62-ajustes-por-comparaciones-múltiples)
  - [6.3. Software y Reproducibilidad](#63-software-y-reproducibilidad)
- [7. Consideraciones Éticas](#7-consideraciones-éticas)
- [8. Cronograma](#8-cronograma)
- [9. Referencias](#9-referencias)
- [10. Anexos](#10-anexos)

</details>

---

## 1. Propósito y Alcance

Este documento establece el **marco experimental** para la validación del sistema **GCD (General Cognitive Dynamics)** como herramienta educativa adaptativa. El objetivo es someter a prueba empírica las hipótesis que fundamentan el diseño del sistema, mediante un experimento controlado, aleatorizado y reproducible.

El alcance incluye la definición de:

- Hipótesis con variables operacionalizadas y efectos esperados.
- Diseño experimental, condiciones, y tamaño muestral.
- Procedimiento detallado de reclutamiento, intervención y evaluación.
- Métricas primarias y secundarias, con instrumentos de medición.
- Plan de análisis estadístico completo y reproducible.

Este marco será **pre-registrado** en el Open Science Framework (OSF) antes del inicio de la recogida de datos, garantizando la transparencia y evitando sesgos de publicación.

---

## 2. Hipótesis de Investigación

### H1: Efecto del Tutor Adaptativo GCD

> **Un tutor adaptado mediante GCD produce mayor retención que un tutor estático.**

| Aspecto | Descripción |
|---------|-------------|
| **Variable Independiente (VI)** | Tipo de tutor: **GCD Adaptativo** vs **Estático** (control). |
| **Variable Dependiente (VD)** | **Retención** – puntuación en prueba de conocimiento administrada 1, 7 y 30 días después de la intervención. |
| **Operacionalización** | La retención se mide como el porcentaje de aciertos en un test de opción múltiple (20 ítems) sobre los contenidos trabajados. Se calcula la diferencia entre la puntuación post-test y la pre-test (ganancia de retención). |
| **Instrumento** | Test de conocimiento diseñado _ad hoc_ con validez de contenido verificada por tres expertos. |
| **Tamaño del efecto esperado** | Cohen's d = 0.50 (efecto medio) basado en estudios previos de tutoría adaptativa (VanLehn, 2011). |
| **Potencia estadística** | 1 - β = 0.80, α = 0.05 (bilateral). |

---

### H2: Predictores de Abandono

> **La persistencia predice mejor el abandono que el rendimiento académico.**

| Aspecto | Descripción |
|---------|-------------|
| **VI** | **Persistencia** – medida como el cociente entre el tiempo total dedicado y el número de sesiones activas, ajustado por intentos fallidos. **Rendimiento académico** – promedio de calificaciones en las evaluaciones sumativas. |
| **VD** | **Abandono** – variable binaria que indica si el participante completó o no las 8 semanas de intervención. |
| **Operacionalización** | La persistencia se calcula automáticamente por el sistema: `(tiempo_total / sesiones_activas) / intentos_fallidos` (escala 0-1). El rendimiento es la media de las notas en las pruebas semanales (0-10). |
| **Instrumento** | Registros del sistema (logs) para persistencia; pruebas semanales para rendimiento. |
| **Tamaño del efecto esperado** | Odds Ratio (OR) para persistencia ≥ 1.5, indicando que un incremento de 1 DE en persistencia reduce el riesgo de abandono en un 50%. |
| **Potencia estadística** | Regresión logística con n=120 y 2 predictores, potencia 0.80 para OR=1.5 (α=0.05). |

---

### H3: Aceleración Metacognitiva

> **La metacognición acelera la velocidad de aprendizaje.**

| Aspecto | Descripción |
|---------|-------------|
| **VI** | **Entrenamiento metacognitivo** – condición experimental donde los participantes reciben prompts de reflexión y autoevaluación durante la intervención. |
| **VD** | **Velocidad de aprendizaje** – pendiente de la curva de aprendizaje ajustada (modelo exponencial) para cada participante. |
| **Operacionalización** | La velocidad de aprendizaje se estima como el parámetro `b` en `conocimiento = a * (1 - exp(-b * sesión))`. Un valor mayor indica aprendizaje más rápido. |
| **Instrumento** | Curvas de conocimiento generadas a partir de las evaluaciones semanales. |
| **Tamaño del efecto esperado** | Diferencia de medias de `b` entre grupos ≥ 0.15 (escala 0-1), equivalente a d=0.40. |
| **Potencia estadística** | t-test para muestras independientes, n=60 por grupo, α=0.05, potencia 0.80 para d=0.40. |

---

### H4: Excepciones Cognitivas y Creatividad

> **Las excepciones cognitivas predicen creatividad futura.**

| Aspecto | Descripción |
|---------|-------------|
| **VI** | **Índice de excepción cognitiva** – frecuencia y tipo de respuestas divergentes o no esperadas durante la interacción con el sistema. |
| **VD** | **Creatividad** – puntuación en el Test de Pensamiento Creativo de Torrance (TTCT) versión figurativa, administrada al final del estudio. |
| **Operacionalización** | El índice de excepción se calcula como: `IE = (excepciones_observadas / excepciones_esperadas) * 100`, donde las excepciones esperadas se estiman a partir de datos normativos del sistema. |
| **Instrumento** | Registro automático de excepciones por el sistema GCD; TTCT para creatividad. |
| **Tamaño del efecto esperado** | Correlación de Pearson r ≥ 0.30 entre IE y TTCT (efecto medio). |
| **Potencia estadística** | n=120, α=0.05, potencia 0.80 para detectar r=0.30. |

---

## 3. Diseño Experimental

### 3.1. Tipo de Diseño

**Diseño mixto**:

- **Factor entre-sujetos**: Grupo (GCD Adaptativo vs Control Estático).
- **Factor intra-sujetos**: Tiempo (medidas repetidas en 8 sesiones semanales, más post-test a 1, 7 y 30 días).

Este diseño permite evaluar tanto diferencias entre grupos como trayectorias individuales de aprendizaje.

### 3.2. Asignación y Cegamiento

- **Aleatorización**: Los participantes serán asignados aleatoriamente a una de las dos condiciones mediante un generador de números aleatorios (block randomization con bloques de 4) estratificando por nivel de conocimiento previo (bajo/medio/alto) para garantizar equilibrio.
- **Cegamiento**: Los evaluadores (que administran las pruebas y codifican los datos) estarán cegados a la condición de los participantes. El participante no podrá ser cegado debido a la naturaleza de la intervención.

### 3.3. Condiciones Experimentales

| Grupo | Características | N |
|-------|-----------------|---|
| **GCD Adaptativo** | Tutoría que ajusta dinámicamente contenidos, dificultad y retroalimentación según el estado cognitivo del estudiante (conocimiento, atención, motivación, persistencia). Incorpora prompts metacognitivos y registra excepciones. | 60 |
| **Control Estático** | Tutoría con contenidos y secuencia fija, sin adaptación. La retroalimentación es genérica y no personalizada. Sin prompts metacognitivos. | 60 |

Ambos grupos utilizan la misma plataforma tecnológica y el mismo temario, diferenciándose únicamente en el motor de adaptación.

### 3.4. Poder Estadístico y Tamaño Muestral

El tamaño muestral se calculó con G*Power para cada hipótesis, utilizando el mayor n requerido.

- H1 (ANOVA mixto): n total = 100 (50 por grupo) para detectar interacción grupo×tiempo con f=0.25, α=0.05, potencia=0.80.
- H2 (Regresión logística): n total = 120 para OR=1.5 con dos predictores.
- H3 (t-test): n total = 120 (60 por grupo) para d=0.40.
- H4 (Correlación): n total = 120 para r=0.30.

Por tanto, **n total = 120** (60 por grupo) asegura potencia adecuada para todas las hipótesis.

---

## 4. Procedimiento

### 4.1. Reclutamiento y Screening

- **Canal**: Voluntarios reclutados a través de carteles en la universidad, redes sociales y correo electrónico.
- **Criterios de inclusión**:
  - Edad 18–35 años.
  - Sin conocimiento previo especializado en la materia (se evaluará con un test previo).
  - Disponibilidad para completar 8 semanas de intervención (2 sesiones/semana).
  - Acceso a ordenador con conexión a internet.
- **Criterios de exclusión**:
  - Diagnóstico de trastorno de aprendizaje o déficit de atención.
  - Participación en otro estudio similar en los últimos 6 meses.
  - Faltar a más de 2 sesiones sin justificación.
- **Screening**: Se aplicará un cuestionario breve para verificar criterios y obtener consentimiento.

### 4.2. Pre-test (Semana 0)

- **Duración**: 1 sesión de 60 minutos.
- **Actividades**:
  - Firma de consentimiento informado.
  - Recogida de datos demográficos (edad, género, nivel educativo, experiencia previa).
  - Aplicación del test de conocimiento base (pre-test) para medir nivel inicial.
  - Aplicación del cuestionario MAI (Metacognitive Awareness Inventory) y escala de motivación (intrínseca/extrínseca).
  - Familiarización con la plataforma (tutorial corto).

### 4.3. Intervención (Semanas 1–8)

- **Frecuencia**: 2 sesiones por semana (martes y jueves), 90 minutos cada una.
- **Estructura de cada sesión**:
  - **Apertura (5 min)**: Revisión de objetivos y activación de conocimientos previos.
  - **Contenido principal (60 min)**: Exposición de materiales y ejercicios prácticos. En el grupo GCD, la dificultad y el tipo de ejercicios se adaptan en tiempo real; en el grupo control, todos reciben el mismo material.
  - **Evaluación formativa (15 min)**: Mini-test de 5 preguntas para medir adquisición inmediata.
  - **Cierre metacognitivo (10 min)**: En el grupo GCD, se pide al estudiante que reflexione sobre su aprendizaje (¿qué fue fácil? ¿qué fue difícil? ¿cómo lo superó?). El grupo control realiza un resumen del contenido sin reflexión guiada.
- **Monitoreo**: El sistema registra todas las interacciones (tiempos de respuesta, aciertos/fallos, patrones de navegación, excepciones).

### 4.4. Post-test y Seguimiento

- **Post-test inmediato (Semana 9)**: Mismo test de conocimiento que el pre-test, más el TTCT (creatividad). Duración: 90 min.
- **Seguimiento a 7 días (Semana 10)**: Test de retención (versión paralela del test de conocimiento). Duración: 30 min.
- **Seguimiento a 30 días (Semana 13)**: Test de retención (otra versión paralela). Duración: 30 min.
- **Seguimiento a 90 días (opcional)**: Si los recursos lo permiten, se realizará un seguimiento adicional para evaluar retención a largo plazo.

---

## 5. Métricas y Variables

### 5.1. Variables Primarias

| Variable | Definición | Instrumento | Momento |
|----------|------------|-------------|---------|
| **Retención** | Puntuación en test de conocimiento (0-1) | Test de opción múltiple validado | Post-test (semana 9), seguimiento 7 y 30 días |
| **Abandono** | Binario (0=completa, 1=abandona) | Registro de asistencia | Durante la intervención |
| **Velocidad aprendizaje** | Pendiente `b` de la curva de conocimiento | Modelo exponencial ajustado a evaluaciones semanales | Semanas 1–8 |
| **Creatividad** | Puntuación en TTCT (percentil) | Test de Torrance (figurativo) | Post-test (semana 9) |

### 5.2. Variables Secundarias y de Proceso

| Variable | Definición | Instrumento | Momento |
|----------|------------|-------------|---------|
| **Persistencia** | Ratio `(tiempo_total / sesiones_activas) / intentos_fallidos` | Logs del sistema | Cada sesión |
| **Atención** | Auto-reporte de atención (escala 1-5) | Escala breve tras cada sesión | Cada sesión |
| **Motivación** | Auto-reporte de motivación (escala 1-5) | Escala breve tras cada sesión | Cada sesión |
| **Metacognición** | Puntuación en MAI | Cuestionario MAI | Pre-test y post-test |
| **Excepción cognitiva** | Índice de desviación de patrones esperados | Logs del sistema (GCD) | Cada sesión |
| **Carga cognitiva** | Puntuación en NASA-TLX | Cuestionario | Post-test |

---

## 6. Plan de Análisis Estadístico

### 6.1. Análisis por Hipótesis

| Hipótesis | Análisis Principal | Prueba Específica | Covariables |
|-----------|---------------------|-------------------|-------------|
| **H1** | ANOVA mixto (grupo × tiempo) | Efecto de interacción en retención | Conocimiento pre-test, edad |
| **H2** | Regresión logística | Modelo con persistencia y rendimiento como predictores | Género, motivación |
| **H3** | t-test para muestras independientes | Comparación de velocidades de aprendizaje entre grupos | Metacognición pre-test (ANCOVA) |
| **H4** | Correlación de Pearson | Correlación entre IE y creatividad (TTCT) | – |

**Detalles adicionales:**

- **H1**: Se utilizará el paquete `lme4` en R (`lmer`) para modelo mixto con efectos aleatorios de sujeto y pendiente de tiempo. Se contrastará la significancia mediante Satterthwaite.
- **H2**: Se evaluará la multicolinealidad (VIF) y la bondad de ajuste (Hosmer-Lemeshow). Se reportarán OR e IC 95%.
- **H3**: Si los supuestos de normalidad se violan, se usará U de Mann-Whitney. El tamaño del efecto se calculará con Cohen's d.
- **H4**: Se calculará el intervalo de confianza bootstrap de la correlación.

### 6.2. Ajustes por Comparaciones Múltiples

Dado que se prueban cuatro hipótesis principales, se aplicará una corrección de **Bonferroni** (α = 0.05 / 4 = 0.0125) para mantener el error tipo I global en 0.05. Los resultados se reportarán con p‑valores ajustados y no ajustados.

### 6.3. Software y Reproducibilidad

| Herramienta | Propósito |
|-------------|-----------|
| **R v4.3** (con `tidyverse`, `lme4`, `survival`, `lifelines`, `rstatix`) | Análisis estadístico principal |
| **Python 3.10** (con `pandas`, `statsmodels`, `scikit-learn`, `pingouin`) | Análisis complementarios y preprocesamiento |
| **RMarkdown / Quarto** | Generación de reportes reproducibles |
| **Docker** | Entorno computacional estandarizado |
| **OSF** | Almacenamiento de datos y pre‑registro |

Todos los scripts estarán disponibles en el repositorio GitHub del proyecto, y los datos anonimizados se publicarán en un repositorio de acceso abierto (ej. Zenodo) tras la finalización del estudio.

---

## 7. Consideraciones Éticas

- **Aprobación por Comité de Ética**: Se solicitará la aprobación del comité de ética de la institución antes del reclutamiento.
- **Consentimiento informado**: Todos los participantes firmarán un consentimiento informado (ver Anexo A).
- **Confidencialidad**: Los datos se anonimizarán asignando un código numérico a cada participante. La información personal se almacenará separadamente y con acceso restringido.
- **Derecho a retirarse**: Los participantes pueden retirarse en cualquier momento sin penalización.
- **Devolución de resultados**: Se ofrecerá a los participantes un resumen de los resultados generales del estudio.

---

## 8. Cronograma

| Fase | Duración | Fechas estimadas |
|------|----------|------------------|
| Pre‑registro y preparación | 2 semanas | Febrero 2026 |
| Reclutamiento y screening | 2 semanas | Marzo 2026 |
| Pre‑test | 1 semana | Marzo 2026 |
| Intervención (8 semanas) | 8 semanas | Abril – Mayo 2026 |
| Post‑test y seguimientos | 4 semanas | Junio 2026 |
| Análisis de datos | 6 semanas | Julio – Agosto 2026 |
| Elaboración de manuscrito | 8 semanas | Septiembre – Octubre 2026 |

---

## 9. Referencias

1. VanLehn, K. (2011). The relative effectiveness of human tutoring, intelligent tutoring systems, and other tutoring systems. *Educational Psychologist*, 46(4), 197-221. [DOI:10.1080/00461520.2011.611369](https://doi.org/10.1080/00461520.2011.611369)
2. Schraw, G., & Dennison, R. S. (1994). Assessing metacognitive awareness. *Contemporary Educational Psychology*, 19(4), 460-475.
3. Torrance, E. P. (1974). *Torrance Tests of Creative Thinking*. Scholastic Testing Service.
4. Pintrich, P. R., & De Groot, E. V. (1990). Motivational and self-regulated learning components of classroom academic performance. *Journal of Educational Psychology*, 82(1), 33-40.
5. Cohen, J. (1988). *Statistical Power Analysis for the Behavioral Sciences* (2nd ed.). Lawrence Erlbaum Associates.

---

## 10. Anexos

### A. Modelo de Consentimiento Informado

*(Se adjuntará documento PDF)*

### B. Plantilla de Datos (CSV)

Se proporcionará la plantilla en `data/templates/data_template.csv` con las columnas definidas en la Sección 5.

### C. Formulario de Screening

*(Se adjuntará documento)*

### D. Scripts de Análisis

Disponibles en el directorio `evaluation/` del repositorio.

---

<div align="center">

**[⬆ Volver Arriba](#-experimental-framework-v10)**

---

*Última actualización: 18 Enero 2026*  
*Versión: 1.0.0*  
*DOI (pre-registro): [pendiente]*  

</div>
