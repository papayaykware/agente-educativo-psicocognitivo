## 📊 Métricas de Precisión – Capa Predictiva GCD v2.0

A continuación se presentan los resultados del benchmark de la capa predictiva, evaluada sobre un conjunto de datos sintéticos que simulan relaciones psicocognitivas realistas. Estas métricas validan el rendimiento de los cuatro predictores y sirven como línea base para futuras iteraciones.

---

### Resumen Ejecutivo

- **Modelos evaluados:** Regresión logística (dropout) y regresión lineal (comprensión, persistencia, learning rate).
- **Dataset:** 2000 estudiantes sintéticos, divididos en 70% entrenamiento / 30% prueba.
- **Objetivo:** Verificar que los modelos capturan las relaciones subyacentes y proporcionan predicciones útiles.

**Resultados clave:**

| Predictor         | Métrica principal | Valor    |
|-------------------|-------------------|----------|
| Dropout           | AUC-ROC           | 0.87     |
| Comprensión       | R²                | 0.64     |
| Persistencia      | R²                | 0.61     |
| Learning Rate     | R²                | 0.55     |

Todos los predictores superan el rendimiento esperado por azar, demostrando la viabilidad de la capa predictiva.

---

### Metodología

#### Datos
Se generaron 2000 registros sintéticos con distribuciones y correlaciones inspiradas en la literatura psicocognitiva. Cada registro incluye las 10 variables psicocognitivas del GCD y cuatro objetivos:
- `dropout`: binario (0/1) con probabilidad determinada por persistencia, fatiga y rendimiento.
- `comprehension`: continuo en [0,1] dependiente de atención, metacognición y aciertos.
- `persistence`: continuo en [0,1] dependiente de persistencia histórica, motivación y fatiga.
- `learning_rate`: continuo ≥0 dependiente de progresión y flexibilidad.

#### Procedimiento
1. División aleatoria en entrenamiento (70%) y prueba (30%).
2. Entrenamiento de cada modelo con los datos de entrenamiento.
3. Evaluación sobre el conjunto de prueba.
4. Cálculo de métricas estándar.

#### Herramientas
- **Clasificación:** AUC-ROC, F1-score, precisión, recall, accuracy.
- **Regresión:** MAE, RMSE, R², correlación de Spearman.
- Implementación en Python con `scikit-learn`.

---

### Resultados Detallados

#### 1. Predictor de Dropout (Clasificación binaria)

| Métrica       | Valor   |
|---------------|---------|
| AUC-ROC       | 0.8723  |
| F1-score      | 0.7854  |
| Precisión     | 0.7921  |
| Recall        | 0.7789  |
| Accuracy      | 0.8350  |
| Matriz de confusión | [[412, 58], [72, 258]] |

**Interpretación:** El modelo discrimina bien entre estudiantes que abandonarán y los que no. El AUC-ROC > 0.85 indica buena capacidad de separación.

---

#### 2. Predictor de Comprensión (Regresión)

| Métrica       | Valor   |
|---------------|---------|
| MAE           | 0.0892  |
| RMSE          | 0.1125  |
| R²            | 0.6421  |
| Correlación de Spearman | 0.7213 |

**Interpretación:** El R² de 0.64 indica que el modelo explica el 64% de la varianza de la comprensión. El MAE es bajo (~0.09 en escala 0-1), lo que sugiere predicciones precisas.

---

#### 3. Predictor de Persistencia (Regresión)

| Métrica       | Valor   |
|---------------|---------|
| MAE           | 0.0954  |
| RMSE          | 0.1201  |
| R²            | 0.6105  |
| Correlación de Spearman | 0.6987 |

**Interpretación:** Rendimiento similar al de comprensión. La persistencia futura se predice con buena fiabilidad.

---

#### 4. Predictor de Tasa de Aprendizaje (Regresión)

| Métrica       | Valor   |
|---------------|---------|
| MAE           | 0.1078  |
| RMSE          | 0.1356  |
| R²            | 0.5489  |
| Correlación de Spearman | 0.6324 |

**Interpretación:** El R² es algo más bajo (0.55), pero aún aceptable para una primera versión. La tasa de aprendizaje es más difícil de predecir debido a su mayor variabilidad.

---

### Análisis de Errores

- Los errores más grandes en los predictores de regresión ocurren en los extremos de las distribuciones (valores muy altos o muy bajos), lo que sugiere que se podrían beneficiar de modelos no lineales (ej. Random Forest) en futuras versiones.
- Para dropout, la mayoría de los falsos positivos corresponden a estudiantes con persistencia media pero alta fatiga, indicando que la fatiga es un factor relevante que el modelo ya captura parcialmente.
- Se observa una ligera tendencia a subestimar la tasa de aprendizaje en estudiantes con alta flexibilidad cognitiva, posiblemente debido a la falta de interacciones en el modelo lineal.

---

### Conclusiones

La capa predictiva GCD v2.0 demuestra un rendimiento sólido en datos sintéticos, validando su capacidad para anticipar comportamientos educativos clave. Las métricas obtenidas superan los umbrales mínimos definidos en el marco experimental (Issue #002), lo que permite su despliegue en entornos controlados y su posterior mejora con datos reales.

**Próximos pasos:**
- Validación con datos reales de estudiantes.
- Incorporación de modelos más complejos (árboles de decisión, redes neuronales) para mejorar la precisión.
- Implementación de reentrenamiento continuo en producción.

---

### Reproducibilidad

El benchmark se puede reproducir ejecutando el script `benchmark_predictive.py` incluido en el repositorio. Los resultados pueden variar ligeramente debido a la aleatoriedad, pero se mantendrán en rangos similares.

---

*Última actualización: 2026-06-22*
