# 📊 Plantillas de Recogida de Datos

Esta sección contiene las plantillas estandarizadas para la recogida de datos del estudio, junto con su diccionario correspondiente. Los archivos están diseñados para ser compatibles con los scripts de análisis (`benchmark.py`, `metrics_report.py`, `statistical_analysis.py`) y garantizar la interoperabilidad entre módulos.

---

## 📁 Archivos incluidos

- `data/templates/data_template.csv` – plantilla CSV con las columnas predefinidas.
- `data/templates/data_dictionary.md` – diccionario de datos detallado (descripción, tipo, rango, valores permitidos).
- `data/templates/example_data.csv` – ejemplo de datos ficticios para ilustrar el formato (opcional).

---

## 📄 `data/templates/data_template.csv`

Este archivo contiene las columnas que deben registrarse **por sesión y sujeto**. Se incluye una fila de ejemplo con valores representativos.

```csv
subject_id,model,session,date,knowledge,retention,attention,motivation,persistence_effort,dropout,creativity
1,GCD,1,2026-04-01,0.42,0.38,4,3,0.65,False,
1,GCD,2,2026-04-03,0.58,0.52,4,4,0.70,False,
1,GCD,3,2026-04-06,0.71,0.63,5,4,0.72,False,
2,Control,1,2026-04-01,0.39,0.30,3,3,0.50,False,
2,Control,2,2026-04-03,0.45,0.35,3,2,0.48,False,
2,Control,3,2026-04-06,0.50,0.38,2,2,0.45,True,
```

### 📋 Columnas y especificaciones

| Columna | Tipo | Requerido | Descripción |
|---------|------|-----------|-------------|
| `subject_id` | Entero | Sí | Identificador único del participante (numérico). |
| `model` | Cadena | Sí | Condición experimental: `"GCD"` o `"Control"`. |
| `session` | Entero | Sí | Número de sesión (1‑16 en el estudio principal). |
| `date` | Fecha (ISO) | Opcional | Fecha de la sesión en formato `YYYY-MM-DD`. |
| `knowledge` | Flotante (0‑1) | Sí | Puntuación de conocimiento en la sesión (proporción de aciertos). |
| `retention` | Flotante (0‑1) | Sí | Puntuación de retención (medida en sesiones específicas). |
| `attention` | Entero (1‑5) | Sí | Auto‑reporte de atención (escala Likert). |
| `motivation` | Entero (1‑5) | Sí | Auto‑reporte de motivación (escala Likert). |
| `persistence_effort` | Flotante (0‑1) | Sí | Índice de esfuerzo persistente calculado por el sistema. |
| `dropout` | Booleano | Sí | Indicador de abandono en esa sesión (`True`/`False`). |
| `creativity` | Flotante (0‑100) | Opcional | Puntuación de creatividad (normalmente medida al final). |

---

## 📖 `data/templates/data_dictionary.md`

### Diccionario de datos detallado

#### `subject_id`
- **Descripción**: Identificador numérico único para cada participante.
- **Tipo**: Entero.
- **Rango**: 1 – 999.
- **Notas**: Se asigna secuencialmente al reclutar. No contiene información personal.

#### `model`
- **Descripción**: Grupo experimental al que pertenece el sujeto.
- **Tipo**: Cadena de texto (categórica).
- **Valores permitidos**: `"GCD"` (tutor adaptativo), `"Control"` (tutor estático).
- **Notas**: Debe coincidir con la asignación aleatoria.

#### `session`
- **Descripción**: Número de la sesión dentro del estudio.
- **Tipo**: Entero.
- **Rango**: 1 – 16 (para la intervención principal) + sesiones de seguimiento (etiquetadas como 17, 18, etc. si se desea).
- **Notas**: Las sesiones de seguimiento (post‑test a 7 y 30 días) pueden registrarse con números consecutivos (ej. 17, 18) o en un archivo separado; se recomienda mantener el mismo formato para facilitar el análisis longitudinal.

#### `date`
- **Descripción**: Fecha en que se realizó la sesión.
- **Tipo**: Cadena de texto en formato ISO (`YYYY-MM-DD`).
- **Notas**: Opcional pero recomendada para controlar efectos temporales.

#### `knowledge`
- **Descripción**: Proporción de respuestas correctas en la evaluación de conocimientos de la sesión.
- **Tipo**: Flotante.
- **Rango**: 0.0 – 1.0.
- **Notas**: Se calcula como (aciertos / total_ítems). Puede ser una evaluación formativa breve.

#### `retention`
- **Descripción**: Puntuación de retención, medida en sesiones específicas (post‑test y seguimientos). En sesiones regulares puede dejarse en blanco o repetir el valor de `knowledge` si se considera.
- **Tipo**: Flotante.
- **Rango**: 0.0 – 1.0.
- **Notas**: Se utiliza para la hipótesis H1. Se recomienda registrar solo en las sesiones de evaluación (post‑test, 7d, 30d).

#### `attention`
- **Descripción**: Nivel de atención auto‑reportado por el participante durante la sesión.
- **Tipo**: Entero (ordinal).
- **Rango**: 1 (muy baja) – 5 (muy alta).
- **Notas**: Se recoge mediante una pregunta simple al final de cada sesión.

#### `motivation`
- **Descripción**: Nivel de motivación auto‑reportado.
- **Tipo**: Entero (ordinal).
- **Rango**: 1 (muy baja) – 5 (muy alta).
- **Notas**: Similar a `attention`, recogida al final de la sesión.

#### `persistence_effort`
- **Descripción**: Índice de persistencia calculado automáticamente por el sistema como `(tiempo_total / sesiones_activas) / intentos_fallidos` normalizado a [0,1].
- **Tipo**: Flotante.
- **Rango**: 0.0 – 1.0.
- **Notas**: Valores altos indican mayor esfuerzo sostenido. Se usa en H2.

#### `dropout`
- **Descripción**: Indica si el participante abandonó el estudio en esa sesión (o antes de la siguiente).
- **Tipo**: Booleano (`True`/`False`).
- **Notas**: Una vez que `dropout` es `True`, las filas de sesiones posteriores deben tener valores nulos (`NaN` o vacío) para todas las columnas, ya que el sujeto ya no participa.

#### `creativity`
- **Descripción**: Puntuación de creatividad (normalmente medida solo en el post‑test).
- **Tipo**: Flotante (0‑100).
- **Rango**: 0 – 100 (puntuación directa o percentil).
- **Notas**: Se registra una vez por sujeto, generalmente en la sesión de post‑test. En sesiones regulares puede dejarse en blanco.

---

## ✅ Validación de compatibilidad

Los scripts de análisis (`benchmark.py`, `metrics_report.py`, `statistical_analysis.py`) han sido diseñados para trabajar con este esquema de datos. Se recomienda:

- Usar los nombres de columna **exactamente** como se indican (sensibles a mayúsculas/minúsculas).
- Mantener el tipo de dato correcto (ej. `dropout` como booleano, no como cadena).
- Para valores faltantes, usar `NaN` (en el CSV se puede dejar en blanco) – los scripts manejan `NaN` adecuadamente.

### Verificación rápida con Python

```python
import pandas as pd
df = pd.read_csv('data/templates/data_template.csv')
# Comprobar columnas esperadas
expected = ['subject_id', 'model', 'session', 'date', 'knowledge', 'retention',
            'attention', 'motivation', 'persistence_effort', 'dropout', 'creativity']
assert set(expected).issubset(set(df.columns)), "Faltan columnas"
# Comprobar tipos básicos
assert df['subject_id'].dtype == int
assert df['model'].dtype == object  # o category
assert df['dropout'].dtype == bool
```

---

## 📁 Estructura final

```
data/
└── templates/
    ├── data_template.csv        # Plantilla vacía con cabeceras
    ├── data_dictionary.md       # Este documento
    └── example_data.csv         # (Opcional) Datos sintéticos de ejemplo
```

---

## 🔗 Uso en el flujo de trabajo

1. **Recogida**: Los investigadores completan la plantilla para cada sujeto y sesión (manual o automáticamente desde el sistema).
2. **Preprocesamiento**: Los scripts de análisis cargan directamente el CSV y realizan las transformaciones necesarias (cálculo de métricas por sujeto, etc.).
3. **Análisis**: `benchmark.py` genera resultados agregados, `metrics_report.py` produce visualizaciones, y `statistical_analysis.py` ejecuta los modelos inferenciales.

---

<div align="center">

**[⬆ Volver al marco experimental](experimental_framework_v1.0.md)**

</div>
