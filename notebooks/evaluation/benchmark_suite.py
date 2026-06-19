#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
benchmark_suite.py - Pipeline de Evaluación Automatizado

Propósito:
    Orquestar la ejecución completa de los scripts de evaluación:
        1. Generar datos simulados (benchmark.py)
        2. Generar reporte visual (metrics_report.py)
        3. Realizar análisis estadístico (statistical_analysis.py)
    Incluye validación cruzada y pruebas de integración para verificar
    la consistencia del pipeline.

Uso:
    python evaluation/benchmark_suite.py --subjects 120 --sessions 16 --output ./results

    O desde Python:
        from evaluation.benchmark_suite import run_full_suite
        run_full_suite(n_subjects=120, sessions=16, output_dir="./results")
"""

import os
import sys
import json
import subprocess
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Optional, Dict, Any
import logging
from pathlib import Path

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Añadir el directorio actual al path para importar módulos locales
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar módulos locales
try:
    from evaluation.benchmark import run_benchmark, ExperimentConfig
    from evaluation.metrics_report import generate_report
    from evaluation.statistical_analysis import run_analysis
except ImportError as e:
    logger.error(f"Error al importar módulos de evaluación: {e}")
    logger.error("Asegúrese de que los archivos benchmark.py, metrics_report.py y statistical_analysis.py están en el directorio 'evaluation/'.")
    sys.exit(1)


# =============================================================================
# 1. Validación Cruzada (Cross-Validation)
# =============================================================================

def cross_validate_models(df_long: pd.DataFrame, subject_metrics: pd.DataFrame,
                          n_folds: int = 5) -> Dict[str, Any]:
    """
    Realiza validación cruzada simple para evaluar la estabilidad de los modelos.
    Actualmente solo implementa una partición aleatoria y comparación de métricas
    en conjuntos de entrenamiento y prueba.

    Retorna un diccionario con estadísticas de estabilidad.
    """
    logger.info(f"Realizando validación cruzada con {n_folds} folds...")
    from sklearn.model_selection import KFold
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import accuracy_score, roc_auc_score
    from sklearn.preprocessing import StandardScaler

    # Preparar datos para clasificación de abandono (si existe)
    if 'dropout_occurred' not in subject_metrics.columns:
        logger.warning("No se encontró 'dropout_occurred' en subject_metrics. Omitiendo CV.")
        return {}

    # Seleccionar predictores disponibles
    predictors = ['avg_persistence', 'retention_final', 'avg_attention', 'avg_motivation']
    available = [p for p in predictors if p in subject_metrics.columns]
    if not available:
        logger.warning("No hay predictores para CV. Omitiendo.")
        return {}

    data = subject_metrics[['dropout_occurred'] + available].dropna()
    X = data[available].values
    y = data['dropout_occurred'].astype(int).values

    if len(X) < n_folds:
        logger.warning("Demasiados folds para el tamaño de datos. Reduciendo a 3.")
        n_folds = min(3, len(X))

    kf = KFold(n_splits=n_folds, shuffle=True, random_state=42)
    accuracies = []
    aucs = []

    for train_idx, test_idx in kf.split(X):
        X_train, X_test = X[train_idx], X[test_idx]
        y_train, y_test = y[train_idx], y[test_idx]

        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        clf = LogisticRegression(random_state=42, max_iter=1000)
        clf.fit(X_train_scaled, y_train)
        y_pred = clf.predict(X_test_scaled)
        y_prob = clf.predict_proba(X_test_scaled)[:, 1]

        accuracies.append(accuracy_score(y_test, y_pred))
        aucs.append(roc_auc_score(y_test, y_prob))

    cv_results = {
        'accuracy_mean': np.mean(accuracies),
        'accuracy_std': np.std(accuracies),
        'auc_mean': np.mean(aucs),
        'auc_std': np.std(aucs),
    }
    logger.info(f"CV resultados: Accuracy = {cv_results['accuracy_mean']:.3f} ± {cv_results['accuracy_std']:.3f}, "
                f"AUC = {cv_results['auc_mean']:.3f} ± {cv_results['auc_std']:.3f}")
    return cv_results


# =============================================================================
# 2. Función Principal del Suite
# =============================================================================

def run_full_suite(
    n_subjects: int = 120,
    sessions: int = 16,
    output_dir: str = "./results",
    random_seed: int = 42,
    run_benchmark: bool = True,
    run_report: bool = True,
    run_statistics: bool = True,
    cross_validate: bool = True,
    data_file: Optional[str] = None
) -> Dict[str, Any]:
    """
    Ejecuta el pipeline completo de evaluación.

    Args:
        n_subjects: Número de sujetos para la simulación.
        sessions: Número de sesiones por sujeto.
        output_dir: Directorio donde guardar todos los resultados.
        random_seed: Semilla para reproducibilidad.
        run_benchmark: Si se debe ejecutar la generación de datos.
        run_report: Si se debe generar el reporte HTML.
        run_statistics: Si se debe ejecutar el análisis estadístico.
        cross_validate: Si se debe realizar validación cruzada.
        data_file: Ruta a un archivo CSV existente (opcional). Si se proporciona,
                   se usará en lugar de generar nuevos datos.

    Returns:
        Diccionario con las rutas de los archivos generados y resultados del CV.
    """
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    logger.info(f"Iniciando Benchmark Suite (seed={random_seed})")

    results = {
        'data_file': None,
        'report_file': None,
        'stats_dir': None,
        'cv_results': None
    }

    # 1. Generar datos si no se proporciona un archivo
    if data_file is None and run_benchmark:
        logger.info("Ejecutando benchmark para generar datos simulados...")
        # Ejecutar benchmark (esto genera archivos CSV y JSON en el directorio de salida)
        try:
            from evaluation.benchmark import run_benchmark
            bench_results = run_benchmark(
                model="gcd_adaptive",
                control="static_tutor",
                n_subjects=n_subjects,
                sessions=sessions,
                random_seed=random_seed,
                output_dir=output_dir
            )
            # Buscar el archivo CSV generado
            csv_files = [f for f in os.listdir(output_dir) if f.startswith("benchmark_results_") and f.endswith(".csv")]
            if not csv_files:
                raise FileNotFoundError("No se encontró archivo CSV de benchmark.")
            # Ordenar por fecha (más reciente primero)
            csv_files.sort(reverse=True)
            data_file = os.path.join(output_dir, csv_files[0])
            results['data_file'] = data_file
            logger.info(f"Datos generados en: {data_file}")
        except Exception as e:
            logger.error(f"Error al ejecutar benchmark: {e}")
            raise

    elif data_file is not None:
        if not os.path.exists(data_file):
            raise FileNotFoundError(f"Archivo de datos no encontrado: {data_file}")
        results['data_file'] = data_file
        logger.info(f"Usando datos existentes: {data_file}")
    else:
        raise ValueError("Debe proporcionar data_file o establecer run_benchmark=True")

    # 2. Generar reporte HTML
    if run_report:
        logger.info("Generando reporte de métricas...")
        report_file = os.path.join(output_dir, f"report_{timestamp}.html")
        try:
            generate_report(
                data=data_file,
                output=report_file,
                include_plots=True,
                title=f"Reporte de Benchmark GCD - {timestamp}"
            )
            results['report_file'] = report_file
            logger.info(f"Reporte generado: {report_file}")
        except Exception as e:
            logger.error(f"Error al generar reporte: {e}")
            raise

    # 3. Análisis estadístico
    if run_statistics:
        logger.info("Ejecutando análisis estadístico...")
        stats_dir = os.path.join(output_dir, f"stats_{timestamp}")
        os.makedirs(stats_dir, exist_ok=True)
        try:
            # run_analysis genera archivos en el directorio stats_dir
            from evaluation.statistical_analysis import run_analysis
            stats_results = run_analysis(data_file, stats_dir)
            results['stats_dir'] = stats_dir
            logger.info(f"Análisis estadístico completado en: {stats_dir}")
        except Exception as e:
            logger.error(f"Error en análisis estadístico: {e}")
            raise

    # 4. Validación cruzada (usando los datos generados)
    if cross_validate:
        logger.info("Realizando validación cruzada...")
        try:
            df_long = pd.read_csv(data_file)
            # Necesitamos subject_metrics; la función de statistical_analysis la calcula
            # pero podemos importar la función de metrics_report
            from evaluation.metrics_report import compute_subject_metrics
            subject_metrics = compute_subject_metrics(df_long)
            cv_res = cross_validate_models(df_long, subject_metrics, n_folds=5)
            results['cv_results'] = cv_res
            # Guardar resultados de CV en JSON
            cv_file = os.path.join(output_dir, f"cv_results_{timestamp}.json")
            with open(cv_file, 'w') as f:
                json.dump(cv_res, f, indent=2)
            logger.info(f"Resultados de CV guardados en: {cv_file}")
        except Exception as e:
            logger.error(f"Error en validación cruzada: {e}")

    # 5. Resumen final
    logger.info("Benchmark Suite completado.")
    logger.info(f"Resultados disponibles en: {output_dir}")
    return results


# =============================================================================
# 3. Script principal (CLI)
# =============================================================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Ejecutar el pipeline completo de evaluación (Benchmark Suite)."
    )
    parser.add_argument(
        "--subjects", type=int, default=120,
        help="Número de sujetos simulados (por defecto 120)."
    )
    parser.add_argument(
        "--sessions", type=int, default=16,
        help="Número de sesiones por sujeto (por defecto 16)."
    )
    parser.add_argument(
        "--output", type=str, default="./results",
        help="Directorio de salida para todos los resultados."
    )
    parser.add_argument(
        "--seed", type=int, default=42,
        help="Semilla aleatoria (por defecto 42)."
    )
    parser.add_argument(
        "--data", type=str, default=None,
        help="Ruta a un archivo CSV existente (opcional). Si se proporciona, no se ejecuta benchmark."
    )
    parser.add_argument(
        "--no-benchmark", action="store_true",
        help="No ejecutar benchmark (usar --data obligatoriamente)."
    )
    parser.add_argument(
        "--no-report", action="store_true",
        help="No generar reporte HTML."
    )
    parser.add_argument(
        "--no-stats", action="store_true",
        help="No ejecutar análisis estadístico."
    )
    parser.add_argument(
        "--no-cv", action="store_true",
        help="No ejecutar validación cruzada."
    )

    args = parser.parse_args()

    # Ejecutar suite
    try:
        results = run_full_suite(
            n_subjects=args.subjects,
            sessions=args.sessions,
            output_dir=args.output,
            random_seed=args.seed,
            run_benchmark=not args.no_benchmark,
            run_report=not args.no_report,
            run_statistics=not args.no_stats,
            cross_validate=not args.no_cv,
            data_file=args.data
        )
        print("\n" + "="*60)
        print("RESUMEN DE EJECUCIÓN")
        print("="*60)
        print(f"Archivo de datos: {results.get('data_file')}")
        print(f"Reporte HTML: {results.get('report_file')}")
        print(f"Directorio de estadísticas: {results.get('stats_dir')}")
        if results.get('cv_results'):
            cv = results['cv_results']
            print(f"CV - Accuracy: {cv['accuracy_mean']:.3f} ± {cv['accuracy_std']:.3f}")
            print(f"CV - AUC: {cv['auc_mean']:.3f} ± {cv['auc_std']:.3f}")
        print("="*60)
    except Exception as e:
        logger.error(f"Error en la ejecución del suite: {e}")
        sys.exit(1)
