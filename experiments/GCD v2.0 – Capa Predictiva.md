# 🧠 GCD v2.0 – Capa Predictiva
## De la descripción a la anticipación

---

> **📌 Estado:** Propuesta de evolución del Gemelo Cognitivo Dinámico (GCD)  
> **Repositorio:** [agente-educativo-psicocognitivo](https://github.com/papayaykware/agente-educativo-psicocognitivo)  
> **Basado en:** Issue #002 y la implementación `predictors.py`  
> **Fecha:** 2026-06-22

---

## 1. Introducción y Motivación

La comunidad científica valora especialmente los modelos que generan **predicciones verificables** frente a aquellos que solo describen fenómenos complejos. Las arquitecturas cognitivas y metacognitivas más influyentes han perdurado porque podían ser contrastadas experimentalmente.

Actualmente, el GCD modela variables como comprensión, retención, atención, motivación y persistencia. **Esto es útil, pero sigue siendo descriptivo.** El sistema observa, adapta y reacciona, pero no anticipa.

El siguiente paso lógico es dotar al GCD de capacidad predictiva, transformándolo en un sistema **proactivo** que no solo responda al estado actual, sino que **prevenga** estados futuros indeseados.

---

## 2. El Salto Científico

La evolución del GCD v1.0 (descriptivo) a GCD v2.0 (predictivo) se resume en:

```
GCD v2.0 = GCD v1.0 + Predictive Layer
```

Esta capa predictiva añade las siguientes funcionalidades:

| Función | Descripción | Estado en v2.0 |
|---------|-------------|----------------|
| `predicted_comprehension` | Nivel de comprensión futura | ✅ Implementado (`predict_comprehension()`) |
| `predicted_dropout` | Probabilidad de abandono | ✅ Implementado (`predict_dropout()`) |
| `predicted_engagement` | Nivel de implicación futura | 🚧 En desarrollo (extensión de `predict_persistence()`) |
| `predicted_mastery` | Probabilidad de alcanzar dominio | 🚧 Planeado para v2.1 |

La filosofía subyacente se inspira en modelos de aprendizaje adaptativo con **teoría de la mente** ([teacher-with-tom.github.io](https://teacher-with-tom.github.io)), donde el sistema mantiene un modelo interno del estudiante y predice su evolución para ajustar la enseñanza de manera proactiva.

> 🔮 **Visión GCD v2.0**  
> - El sistema mantiene una **representación interna del estudiante** (modelo del aprendiz).  
> - **Predice su estado futuro** (ej. probabilidad de olvido, riesgo de abandono).  
> - **Ajusta la enseñanza proactivamente** (no solo reactivamente).

---

## 3. Arquitectura Propuesta

La capa predictiva se integra en el GCD mediante un flujo de trabajo continuo que combina observación, predicción y acción.

### 3.1 Componentes Clave

| Componente | Descripción | Tecnología sugerida |
|------------|-------------|----------------------|
| **Modelo de Estado** | Vector de estado cognitivo de baja dimensionalidad | Autoencoders, PCA |
| **Predictor de Transición** | Predice el siguiente estado dado el actual y la intervención | LSTM, Transformers, Modelos Ocultos de Markov |
| **Función de Coste** | Mide discrepancia entre estado actual y objetivo | Distancia de Mahalanobis, KL‑divergencia |
| **Política de Actuación** | Decide qué contenido/estrategia entregar para minimizar el coste | Bandidos contextuales, Aprendizaje por Refuerzo |

### 3.2 Flujo de Trabajo

1. **Observación**: El tutor recoge respuestas, tiempos de reacción, errores, etc.  
2. **Actualización del modelo interno**: Se actualiza el vector de estado (ej. con filtro de Kalman o red recurrente).  
3. **Predicción**: Se estima el estado en el siguiente paso (o en un horizonte temporal).  
4. **Evaluación**: Si la predicción se desvía del objetivo (coste alto), se selecciona una acción correctiva.  
5. **Intervención**: Se aplica la acción (cambio de contenido, refuerzo, pausa, etc.).  
6. **Registro**: Se almacena el resultado para retroalimentar y mejorar los modelos.

Este ciclo se repite en tiempo real, permitiendo una **adaptación continua** y **anticipada**.

---

## 4. Evaluación y Métricas

La capa predictiva será validada mediante tres enfoques complementarios:

1. **Precisión de predicción** (benchmark):
   - Métricas: RMSE, MAE, R², AUC‑ROC (según el predictor).
   - Comparación con modelos baseline (ej. media histórica).
   - Resultados iniciales (sobre datos sintéticos) disponibles en [`benchmark_predictive.py`](https://github.com/papayaykware/agente-educativo-psicocognitivo/blob/main/experiments/benchmark_predictive.py).

2. **Mejora en retención**:
   - Experimento controlado: GCD v1.0 (descriptivo) vs. GCD v2.0 (predictivo).
   - Medición de la retención a largo plazo (pruebas diferidas).

3. **Reducción de abandono**:
   - Seguimiento de la tasa de abandono en escenarios reales (o simulados) con y sin intervención predictiva.

Todos los experimentos se ajustan al [Marco Experimental v1.0](https://github.com/papayaykware/agente-educativo-psicocognitivo/blob/main/experiments/Experimental%20Framework%20Documentationv1.0.md).

---

## 5. Integración con la Implementación Actual

La capa predictiva ya cuenta con una implementación funcional en Python (véase [`predictors.py`](https://github.com/papayaykware/agente-educativo-psicocognitivo/blob/main/experiments/predictors.py)). Esta implementación incluye:

- Clase `PredictiveLayer` para entrenamiento, persistencia y predicción.
- Cuatro predictores iniciales (`dropout`, `comprehension`, `persistence`, `learning_rate`).
- Funciones de conveniencia para uso directo.
- Script de benchmark para validación.

El código está diseñado para ser **extensible**; la adición de nuevos predictores (como `engagement` o `mastery`) solo requiere seguir el mismo patrón de interfaz.

---

## 6. Próximos Pasos

- ✅ **Implementar la capa predictiva básica** (Issue #002 completada).  
- 🔄 **Validar con datos reales** de estudiantes (en curso).  
- 🔄 **Mejorar modelos** (pasar de regresión lineal a árboles de decisión o redes neuronales).  
- 🚧 **Añadir predictores de engagement y mastery** (Issue #003 – planificada).  
- 🚧 **Incorporar el ciclo completo de intervención proactiva** (integración con el tutor adaptativo).  

---

## 7. Cómo Contribuir

Si deseas colaborar en la evolución del GCD hacia un sistema predictivo:

1. **Explora el código** en [`experiments/`](https://github.com/papayaykware/agente-educativo-psicocognitivo/tree/main/experiments).  
2. **Prueba el benchmark** con datos sintéticos o reales.  
3. **Propón mejoras** en los modelos predictivos o en la arquitectura (abre un Issue o Pull Request).  
4. **Comparte tus ideas** sobre cómo integrar la predicción en la experiencia educativa.  

---

## 8. Referencias

- [GCD Experimental Validation v0.1 – Hipótesis y métricas](https://github.com/papayaykware/agente-educativo-psicocognitivo/blob/main/experiments/GCD%20Experimental%20Validation%20v0.1.md)  
- [Experimental Framework v1.0](https://github.com/papayaykware/agente-educativo-psicocognitivo/blob/main/experiments/Experimental%20Framework%20Documentationv1.0.md)  
- [Issue #002 – Predictive Layer v1.0](https://github.com/papayaykware/agente-educativo-psicocognitivo/blob/main/experiments/Issue%20%23002%20%E2%80%93%20Predictive%20Layer%20v1.0.md)  
- Teacher with Theory of Mind – [teacher-with-tom.github.io](https://teacher-with-tom.github.io)

---

> **Nota final:** La transición de un sistema descriptivo a uno predictivo no solo mejora la efectividad educativa, sino que también aumenta la **transparencia y verificabilidad** del modelo, alineándolo con las mejores prácticas de la ciencia cognitiva computacional.

---

*Última actualización: 2026-06-22*
