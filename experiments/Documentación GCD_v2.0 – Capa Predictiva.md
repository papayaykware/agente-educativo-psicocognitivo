# Documentación GCD_v2.0 – Capa Predictiva

A continuación se presenta la documentación completa de la versión **GCD_v2.0**, que incorpora la **capa predictiva** al Gemelo Cognitivo Dinámico (GCD). Esta documentación está diseñada para su publicación en el repositorio de GitHub, dentro de la carpeta `experiments/` o como parte de la documentación central del proyecto.

---

## 📘 GCD_v2.0 – Capa Predictiva del Gemelo Cognitivo Dinámico

### 1. Introducción

El **Gemelo Cognitivo Dinámico (GCD)** es un modelo computacional que representa el estado psicocognitivo de un estudiante en tiempo real, integrando variables como atención, motivación, persistencia, metacognición, flexibilidad cognitiva, fatiga, engagement, y rendimiento. Hasta la versión v1.0, el GCD operaba como un sistema **descriptivo-reactivo**: monitorizaba y adaptaba la intervención en función del estado actual del estudiante.

Con la **versión v2.0**, el GCD se convierte en un sistema **predictivo-adaptativo**, capaz de anticipar comportamientos críticos y resultados de aprendizaje futuros. Esta capacidad predictiva permite al tutor educativo intervenir de forma proactiva, mejorando la retención, la comprensión y la tasa de aprendizaje.

La capa predictiva se implementa como un módulo de software independiente, entrenable con datos históricos y fácilmente integrable en el flujo de trabajo del GCD.

---

### 2. Arquitectura de la Capa Predictiva

La capa predictiva está compuesta por **cuatro modelos supervisados**, cada uno entrenado para predecir una variable objetivo específica a partir de las variables psicocognitivas del GCD.

```
┌──────────────────────────────────────────────────────────────┐
│                     CAPA PREDICTIVA GCD v2.0                 │
├──────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────────┐  ┌──────────────────┐  │
│  │ Preprocesado│→│ Modelo Dropout  │→│ predict_dropout()  │  │
│  │ (scaler)    │  │ (Logistic Reg.) │  │   (probabilidad) │  │
│  └─────────────┘  └─────────────────┘  └──────────────────┘  │
│  ┌─────────────┐  ┌─────────────────┐  ┌──────────────────┐  │
│  │ Preprocesado│→│ Modelo Compren. │→│predict_compreh.()  │  │
│  │ (scaler)    │  │ (Linear Reg.)   │  │   (nivel 0-1)    │  │
│  └─────────────┘  └─────────────────┘  └──────────────────┘  │
│  ┌─────────────┐  ┌─────────────────┐  ┌──────────────────┐  │
│  │ Preprocesado│→│ Modelo Persist. │→│predict_persist.()  │  │
│  │ (scaler)    │  │ (Linear Reg.)   │  │   (nivel 0-1)    │  │
│  └─────────────┘  └─────────────────┘  └──────────────────┘  │
│  ┌─────────────┐  ┌─────────────────┐  ┌──────────────────┐  │
│  │ Preprocesado│→│ Modelo LearnRate │→│predict_learnRate()│  │
│  │ (scaler)    │  │ (Linear Reg.)   │  │   (tasa >=0)     │  │
│  └─────────────┘  └─────────────────┘  └──────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

Cada modelo sigue un pipeline común:
1. **Escalado estándar** de las variables de entrada (media 0, desviación 1).
2. **Modelo base** (regresión logística para clasificación, regresión lineal para regresión).
3. **Postprocesado** (clip de salidas, transformación de probabilidades).

Los modelos se entrenan por separado, pero comparten las mismas características de entrada. Esto permite una implementación modular y una fácil sustitución de algoritmos.

---

### 3. Predictores Disponibles

#### 3.1 `predict_dropout()`

- **Objetivo:** Estimar la probabilidad de que el estudiante abandone la actividad educativa en el corto plazo.
- **Variables clave:** Persistencia (baja), fatiga (alta), rendimiento (bajo), engagement (bajo).
- **Salida:** `float` entre 0 y 1 (probabilidad).
- **Uso típico:** Activar alertas tempranas y estrategias de retención.

#### 3.2 `predict_comprehension()`

- **Objetivo:** Predecir el nivel de comprensión del contenido actual o próximo.
- **Variables clave:** Atención, metacognición, aciertos previos.
- **Salida:** `float` entre 0 y 1 (nivel de comprensión estimado).
- **Uso típico:** Ajustar la dificultad o el ritmo del material.

#### 3.3 `predict_persistence()`

- **Objetivo:** Predecir la persistencia futura del estudiante (capacidad de mantenerse en la tarea).
- **Variables clave:** Persistencia histórica, motivación, fatiga.
- **Salida:** `float` entre 0 y 1 (nivel de persistencia esperado).
- **Uso típico:** Personalizar refuerzos positivos y dosificar la carga de trabajo.

#### 3.4 `predict_learning_rate()`

- **Objetivo:** Estimar la tasa de aprendizaje futura (velocidad de adquisición de nuevos conocimientos).
- **Variables clave:** Progresión histórica, flexibilidad cognitiva.
- **Salida:** `float` ≥ 0 (tasa de aprendizaje, en unidades normalizadas).
- **Uso típico:** Planificar secuencias de aprendizaje y estimar tiempos de finalización.

---

### 4. Integración con el GCD

La capa predictiva se integra en el GCD mediante la clase `PredictiveLayer`, que gestiona el entrenamiento, persistencia y predicción. El GCD puede llamar a los métodos predictivos en cada actualización de estado del estudiante.

**Ejemplo de integración:**

```python
from predictors import PredictiveLayer

# Cargar modelos pre-entrenados
layer = PredictiveLayer()
layer.load_models(prefix="gcd_production")

# Obtener estado actual del estudiante (diccionario)
estado = {
    'atencion': 0.75,
    'motivacion': 0.82,
    'persistencia': 0.60,
    'metacognicion': 0.70,
    'flexibilidad_cognitiva': 0.65,
    'rendimiento': 0.80,
    'engagement': 0.85,
    'fatiga': 0.30,
    'aciertos_previos': 12,
    'progresion_historica': 0.55
}

# Obtener predicciones
dropout_prob = layer.predict_dropout(estado)
comp_level = layer.predict_comprehension(estado)
persist_future = layer.predict_persistence(estado)
lr = layer.predict_learning_rate(estado)

# Tomar decisiones adaptativas
if dropout_prob > 0.6:
    activar_plan_retencion()
if comp_level < 0.4:
    reducir_dificultad()
```

La latencia de cada predicción es **< 100 ms** en hardware estándar, lo que permite su uso en tiempo real.

---

### 5. Guía de Uso

#### 5.1 Entrenamiento inicial

Para entrenar los modelos con datos históricos:

```python
import pandas as pd
from predictors import PredictiveLayer

# Cargar dataset con variables psicocognitivas y objetivos
data = pd.read_csv('datos_historicos.csv')

layer = PredictiveLayer()
target_cols = {
    'dropout': 'dropout_col',
    'comprehension': 'comp_col',
    'persistence': 'persist_col',
    'learning_rate': 'lr_col'
}
layer.fit(data, target_cols)
layer.save_models(prefix="gcd_model")
```

#### 5.2 Carga en producción

```python
layer = PredictiveLayer()
layer.load_models(prefix="gcd_model")
```

#### 5.3 Predicción por lotes

```python
estudiantes = [estado1, estado2, estado3]  # lista de diccionarios
df_pred = layer.predict_batch(estudiantes)
print(df_pred)
```

#### 5.4 Funciones de conveniencia

Si los modelos están guardados en la ubicación predeterminada (`./models/gcd_*.pkl`), se pueden usar las funciones directamente:

```python
from predictors import predict_dropout, predict_comprehension

prob = predict_dropout(estado)
comp = predict_comprehension(estado)
```

---

### 6. Extensibilidad

La capa predictiva está diseñada para ser extendida fácilmente:

- **Nuevos predictores:** Añadir un nuevo método en `PredictiveLayer` siguiendo la misma interfaz.
- **Modelos alternativos:** Sustituir el pipeline de un predictor por cualquier estimador de `scikit-learn` o personalizado.
- **Variables adicionales:** Ampliar la lista `VARIABLES_PSICO` y reentrenar los modelos.

Para añadir un nuevo predictor, basta con implementar el método de entrenamiento y el de predicción, siguiendo el patrón de los existentes.

---

### 7. Consideraciones Técnicas

- **Lenguaje:** Python 3.10+
- **Dependencias principales:** `numpy`, `pandas`, `scikit-learn`, `joblib`
- **Persistencia:** Modelos serializados con `joblib` para carga rápida.
- **Privacidad:** Los datos de entrada no se almacenan; solo se usan en memoria durante la predicción.
- **Mantenimiento:** Se recomienda reentrenar periódicamente los modelos para evitar la deriva conceptual.
- **Rendimiento:** Optimizado para baja latencia (< 100 ms por estudiante).

---

### 8. Referencias

- [GCD Experimental Validation v0.1 – Hipótesis y métricas](https://github.com/papayaykware/agente-educativo-psicocognitivo/blob/main/experiments/GCD%20Experimental%20Validation%20v0.1.md)
- [Experimental Framework v1.0](https://github.com/papayaykware/agente-educativo-psicocognitivo/blob/main/experiments/Experimental%20Framework%20Documentationv1.0.md)
- Issue #002 – Predictive Layer v1.0 (en este repositorio)
- [Scikit-learn Documentation](https://scikit-learn.org/)

---

### 9. Historial de Versiones

| Versión | Fecha       | Cambios                                |
|---------|-------------|----------------------------------------|
| v2.0    | 2026-06-22  | Lanzamiento inicial de la capa predictiva. |

---

**Autores:** Equipo de desarrollo del GCD  
**Contacto:** *(opcional)*

