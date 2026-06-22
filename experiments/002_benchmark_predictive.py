"""
benchmark_predictive.py - Benchmark de la Capa Predictiva del GCD v2.0

Este script genera datos sintéticos, entrena los modelos predictivos,
y evalúa su precisión utilizando métricas estándar.
Los resultados se imprimen en consola y se guardan en un archivo de reporte.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    roc_auc_score, f1_score, precision_score, recall_score,
    mean_absolute_error, mean_squared_error, r2_score,
    confusion_matrix, classification_report
)
from scipy.stats import spearmanr
import json
from datetime import datetime
import os
import sys

# Importar la capa predictiva
from predictors import PredictiveLayer, VARIABLES_PSICO

# ----------------------------------------------------------------------
# 1. Generación de datos sintéticos
# ----------------------------------------------------------------------
def generate_synthetic_data(n_students: int = 1000, seed: int = 42) -> pd.DataFrame:
    """
    Genera un DataFrame sintético con variables psicocognitivas y
    los cuatro objetivos de predicción.
    """
    np.random.seed(seed)
    
    # Variables psicocognitivas (distribuciones uniformes con correlaciones inducidas)
    # Persistencia y motivación correlacionadas positivamente, fatiga negativamente
    persistencia = np.random.uniform(0.1, 1.0, n_students)
    motivacion = 0.3 + 0.5 * persistencia + 0.2 * np.random.normal(0, 1, n_students)
    motivacion = np.clip(motivacion, 0, 1)
    atencion = np.random.uniform(0.3, 1.0, n_students)
    metacognicion = 0.2 + 0.6 * atencion + 0.2 * np.random.normal(0, 1, n_students)
    metacognicion = np.clip(metacognicion, 0, 1)
    flexibilidad = np.random.uniform(0.2, 1.0, n_students)
    rendimiento = 0.1 + 0.4 * atencion + 0.3 * metacognicion + 0.2 * np.random.normal(0, 1, n_students)
    rendimiento = np.clip(rendimiento, 0, 1)
    engagement = 0.2 + 0.3 * motivacion + 0.3 * persistencia + 0.2 * np.random.normal(0, 1, n_students)
    engagement = np.clip(engagement, 0, 1)
    fatiga = 0.1 + 0.3 * (1 - persistencia) + 0.2 * np.random.normal(0, 1, n_students)
    fatiga = np.clip(fatiga, 0, 0.9)
    aciertos_previos = np.random.poisson(lam=10, size=n_students) + 5
    aciertos_previos = np.clip(aciertos_previos, 0, 30)
    progresion = 0.2 + 0.5 * persistencia + 0.3 * flexibilidad + 0.2 * np.random.normal(0, 1, n_students)
    progresion = np.clip(progresion, 0, 1)
    
    data = pd.DataFrame({
        'atencion': atencion,
        'motivacion': motivacion,
        'persistencia': persistencia,
        'metacognicion': metacognicion,
        'flexibilidad_cognitiva': flexibilidad,
        'rendimiento': rendimiento,
        'engagement': engagement,
        'fatiga': fatiga,
        'aciertos_previos': aciertos_previos,
        'progresion_historica': progresion
    })
    
    # Generar objetivos con relaciones no lineales y ruido
    # Dropout (binario): baja persistencia, alta fatiga, bajo rendimiento
    logit_dropout = -1.5 - 2.5 * persistencia + 1.8 * fatiga - 1.2 * rendimiento + 0.5 * (1 - engagement)
    prob_dropout = 1 / (1 + np.exp(-logit_dropout))
    dropout = (prob_dropout > 0.5).astype(int)
    
    # Comprensión (0-1): depende de atención, metacognición y aciertos
    comprehension = 0.2 + 0.35 * atencion + 0.25 * metacognicion + 0.15 * (aciertos_previos / 30) + 0.1 * np.random.normal(0, 1, n_students)
    comprehension = np.clip(comprehension, 0, 1)
    
    # Persistencia futura (0-1): depende de persistencia histórica, motivación, fatiga
    persistence_future = 0.1 + 0.5 * persistencia + 0.25 * motivacion - 0.2 * fatiga + 0.1 * np.random.normal(0, 1, n_students)
    persistence_future = np.clip(persistence_future, 0, 1)
    
    # Learning rate (positivo): depende de progresión y flexibilidad
    learning_rate = 0.1 + 0.4 * progresion + 0.35 * flexibilidad + 0.05 * np.random.normal(0, 1, n_students)
    learning_rate = np.maximum(0, learning_rate)
    
    data['dropout'] = dropout
    data['comprehension'] = comprehension
    data['persistence'] = persistence_future
    data['learning_rate'] = learning_rate
    
    return data


# ----------------------------------------------------------------------
# 2. Funciones de evaluación
# ----------------------------------------------------------------------
def evaluate_classification(y_true, y_pred_proba, threshold=0.5):
    """Evalúa un clasificador binario."""
    y_pred = (y_pred_proba >= threshold).astype(int)
    metrics = {
        'auc_roc': roc_auc_score(y_true, y_pred_proba),
        'f1': f1_score(y_true, y_pred),
        'precision': precision_score(y_true, y_pred),
        'recall': recall_score(y_true, y_pred),
        'accuracy': np.mean(y_true == y_pred),
        'confusion_matrix': confusion_matrix(y_true, y_pred).tolist()
    }
    return metrics

def evaluate_regression(y_true, y_pred):
    """Evalúa un modelo de regresión."""
    metrics = {
        'mae': mean_absolute_error(y_true, y_pred),
        'rmse': np.sqrt(mean_squared_error(y_true, y_pred)),
        'r2': r2_score(y_true, y_pred),
        'spearman_corr': spearmanr(y_true, y_pred)[0]
    }
    return metrics


# ----------------------------------------------------------------------
# 3. Benchmark principal
# ----------------------------------------------------------------------
def run_benchmark(output_dir: str = "./benchmark_results"):
    """
    Ejecuta el benchmark completo: genera datos, entrena modelos,
    evalúa y guarda reporte.
    """
    print("=" * 60)
    print("Benchmark de la Capa Predictiva del GCD v2.0")
    print("=" * 60)
    
    # 1. Generar datos
    print("\n[1] Generando datos sintéticos...")
    data = generate_synthetic_data(n_students=2000, seed=42)
    print(f"    Datos generados: {len(data)} registros.")
    
    # Dividir en entrenamiento (70%) y prueba (30%)
    train_data, test_data = train_test_split(data, test_size=0.3, random_state=42)
    print(f"    Entrenamiento: {len(train_data)}, Prueba: {len(test_data)}")
    
    # 2. Entrenar la capa predictiva
    print("\n[2] Entrenando modelos predictivos...")
    layer = PredictiveLayer()
    target_cols = {
        'dropout': 'dropout',
        'comprehension': 'comprehension',
        'persistence': 'persistence',
        'learning_rate': 'learning_rate'
    }
    layer.fit(train_data, target_cols)
    
    # Guardar modelos (opcional)
    layer.save_models(prefix="gcd_benchmark")
    
    # 3. Evaluar en prueba
    print("\n[3] Evaluando en conjunto de prueba...")
    X_test = test_data[VARIABLES_PSICO]
    y_test = test_data[['dropout', 'comprehension', 'persistence', 'learning_rate']]
    
    # Predicciones
    pred_dropout_proba = layer.dropout_model.predict_proba(X_test)[:, 1]
    pred_comprehension = np.clip(layer.comprehension_model.predict(X_test), 0, 1)
    pred_persistence = np.clip(layer.persistence_model.predict(X_test), 0, 1)
    pred_learning_rate = np.maximum(0, layer.learning_rate_model.predict(X_test))
    
    # 4. Calcular métricas
    print("\n[4] Calculando métricas...")
    results = {}
    
    # Dropout
    results['dropout'] = evaluate_classification(y_test['dropout'], pred_dropout_proba)
    print(f"  Dropout AUC-ROC: {results['dropout']['auc_roc']:.4f}, F1: {results['dropout']['f1']:.4f}")
    
    # Comprensión
    results['comprehension'] = evaluate_regression(y_test['comprehension'], pred_comprehension)
    print(f"  Comprensión MAE: {results['comprehension']['mae']:.4f}, R2: {results['comprehension']['r2']:.4f}")
    
    # Persistencia
    results['persistence'] = evaluate_regression(y_test['persistence'], pred_persistence)
    print(f"  Persistencia MAE: {results['persistence']['mae']:.4f}, R2: {results['persistence']['r2']:.4f}")
    
    # Learning Rate
    results['learning_rate'] = evaluate_regression(y_test['learning_rate'], pred_learning_rate)
    print(f"  Learning Rate MAE: {results['learning_rate']['mae']:.4f}, R2: {results['learning_rate']['r2']:.4f}")
    
    # 5. Guardar reporte
    print("\n[5] Guardando reporte...")
    os.makedirs(output_dir, exist_ok=True)
    report = {
        'timestamp': datetime.now().isoformat(),
        'dataset_size': len(data),
        'train_size': len(train_data),
        'test_size': len(test_data),
        'metrics': results,
        'model_params': {
            'dropout': str(layer.dropout_model),
            'comprehension': str(layer.comprehension_model),
            'persistence': str(layer.persistence_model),
            'learning_rate': str(layer.learning_rate_model)
        }
    }
    
    report_path = os.path.join(output_dir, f"benchmark_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    print(f"    Reporte guardado en: {report_path}")
    
    # También guardar un resumen en texto
    summary_path = os.path.join(output_dir, "benchmark_summary.txt")
    with open(summary_path, 'w') as f:
        f.write("RESUMEN DEL BENCHMARK DE LA CAPA PREDICTIVA DEL GCD\n")
        f.write("=" * 50 + "\n")
        f.write(f"Fecha: {report['timestamp']}\n")
        f.write(f"Tamaño del dataset: {report['dataset_size']}\n")
        f.write(f"Train/Test: {report['train_size']}/{report['test_size']}\n\n")
        for target, metrics in results.items():
            f.write(f"--- {target.upper()} ---\n")
            for metric, value in metrics.items():
                if metric == 'confusion_matrix':
                    f.write(f"  {metric}: {value}\n")
                else:
                    f.write(f"  {metric}: {value:.4f}\n")
            f.write("\n")
    print(f"    Resumen guardado en: {summary_path}")
    
    print("\nBenchmark completado exitosamente.")
    return results


# ----------------------------------------------------------------------
# 4. Ejecución directa
# ----------------------------------------------------------------------
if __name__ == "__main__":
    # Si se pasa un argumento, se usa como directorio de salida
    out_dir = sys.argv[1] if len(sys.argv) > 1 else "./benchmark_results"
    run_benchmark(output_dir=out_dir)
