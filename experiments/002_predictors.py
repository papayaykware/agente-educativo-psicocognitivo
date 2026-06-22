"""
predictors.py - Capa Predictiva del Gemelo Cognitivo Dinámico (GCD) v2.0

Implementa los cuatro predictores básicos:
- predict_dropout()
- predict_comprehension()
- predict_persistence()
- predict_learning_rate()

Utiliza modelos de scikit-learn entrenados sobre variables psicocognitivas.
La clase PredictiveLayer gestiona el entrenamiento, persistencia y predicción.
"""

import numpy as np
import pandas as pd
from typing import Dict, Optional, Tuple, List, Any
import joblib
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')

# ----------------------------------------------------------------------
# Constantes y mapeos de variables
# ----------------------------------------------------------------------
VARIABLES_PSICO = [
    'atencion', 'motivacion', 'persistencia', 'metacognicion',
    'flexibilidad_cognitiva', 'rendimiento', 'engagement', 'fatiga',
    'aciertos_previos', 'progresion_historica'
]

# Umbrales para clasificación binaria (dropout, etc.)
DROPOUT_THRESHOLD = 0.5


class PredictiveLayer:
    """
    Capa predictiva del GCD. Contiene los cuatro modelos predictivos,
    cada uno con su propio preprocesamiento y pipeline.
    """

    def __init__(self, models_dir: Optional[str] = None):
        """
        Inicializa la capa predictiva.

        Args:
            models_dir: Directorio donde se guardan/cargan los modelos serializados.
                        Si es None, se usará './models' por defecto.
        """
        self.models_dir = models_dir or './models'
        self.dropout_model: Optional[Pipeline] = None
        self.comprehension_model: Optional[Pipeline] = None
        self.persistence_model: Optional[Pipeline] = None
        self.learning_rate_model: Optional[Pipeline] = None
        self._fitted = False

    # ------------------------------------------------------------------
    # Entrenamiento de modelos
    # ------------------------------------------------------------------
    def fit(self, data: pd.DataFrame, target_cols: Dict[str, str]) -> None:
        """
        Entrena los cuatro modelos a partir de un DataFrame con variables
        psicocognitivas y las columnas objetivo.

        Args:
            data: DataFrame con columnas de variables y objetivos.
            target_cols: Diccionario mapeando 'dropout', 'comprehension',
                         'persistence', 'learning_rate' a nombres de columnas
                         en 'data'.
        """
        # Separar características (todas las variables psicocognitivas)
        X = data[VARIABLES_PSICO].copy()

        # Entrenar cada modelo
        self.dropout_model = self._train_dropout(X, data[target_cols['dropout']])
        self.comprehension_model = self._train_comprehension(X, data[target_cols['comprehension']])
        self.persistence_model = self._train_persistence(X, data[target_cols['persistence']])
        self.learning_rate_model = self._train_learning_rate(X, data[target_cols['learning_rate']])

        self._fitted = True
        print("Modelos entrenados correctamente.")

    def _train_dropout(self, X: pd.DataFrame, y: pd.Series) -> Pipeline:
        """Entrena modelo de dropout (clasificación binaria)."""
        # Escalamos y aplicamos regresión logística
        pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('clf', LogisticRegression(class_weight='balanced', random_state=42))
        ])
        pipeline.fit(X, y)
        return pipeline

    def _train_comprehension(self, X: pd.DataFrame, y: pd.Series) -> Pipeline:
        """Entrena modelo de comprensión (regresión, valor 0-1)."""
        pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('reg', LinearRegression())
        ])
        pipeline.fit(X, y)
        return pipeline

    def _train_persistence(self, X: pd.DataFrame, y: pd.Series) -> Pipeline:
        """Entrena modelo de persistencia futura (regresión, valor 0-1)."""
        pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('reg', LinearRegression())
        ])
        pipeline.fit(X, y)
        return pipeline

    def _train_learning_rate(self, X: pd.DataFrame, y: pd.Series) -> Pipeline:
        """Entrena modelo de tasa de aprendizaje (regresión, valor positivo)."""
        pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('reg', LinearRegression())
        ])
        pipeline.fit(X, y)
        return pipeline

    # ------------------------------------------------------------------
    # Predicciones
    # ------------------------------------------------------------------
    def predict_dropout(self, student_data: Dict[str, float]) -> float:
        """
        Predice probabilidad de abandono (0-1).

        Args:
            student_data: Diccionario con variables psicocognitivas.

        Returns:
            Probabilidad de dropout.
        """
        if not self._fitted:
            raise RuntimeError("Modelos no entrenados. Llame a fit() primero.")
        X = self._dict_to_df(student_data)
        proba = self.dropout_model.predict_proba(X)[0, 1]  # probabilidad clase 1
        return float(proba)

    def predict_comprehension(self, student_data: Dict[str, float]) -> float:
        """Predice nivel de comprensión (0-1)."""
        if not self._fitted:
            raise RuntimeError("Modelos no entrenados. Llame a fit() primero.")
        X = self._dict_to_df(student_data)
        pred = self.comprehension_model.predict(X)[0]
        return float(np.clip(pred, 0.0, 1.0))

    def predict_persistence(self, student_data: Dict[str, float]) -> float:
        """Predice persistencia futura (0-1)."""
        if not self._fitted:
            raise RuntimeError("Modelos no entrenados. Llame a fit() primero.")
        X = self._dict_to_df(student_data)
        pred = self.persistence_model.predict(X)[0]
        return float(np.clip(pred, 0.0, 1.0))

    def predict_learning_rate(self, student_data: Dict[str, float]) -> float:
        """Predice tasa de aprendizaje (valor positivo)."""
        if not self._fitted:
            raise RuntimeError("Modelos no entrenados. Llame a fit() primero.")
        X = self._dict_to_df(student_data)
        pred = self.learning_rate_model.predict(X)[0]
        return float(max(0.0, pred))  # no negativo

    # ------------------------------------------------------------------
    # Persistencia (guardar/cargar)
    # ------------------------------------------------------------------
    def save_models(self, prefix: str = "gcd") -> None:
        """Guarda los modelos en archivos dentro de models_dir."""
        import os
        os.makedirs(self.models_dir, exist_ok=True)
        for name, model in [
            ('dropout', self.dropout_model),
            ('comprehension', self.comprehension_model),
            ('persistence', self.persistence_model),
            ('learning_rate', self.learning_rate_model)
        ]:
            if model is not None:
                path = os.path.join(self.models_dir, f"{prefix}_{name}.pkl")
                joblib.dump(model, path)
        print(f"Modelos guardados en {self.models_dir}")

    def load_models(self, prefix: str = "gcd") -> None:
        """Carga modelos desde archivos."""
        import os
        for name in ['dropout', 'comprehension', 'persistence', 'learning_rate']:
            path = os.path.join(self.models_dir, f"{prefix}_{name}.pkl")
            if os.path.exists(path):
                model = joblib.load(path)
                setattr(self, f"{name}_model", model)
            else:
                raise FileNotFoundError(f"Modelo no encontrado: {path}")
        self._fitted = True
        print("Modelos cargados correctamente.")

    # ------------------------------------------------------------------
    # Auxiliares
    # ------------------------------------------------------------------
    @staticmethod
    def _dict_to_df(data: Dict[str, float]) -> pd.DataFrame:
        """Convierte un diccionario en DataFrame con columnas en el orden correcto."""
        # Asegurar que todas las variables están presentes, rellenar con 0 si faltan
        row = {var: data.get(var, 0.0) for var in VARIABLES_PSICO}
        return pd.DataFrame([row])

    # ------------------------------------------------------------------
    # Método de conveniencia para predicción lote
    # ------------------------------------------------------------------
    def predict_batch(self, students: List[Dict[str, float]]) -> pd.DataFrame:
        """
        Predice para una lista de estudiantes y devuelve un DataFrame
        con todas las predicciones.
        """
        X = pd.DataFrame(students)[VARIABLES_PSICO]
        results = {}
        if self.dropout_model:
            results['dropout'] = self.dropout_model.predict_proba(X)[:, 1]
        if self.comprehension_model:
            results['comprehension'] = np.clip(self.comprehension_model.predict(X), 0, 1)
        if self.persistence_model:
            results['persistence'] = np.clip(self.persistence_model.predict(X), 0, 1)
        if self.learning_rate_model:
            results['learning_rate'] = np.maximum(0, self.learning_rate_model.predict(X))
        return pd.DataFrame(results)


# ----------------------------------------------------------------------
# Funciones de alto nivel (para usar sin instanciar la clase)
# ----------------------------------------------------------------------
_DEFAULT_LAYER: Optional[PredictiveLayer] = None


def get_default_layer() -> PredictiveLayer:
    """Retorna la instancia por defecto de la capa predictiva."""
    global _DEFAULT_LAYER
    if _DEFAULT_LAYER is None:
        _DEFAULT_LAYER = PredictiveLayer()
        try:
            _DEFAULT_LAYER.load_models()
        except FileNotFoundError:
            print("No se encontraron modelos pre-entrenados. Entrene primero con datos.")
    return _DEFAULT_LAYER


def predict_dropout(student_data: Dict[str, float]) -> float:
    """Función de conveniencia para predict_dropout."""
    return get_default_layer().predict_dropout(student_data)


def predict_comprehension(student_data: Dict[str, float]) -> float:
    """Función de conveniencia para predict_comprehension."""
    return get_default_layer().predict_comprehension(student_data)


def predict_persistence(student_data: Dict[str, float]) -> float:
    """Función de conveniencia para predict_persistence."""
    return get_default_layer().predict_persistence(student_data)


def predict_learning_rate(student_data: Dict[str, float]) -> float:
    """Función de conveniencia para predict_learning_rate."""
    return get_default_layer().predict_learning_rate(student_data)


# ----------------------------------------------------------------------
# Ejemplo de uso (si se ejecuta directamente)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    # Crear datos sintéticos de ejemplo
    np.random.seed(42)
    n = 500
    data = pd.DataFrame({
        'atencion': np.random.uniform(0.3, 1.0, n),
        'motivacion': np.random.uniform(0.2, 1.0, n),
        'persistencia': np.random.uniform(0.1, 1.0, n),
        'metacognicion': np.random.uniform(0.2, 1.0, n),
        'flexibilidad_cognitiva': np.random.uniform(0.3, 1.0, n),
        'rendimiento': np.random.uniform(0.0, 1.0, n),
        'engagement': np.random.uniform(0.2, 1.0, n),
        'fatiga': np.random.uniform(0.0, 0.8, n),
        'aciertos_previos': np.random.uniform(0, 20, n),
        'progresion_historica': np.random.uniform(0, 1, n),
    })
    # Generar objetivos sintéticos
    data['dropout'] = (1 / (1 + np.exp(-(0.5 - data['persistencia']*2 + data['fatiga']*1.5 + data['rendimiento']*(-1.5) + np.random.normal(0, 0.3, n)))) > 0.5).astype(int)
    data['comprehension'] = np.clip(0.3*data['atencion'] + 0.3*data['metacognicion'] + 0.2*data['aciertos_previos']/20 + np.random.normal(0, 0.1, n), 0, 1)
    data['persistence'] = np.clip(0.5*data['persistencia'] + 0.3*data['motivacion'] - 0.2*data['fatiga'] + np.random.normal(0, 0.1, n), 0, 1)
    data['learning_rate'] = np.maximum(0, 0.4*data['progresion_historica'] + 0.3*data['flexibilidad_cognitiva'] + np.random.normal(0, 0.1, n))

    # Entrenar capa
    layer = PredictiveLayer()
    target_cols = {
        'dropout': 'dropout',
        'comprehension': 'comprehension',
        'persistence': 'persistence',
        'learning_rate': 'learning_rate'
    }
    layer.fit(data, target_cols)

    # Guardar modelos
    layer.save_models()

    # Probar predicción en un estudiante nuevo
    estudiante = {
        'atencion': 0.8,
        'motivacion': 0.9,
        'persistencia': 0.7,
        'metacognicion': 0.6,
        'flexibilidad_cognitiva': 0.8,
        'rendimiento': 0.85,
        'engagement': 0.9,
        'fatiga': 0.2,
        'aciertos_previos': 15,
        'progresion_historica': 0.7
    }
    print("Predicciones para estudiante ejemplo:")
    print(f"  Dropout: {layer.predict_dropout(estudiante):.3f}")
    print(f"  Comprensión: {layer.predict_comprehension(estudiante):.3f}")
    print(f"  Persistencia futura: {layer.predict_persistence(estudiante):.3f}")
    print(f"  Tasa de aprendizaje: {layer.predict_learning_rate(estudiante):.3f}")
