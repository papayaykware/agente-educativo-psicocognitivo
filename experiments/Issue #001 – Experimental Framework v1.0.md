# 📋 Issue #001 – Experimental Framework v1.0

> **Estado:** Abierto  
> **Prioridad:** Alta  
> **Hito:** Lanzamiento v1.0  
> **Etiquetas:** `documentation`, `experimental-design`, `pre-registration`  
> **Asignado:** @.......... 

---

## 🎯 Objetivo

Documentar y publicar el marco experimental completo que guiará la recogida de datos para validar las hipótesis del proyecto GCD. Este marco debe ser **reproducible, transparente y pre-registrable** en un repositorio abierto (OSF), garantizando que los resultados sean científicos y verificables.

El entregable final será un conjunto de documentos listos para ser utilizados en la fase de recogida de datos, incluyendo:

- Protocolo experimental detallado
- Plantillas de datos estandarizadas
- Criterios de inclusión/exclusión
- Consentimiento informado
- Registro pre-registro en OSF

---

## 📝 Tareas

### 1. Finalizar `experimental_framework_v1.0.md`

- [ ] Revisar y completar las **hipótesis H1–H4** con:
  - Variables independientes y dependientes claramente definidas.
  - Operacionalización de cada variable (instrumentos de medición).
  - Tamaño del efecto esperado y potencia estadística.
- [ ] Incluir **diseño experimental**:
  - Tipo de diseño (entre-sujetos, intra-sujetos, mixto).
  - Asignación aleatoria y cegamiento.
  - Condiciones experimentales (grupo GCD vs Control).
- [ ] Detallar el **procedimiento** paso a paso:
  - Reclutamiento, screening, pre-test, intervención, post-test, seguimiento.
  - Duración y frecuencia de las sesiones.
- [ ] Definir **métricas primarias y secundarias**:
  - Retención, abandono, velocidad de aprendizaje, creatividad.
  - Variables de proceso (atención, motivación, persistencia, metacognición).
- [ ] Especificar el **plan de análisis estadístico**:
  - Pruebas a utilizar para cada hipótesis.
  - Criterios de significancia y ajustes por comparaciones múltiples.
  - Software y scripts a utilizar.

**Referencia:** El borrador inicial se encuentra en [`experimental_framework_v1.0.md`](experimental_framework_v1.0.md). Se debe completar con los detalles faltantes.

---

### 2. Crear plantillas de recogida de datos (CSV estandarizadas)

- [ ] Definir un esquema de datos común para todas las sesiones y sujetos.
- [ ] Crear plantillas CSV con columnas predefinidas:
  - `subject_id`, `group` (GCD/Control), `session`, `date`, `knowledge_score`, `retention_score`, `attention_rating`, `motivation_rating`, `persistence_effort`, `dropout_flag`, `creativity_score`, etc.
- [ ] Incluir un diccionario de datos (descripción de cada campo, tipo, rango).
- [ ] Asegurar que las plantillas sean compatibles con los scripts de análisis (`benchmark.py`, `metrics_report.py`, `statistical_analysis.py`).

**Entregable:** Archivos CSV de ejemplo y documentación en la carpeta `data/templates/`.

---

### 3. Definir criterios de inclusión/exclusión para participantes

- [ ] Establecer criterios de inclusión:
  - Edad mínima/máxima.
  - Nivel educativo (o ausencia de).
  - Conocimientos previos requeridos (o no).
  - Disponibilidad para completar el estudio.
- [ ] Establecer criterios de exclusión:
  - Condiciones médicas o psicológicas que interfieran.
  - Participación simultánea en otros estudios similares.
  - Incumplimiento de las sesiones (definir umbral de abandono).
- [ ] Redactar un **formulario de screening** para aplicar a los candidatos.

**Entregable:** Sección en el protocolo experimental y documento de screening.

---

### 4. Redactar protocolo de consentimiento informado

- [ ] Elaborar un documento de consentimiento informado que cumpla con estándares éticos (declaración de Helsinki, GDPR si aplica).
- [ ] Incluir:
  - Propósito del estudio.
  - Procedimientos (duración, tareas, riesgos/beneficios).
  - Confidencialidad y anonimización de datos.
  - Derecho a retirarse sin consecuencias.
  - Contacto para preguntas.
- [ ] Preparar una versión en formato PDF para firmar.

**Entregable:** `consent_form_v1.0.pdf` y versión editable (Word/LaTeX).

---

### 5. Establecer registro pre‑registro en Open Science Framework (OSF)

- [ ] Crear una cuenta en OSF (si no existe) y un proyecto para el estudio.
- [ ] Subir el protocolo experimental, plantillas de datos, y análisis planificado.
- [ ] Completar el formulario de pre‑registro con toda la información requerida.
- [ ] Obtener un DOI para el pre‑registro y añadirlo al repositorio (en el README y en el marco experimental).

**Entregable:** Enlace al pre‑registro y DOI asignado.

---

## 📦 Entregables finales

Al cerrar este issue, el repositorio debe contener:

1. `docs/experimental_framework_v1.0.md` – documento completo del marco experimental.
2. `data/templates/data_template.csv` – plantilla de recogida de datos con diccionario.
3. `docs/screening_form.md` – criterios de inclusión/exclusión y formulario.
4. `docs/consent_form_v1.0.pdf` – consentimiento informado.
5. Enlace al pre‑registro en OSF (en el README y en el marco experimental).

---

## 🔗 Referencias y recursos

- [OSF Pre‑registration](https://osf.io/prereg/)
- [Consentimiento informado – guía](https://www.wma.net/policies-post/wma-declaration-of-helsinki-ethical-principles-for-medical-research-involving-human-subjects/)
- [GDPR y protección de datos](https://gdpr-info.eu/)

---

## ✅ Checklist de revisión

- [ ] Todas las hipótesis están claramente formuladas y operacionalizadas.
- [ ] El diseño experimental es apropiado para las hipótesis.
- [ ] Las métricas están bien definidas y son medibles.
- [ ] El plan de análisis estadístico es riguroso y se ajusta a las hipótesis.
- [ ] Las plantillas de datos son completas y compatibles con los scripts.
- [ ] Los criterios de inclusión/exclusión son claros y aplicables.
- [ ] El consentimiento informado es ético y legal.
- [ ] El pre‑registro está completo y accesible.

---
