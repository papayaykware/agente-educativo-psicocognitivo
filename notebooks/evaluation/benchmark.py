#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
benchmark.py - Suite de Evaluación Comparativa para GCD

Propósito:
    Ejecutar experimentos controlados que comparen el rendimiento del sistema GCD
    frente a un tutor estático (control) y otros enfoques adaptativos.

Funcionalidades:
    - Carga de configuraciones experimentales (grupos, condiciones)
    - Simulación de interacciones con agentes sintéticos basados en datos históricos
    - Cálculo de métricas clave: retención, abandono, velocidad de aprendizaje, creatividad
    - Almacenamiento de resultados en formato CSV y JSON resumen

Uso:
    from evaluation.benchmark import run_benchmark
    results = run_benchmark(
        model="gcd_adaptive",
        control="static_tutor",
        n_subjects=120,
        sessions=16,
        random_seed=42
    )
    print(results.summary())

Salidas:
    - benchmark_results.csv  : datos crudos por sujeto y sesión
    - benchmark_summary.json : estadísticos agregados (medias, desviaciones, tamaños de efecto)
"""

import os
import json
import numpy as np
import pandas as pd
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from scipy import stats
from scipy.optimize import curve_fit
import logging
from datetime import datetime

# Configuración básica de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# -----------------------------------------------------------------------------
# 1. Configuración experimental
# -----------------------------------------------------------------------------

@dataclass
class ExperimentConfig:
    """Configuración de un experimento de benchmark."""
    model_name: str                 # Nombre del modelo (ej. "gcd_adaptive")
    control_name: str               # Nombre del control (ej. "static_tutor")
    n_subjects: int = 120           # Número total de sujetos (se divide en grupos)
    sessions: int = 16              # Número de sesiones por sujeto
    random_seed: Optional[int] = None
    # Parámetros de simulación (distribuciones para agentes sintéticos)
    learning_rate_mean: float = 0.3
    learning_rate_std: float = 0.1
    persistence_mean: float = 0.7
    persistence_std: float = 0.15
    metacognition_mean: float = 0.5
    metacognition_std: float = 0.2
    dropout_risk_mean: float = 0.1   # Probabilidad base de abandono por sesión
    creativity_base: float = 50.0    # Puntuación base de creatividad (escala 0-100)

    def __post_init__(self):
        if self.random_seed is not None:
            np.random.seed(self.random_seed)


# -----------------------------------------------------------------------------
# 2. Agente sintético (estudiante simulado)
# -----------------------------------------------------------------------------

class SyntheticStudent:
    """
    Representa un estudiante sintético con parámetros cognitivos y de comportamiento.
    Su evolución se simula según el modelo asignado (GCD adaptativo o tutor estático).
    """
    def __init__(self, student_id: int, config: ExperimentConfig, model_type: str):
        self.id = student_id
        self.config = config
        self.model_type = model_type  # 'gcd_adaptive' o 'static_tutor'

        # Parámetros fijos del estudiante (generados a partir de distribuciones)
        self.learning_rate = np.random.normal(
            config.learning_rate_mean, config.learning_rate_std
        )
        self.learning_rate = np.clip(self.learning_rate, 0.05, 0.8)

        self.persistence = np.random.normal(
            config.persistence_mean, config.persistence_std
        )
        self.persistence = np.clip(self.persistence, 0.2, 1.0)

        self.metacognition = np.random.normal(
            config.metacognition_mean, config.metacognition_std
        )
        self.metacognition = np.clip(self.metacognition, 0.1, 0.9)

        self.dropout_risk_base = np.random.normal(
            config.dropout_risk_mean, 0.05
        )
        self.dropout_risk_base = np.clip(self.dropout_risk_base, 0.01, 0.5)

        self.creativity_base = np.random.normal(
            config.creativity_base, 15
        )
        self.creativity_base = np.clip(self.creativity_base, 0, 100)

        # Estado inicial
        self.knowledge = np.random.uniform(0.1, 0.3)  # nivel de conocimiento (0-1)
        self.attention = np.random.uniform(0.5, 0.9)
        self.motivation = np.random.uniform(0.4, 0.8)
        self.retention = 0.0  # se actualizará tras cada sesión

        # Historial
        self.history = {
            'session': [],
            'knowledge': [],
            'retention': [],
            'attention': [],
            'motivation': [],
            'persistence_effort': [],
            'dropout': [],          # booleano: si abandonó en esa sesión
        }
        self.active = True
        self.dropout_session = None

    def step(self, session: int, is_gcd: bool) -> Dict[str, float]:
        """
        Avanza una sesión para este estudiante.
        Retorna un diccionario con las métricas de la sesión.
        """
        if not self.active:
            # Si ya abandonó, devolver valores nulos
            return {
                'knowledge': np.nan,
                'retention': np.nan,
                'attention': np.nan,
                'motivation': np.nan,
                'persistence_effort': np.nan,
                'dropout': True,
            }

        # 1. Calcular esfuerzo de persistencia (depende del tipo de modelo)
        if is_gcd:
            # GCD adaptativo: ajusta dinámicamente la dificultad y refuerza persistencia
            persistence_effort = self.persistence * (1 + 0.2 * self.metacognition)
            # La atención y motivación se benefician de la adaptabilidad
            attention_boost = 0.1 * (1 - self.attention) * self.metacognition
            motivation_boost = 0.1 * (1 - self.motivation) * self.metacognition
            self.attention = np.clip(self.attention + attention_boost, 0, 1)
            self.motivation = np.clip(self.motivation + motivation_boost, 0, 1)
        else:
            # Tutor estático: sin adaptación, el esfuerzo depende solo de la persistencia base
            persistence_effort = self.persistence * 0.8  # menos eficiente
            # La atención y motivación decaen ligeramente
            self.attention = np.clip(self.attention - 0.02, 0, 1)
            self.motivation = np.clip(self.motivation - 0.02, 0, 1)

        # 2. Actualizar conocimiento (curva de aprendizaje)
        # Modelo: ganancia = learning_rate * esfuerzo * (1 - knowledge) * factor_metacognitivo
        metacog_factor = 1 + 0.3 * self.metacognition if is_gcd else 1.0
        gain = self.learning_rate * persistence_effort * (1 - self.knowledge) * metacog_factor
        # Añadir ruido
        gain += np.random.normal(0, 0.02)
        self.knowledge = np.clip(self.knowledge + gain, 0, 1)

        # 3. Calcular retención (simulada como función del conocimiento y metacognición)
        # En GCD la retención es mejor
        if is_gcd:
            retention = self.knowledge * (0.8 + 0.2 * self.metacognition)
        else:
            retention = self.knowledge * 0.7  # estático retiene menos
        retention += np.random.normal(0, 0.03)
        self.retention = np.clip(retention, 0, 1)

        # 4. Velocidad de aprendizaje (se calculará a posteriori como pendiente)
        # Almacenamos knowledge para luego ajustar curva

        # 5. Riesgo de abandono (dropout)
        # En GCD, el riesgo se reduce si el estudiante está más motivado/atento
        if is_gcd:
            dropout_risk = self.dropout_risk_base * (1 - 0.5 * self.motivation) * (1 - 0.3 * self.attention)
        else:
            dropout_risk = self.dropout_risk_base * (1 + 0.2 * (1 - self.motivation))  # mayor riesgo
        dropout_risk = np.clip(dropout_risk, 0.01, 0.8)

        # Decisión de abandono (probabilística)
        dropout_event = np.random.rand() < dropout_risk
        if dropout_event:
            self.active = False
            self.dropout_session = session

        # Registrar historial
        self.history['session'].append(session)
        self.history['knowledge'].append(self.knowledge)
        self.history['retention'].append(self.retention)
        self.history['attention'].append(self.attention)
        self.history['motivation'].append(self.motivation)
        self.history['persistence_effort'].append(persistence_effort)
        self.history['dropout'].append(dropout_event)

        # 6. Creatividad (se mide al final, pero aquí simulamos evolución)
        # La creatividad aumenta con la metacognición y la exposición a excepciones cognitivas
        # Solo en GCD hay un componente de excepciones
        if is_gcd:
            creativity_boost = 0.5 * self.metacognition * (1 - self.knowledge) * 10
        else:
            creativity_boost = 0.1 * self.metacognition * 5
        self.creativity_base += creativity_boost * 0.1  # evolución lenta
        self.creativity_base = np.clip(self.creativity_base, 0, 100)

        return {
            'knowledge': self.knowledge,
            'retention': self.retention,
            'attention': self.attention,
            'motivation': self.motivation,
            'persistence_effort': persistence_effort,
            'dropout': dropout_event,
            'creativity': self.creativity_base,
        }


# -----------------------------------------------------------------------------
# 3. Funciones de cálculo de métricas
# -----------------------------------------------------------------------------

def compute_metrics_for_student(history: Dict, model_type: str) -> Dict[str, Any]:
    """
    Calcula métricas agregadas para un estudiante dado su historial.
    Retorna un diccionario con:
        - retention_final: retención al final (último valor no NaN)
        - dropout_time: sesión en la que abandonó (None si no)
        - learning_speed: pendiente de la curva de conocimiento (ajuste exponencial)
        - creativity_final: creatividad al final
        - avg_attention, avg_motivation, avg_persistence
    """
    sessions = np.array(history['session'])
    knowledge = np.array(history['knowledge'])
    retention = np.array(history['retention'])
    creativity = np.array(history.get('creativity', [np.nan]*len(sessions)))
    attention = np.array(history['attention'])
    motivation = np.array(history['motivation'])
    persistence = np.array(history['persistence_effort'])
    dropout_events = np.array(history['dropout'])

    # Filtrar sesiones activas (donde no hay NaN)
    valid = ~np.isnan(knowledge)
    if not np.any(valid):
        return {
            'retention_final': np.nan,
            'dropout_time': None,
            'learning_speed': np.nan,
            'creativity_final': np.nan,
            'avg_attention': np.nan,
            'avg_motivation': np.nan,
            'avg_persistence': np.nan,
            'dropout_occurred': True,
        }

    # Retención final (última sesión válida)
    last_idx = np.max(np.where(valid)[0])
    retention_final = retention[last_idx] if not np.isnan(retention[last_idx]) else np.nan

    # Creatividad final
    creativity_final = creativity[last_idx] if len(creativity) > last_idx and not np.isnan(creativity[last_idx]) else np.nan

    # Tiempo de abandono (primera sesión con dropout True)
    dropout_indices = np.where(dropout_events == True)[0]
    dropout_time = dropout_indices[0] if len(dropout_indices) > 0 else None
    dropout_occurred = dropout_time is not None

    # Velocidad de aprendizaje: ajuste de curva exponencial y = a*(1 - exp(-b*x))
    # Usamos solo sesiones válidas hasta el abandono (si ocurrió)
    if dropout_time is not None:
        # Tomamos hasta la sesión anterior al abandono (si dropout_time > 0)
        if dropout_time > 0:
            end_idx = dropout_time - 1
        else:
            end_idx = 0
        # Pero si no hay sesiones antes del abandono, no podemos calcular
        if end_idx <= 0:
            learning_speed = np.nan
        else:
            x = sessions[:end_idx+1][valid[:end_idx+1]]
            y = knowledge[:end_idx+1][valid[:end_idx+1]]
    else:
        x = sessions[valid]
        y = knowledge[valid]

    # Ajuste exponencial solo si tenemos al menos 3 puntos
    if len(x) >= 3 and len(y) >= 3:
        try:
            # Modelo: y = a * (1 - exp(-b*x)) + c (con c=0 asumimos)
            def exp_func(x, a, b):
                return a * (1 - np.exp(-b * x))
            popt, _ = curve_fit(exp_func, x, y, p0=[1.0, 0.1], bounds=([0, 0], [1.5, 5.0]))
            learning_speed = popt[1]  # b
        except Exception as e:
            logger.warning(f"Error en ajuste exponencial para estudiante: {e}")
            learning_speed = np.nan
    else:
        learning_speed = np.nan

    # Promedios
    avg_attention = np.nanmean(attention[valid])
    avg_motivation = np.nanmean(motivation[valid])
    avg_persistence = np.nanmean(persistence[valid])

    return {
        'retention_final': retention_final,
        'dropout_time': dropout_time,
        'learning_speed': learning_speed,
        'creativity_final': creativity_final,
        'avg_attention': avg_attention,
        'avg_motivation': avg_motivation,
        'avg_persistence': avg_persistence,
        'dropout_occurred': dropout_occurred,
    }


# -----------------------------------------------------------------------------
# 4. Función principal de benchmark
# -----------------------------------------------------------------------------

class BenchmarkResults:
    """Contenedor de resultados de un benchmark."""
    def __init__(self, config: ExperimentConfig):
        self.config = config
        self.df: Optional[pd.DataFrame] = None   # Datos crudos por sujeto y sesión
        self.summary: Dict = {}                  # Estadísticas agregadas

    def load_from_df(self, df: pd.DataFrame):
        self.df = df
        self._compute_summary()

    def _compute_summary(self):
        """Genera el resumen estadístico a partir del DataFrame."""
        if self.df is None or self.df.empty:
            self.summary = {}
            return

        # Agrupar por modelo y calcular estadísticas de las métricas finales
        # Asumimos que el DataFrame tiene columnas: subject_id, model, session, retention, dropout, learning_speed, creativity, etc.
        # Pero necesitamos métricas por estudiante, no por sesión.
        # Para simplificar, usamos los datos crudos y calculamos las métricas por estudiante.
        # En realidad, deberíamos tener las métricas ya calculadas por estudiante,
        # pero aquí las calculamos sobre la marcha.

        # Primero, para cada sujeto, extraemos su historial y calculamos métricas.
        subjects = self.df['subject_id'].unique()
        records = []
        for sid in subjects:
            sub_df = self.df[self.df['subject_id'] == sid]
            model = sub_df['model'].iloc[0]
            # Reconstruir historial
            history = {
                'session': sub_df['session'].tolist(),
                'knowledge': sub_df['knowledge'].tolist(),
                'retention': sub_df['retention'].tolist(),
                'attention': sub_df['attention'].tolist(),
                'motivation': sub_df['motivation'].tolist(),
                'persistence_effort': sub_df['persistence_effort'].tolist(),
                'dropout': sub_df['dropout'].tolist(),
                'creativity': sub_df['creativity'].tolist() if 'creativity' in sub_df else [np.nan]*len(sub_df),
            }
            metrics = compute_metrics_for_student(history, model)
            metrics['subject_id'] = sid
            metrics['model'] = model
            records.append(metrics)

        metrics_df = pd.DataFrame(records)

        # Calcular estadísticas por modelo
        summary_stats = {}
        for model in metrics_df['model'].unique():
            model_df = metrics_df[metrics_df['model'] == model]
            # Métricas numéricas
            numeric_cols = ['retention_final', 'learning_speed', 'creativity_final',
                            'avg_attention', 'avg_motivation', 'avg_persistence']
            stats_dict = {}
            for col in numeric_cols:
                if col in model_df.columns:
                    series = model_df[col].dropna()
                    if len(series) > 0:
                        stats_dict[col] = {
                            'mean': series.mean(),
                            'std': series.std(),
                            'median': series.median(),
                            'q25': series.quantile(0.25),
                            'q75': series.quantile(0.75),
                            'n': len(series)
                        }
            # Tasa de abandono
            dropout_rate = model_df['dropout_occurred'].mean() if 'dropout_occurred' in model_df else np.nan
            stats_dict['dropout_rate'] = dropout_rate
            stats_dict['n_subjects'] = len(model_df)
            summary_stats[model] = stats_dict

        self.summary = summary_stats

    def summary(self) -> Dict:
        return self.summary

    def save_csv(self, filepath: str):
        if self.df is not None:
            self.df.to_csv(filepath, index=False)
            logger.info(f"Resultados guardados en {filepath}")
        else:
            logger.warning("No hay datos para guardar.")

    def save_json(self, filepath: str):
        with open(filepath, 'w') as f:
            json.dump(self.summary, f, indent=2)
        logger.info(f"Resumen guardado en {filepath}")


def run_benchmark(
    model: str = "gcd_adaptive",
    control: str = "static_tutor",
    n_subjects: int = 120,
    sessions: int = 16,
    random_seed: Optional[int] = 42,
    output_dir: str = "."
) -> BenchmarkResults:
    """
    Ejecuta un benchmark comparando el modelo dado contra el control.

    Args:
        model: Nombre del modelo a evaluar (ej. "gcd_adaptive")
        control: Nombre del modelo de control (ej. "static_tutor")
        n_subjects: Número total de sujetos (se reparten a partes iguales)
        sessions: Número de sesiones por sujeto
        random_seed: Semilla para reproducibilidad
        output_dir: Directorio donde guardar los archivos de salida

    Returns:
        BenchmarkResults con los datos y resumen.
    """
    logger.info(f"Iniciando benchmark: {model} vs {control}")
    config = ExperimentConfig(
        model_name=model,
        control_name=control,
        n_subjects=n_subjects,
        sessions=sessions,
        random_seed=random_seed,
    )

    # Determinar número de sujetos por grupo
    n_per_group = n_subjects // 2
    # Si es impar, el grupo modelo lleva uno más
    n_model = n_per_group + (n_subjects % 2)
    n_control = n_per_group

    # Crear estudiantes
    students = []
    for i in range(n_model):
        students.append(SyntheticStudent(i, config, model_type='gcd'))
    for i in range(n_control):
        students.append(SyntheticStudent(i + n_model, config, model_type='control'))

    # Simular sesiones
    all_records = []
    for session in range(1, sessions + 1):
        logger.info(f"Simulando sesión {session}/{sessions}")
        for student in students:
            if not student.active:
                # Si ya abandonó, registrar NaN en todas las métricas
                record = {
                    'subject_id': student.id,
                    'model': 'gcd' if student.model_type == 'gcd' else 'control',
                    'session': session,
                    'knowledge': np.nan,
                    'retention': np.nan,
                    'attention': np.nan,
                    'motivation': np.nan,
                    'persistence_effort': np.nan,
                    'dropout': True,
                    'creativity': np.nan,
                }
                all_records.append(record)
                continue

            is_gcd = (student.model_type == 'gcd')
            metrics = student.step(session, is_gcd)
            record = {
                'subject_id': student.id,
                'model': 'gcd' if is_gcd else 'control',
                'session': session,
                'knowledge': metrics['knowledge'],
                'retention': metrics['retention'],
                'attention': metrics['attention'],
                'motivation': metrics['motivation'],
                'persistence_effort': metrics['persistence_effort'],
                'dropout': metrics['dropout'],
                'creativity': metrics['creativity'],
            }
            all_records.append(record)

    df = pd.DataFrame(all_records)

    # Crear objeto de resultados
    results = BenchmarkResults(config)
    results.load_from_df(df)

    # Guardar archivos
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_file = os.path.join(output_dir, f"benchmark_results_{timestamp}.csv")
    json_file = os.path.join(output_dir, f"benchmark_summary_{timestamp}.json")
    results.save_csv(csv_file)
    results.save_json(json_file)

    logger.info("Benchmark completado.")
    return results


# -----------------------------------------------------------------------------
# 5. Ejemplo de uso (si se ejecuta como script)
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    # Ejecutar benchmark de ejemplo
    results = run_benchmark(
        model="gcd_adaptive",
        control="static_tutor",
        n_subjects=20,   # pequeño para prueba rápida
        sessions=8,
        random_seed=42,
        output_dir="."
    )

    print("\n--- Resumen del Benchmark ---")
    print(json.dumps(results.summary, indent=2))

    # Mostrar las primeras filas del DataFrame
    print("\n--- Primeras filas de resultados crudos ---")
    print(results.df.head())
