# Issue #002 – Predictive Layer v1.0

**Estado:** Pendiente  
**Prioridad:** Alta  
**Repositorio:** [agente-educativo-psicocognitivo](https://github.com/papayaykware/agente-educativo-psicocognitivo)  
**Relacionado con:** [GCD Experimental Validation v0.1](https://github.com/papayaykware/agente-educativo-psicocognitivo/blob/main/experiments/GCD%20Experimental%20Validation%20v0.1.md) · [Experimental Framework v1.0](https://github.com/papayaykware/agente-educativo-psicocognitivo/blob/main/experiments/Experimental%20Framework%20Documentationv1.0.md) · Issue #001

---

## 1. Título

**Predictive Layer v1.0**

---

## 2. Objetivo General

Incorporar capacidades predictivas al **Gemelo Cognitivo Dinámico (GCD)** , transformando el sistema de un modelo descriptivo-reactivo a uno **predictivo-adaptativo**. La capa predictiva permitirá anticipar comportamientos críticos del estudiante y ajustar la intervención educativa de forma proactiva.

---

## 3. Contexto

El GCD ha demostrado capacidad para describir y adaptarse a variables psicocognitivas como atención, motivación, persistencia, metacognición y flexibilidad cognitiva. Sin embargo, su verdadero valor científico y aplicado radica en su **capacidad predictiva**: ¿puede el GCD anticipar resultados de aprendizaje a partir de estas variables?

La validación experimental del GCD (v0.1) plantea hipótesis que exigen capacidad predictiva, como:
- **GCD-002:** La persistencia predice mejor el abandono que el rendimiento académico.
- **GCD-001:** La adaptación basada en GCD mejora la progresión de aprendizaje.

Issue #002 materializa esta capacidad predictiva en una capa de software integrada en el GCD.

---

## 4. Funcionalidades Iniciales

La capa predictiva v1.0 implementará **cuatro predictores básicos**, operacionalizados a partir de las variables psicocognitivas del GCD:

| Función | Descripción | Variable(s) de entrada | Salida |
|---------|-------------|------------------------|--------|
| `predict_dropout()` | Predice probabilidad de abandono del estudiante | Persistencia, rendimiento, engagement | `float` (0–1) |
| `predict_comprehension()` | Predice nivel de comprensión del contenido | Atención, metacognición, aciertos previos | `float` (0–1) |
| `predict_persistence()` | Predice persistencia futura del estudiante | Persistencia histórica, motivación, fatiga | `float` (0–1) |
| `predict_learning_rate()` | Predice velocidad de aprendizaje futura | Progresión histórica, flexibilidad cognitiva | `float` (tasa) |

Todas las funciones seguirán una interfaz unificada:
```python
def predict_*(student_data: Dict, context: Optional[Dict] = None) -> float
```

---

## 5. Entregables

### 5.1. `predictors.py`
Módulo Python que contiene la implementación de los cuatro predictores. Incluirá:
- Modelos predictivos (regresión logística, modelos lineales o árboles de decisión según validación).
- Preprocesamiento de variables psicocognitivas.
- Funciones de carga y persistencia de modelos entrenados.
- Docstrings y typing completo.

### 5.2. `benchmark_predictive.py`
Script de evaluación y validación de los predictores. Incluirá:
- Carga de datos históricos (sintéticos o reales).
- Entrenamiento y validación cruzada (k-fold).
- Cálculo de métricas de precisión (ver sección 6).
- Generación de reporte comparativo entre predictores.

### 5.3. Documentación **GCD_v2.0**
Actualización de la documentación del sistema que incorpore:
- Arquitectura de la capa predictiva.
- Descripción de cada predictor, su fundamento psicocognitivo y su uso.
- Ejemplos de integración con el tutor adaptativo.
- Guía de extensión para nuevos predictores.

### 5.4. Métricas de Precisión
Para cada predictor se reportarán al menos las siguientes métricas:
- **Dropout:** AUC-ROC, F1-score, sensibilidad, especificidad.
- **Comprensión:** MAE, RMSE, R².
- **Persistencia:** MAE, RMSE, correlación de Spearman.
- **Learning Rate:** MAE, RMSE, R².

Además, se calculará el **error de generalización** mediante validación cruzada y, cuando sea posible, se contrastará con los criterios de éxito definidos en el marco experimental.

---

## 6. Criterios de Aceptación

- [ ] Los cuatro predictores están implementados y documentados en `predictors.py`.
- [ ] `benchmark_predictive.py` ejecuta sin errores y genera un reporte de métricas.
- [ ] Todas las métricas de precisión superan los umbrales mínimos definidos (según validación estadística).
- [ ] La documentación GCD_v2.0 incluye un capítulo completo sobre la capa predictiva.
- [ ] El código pasa las pruebas unitarias (cobertura ≥ 80 %).
- [ ] Los predictores son invocables desde el GCD en tiempo real con latencia < 100 ms.

---

## 7. Consideraciones Técnicas

- **Lenguaje:** Python 3.10+.
- **Dependencias:** `numpy`, `pandas`, `scikit-learn`, `statsmodels` (opcional).
- **Arquitectura:** Los predictores se diseñarán como **servicios desacoplados** para facilitar su evolución y sustitución.
- **Persistencia:** Los modelos entrenados se serializarán con `joblib` o `pickle` para su carga en producción.
- **Privacidad:** Los datos de entrada serán anonimizados y no se almacenarán fuera de la sesión del usuario.

---

## 8. Plan de Implementación Sugerido

| Fase | Tarea | Duración estimada |
|------|-------|-------------------|
| 1 | Diseño de la interfaz y definición de tipos | 1 día |
| 2 | Implementación de `predict_dropout()` y `predict_persistence()` | 3 días |
| 3 | Implementación de `predict_comprehension()` y `predict_learning_rate()` | 3 días |
| 4 | Desarrollo de `benchmark_predictive.py` y validación | 2 días |
| 5 | Redacción de documentación GCD_v2.0 | 2 días |
| 6 | Pruebas unitarias y de integración | 2 días |

**Total estimado:** 13 días hábiles.

---

## 9. Riesgos y Mitigación

| Riesgo | Mitigación |
|--------|------------|
| Datos insuficientes para entrenar modelos robustos | Usar datos sintéticos validados y técnicas de bootstrapping |
| Sobreajuste de los predictores | Validación cruzada estricta y regularización |
| Latencia excesiva en tiempo real | Optimizar con modelos ligeros (ej. regresión logística vs. redes neuronales) |
| Deriva conceptual (cambios en la población de estudiantes) | Implementar mecanismo de reentrenamiento periódico |

---

## 10. Referencias

- [GCD Experimental Validation v0.1 – Hipótesis y métricas](https://github.com/papayaykware/agente-educativo-psicocognitivo/blob/main/experiments/GCD%20Experimental%20Validation%20v0.1.md)
- [Experimental Framework Documentation v1.0 – Diseño experimental](https://github.com/papayaykware/agente-educativo-psicocognitivo/blob/main/experiments/Experimental%20Framework%20Documentationv1.0.md)
- [Issue #001 – Experimental Framework v1.0](https://github.com/papayaykware/agente-educativo-psicocognitivo/blob/main/experiments/Issue%20%23001%20%E2%80%93%20Experimental%20Framework%20v1.0.md)

---

**Asignado a:** *(por definir)*  
**Fecha de creación:** 2026-06-22  
**Última actualización:** 2026-06-22
