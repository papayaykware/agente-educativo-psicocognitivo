#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
statistical_tests.py - Pruebas Estadísticas Modulares

Propósito:
    Proporcionar funciones modulares para pruebas estadísticas comunes,
    incluyendo contrastes paramétricos y no paramétricos, pruebas de
    normalidad, homocedasticidad, y cálculo de tamaños del efecto.

Funciones principales:
    - t_test: t de Student (independiente o pareada)
    - mann_whitney: U de Mann-Whitney (muestras independientes)
    - wilcoxon: Wilcoxon (muestras pareadas)
    - anova_one_way: ANOVA de un factor
    - anova_two_way: ANOVA de dos factores (con interacción)
    - chi_square: Chi-cuadrado de independencia o bondad de ajuste
    - correlation: Pearson o Spearman
    - effect_size: Cohen's d, eta-cuadrado, V de Cramer, etc.
    - normality_tests: Shapiro-Wilk, Kolmogorov-Smirnov
    - homoscedasticity_tests: Levene, Bartlett
    - confidence_interval: Intervalo de confianza para la media

Todas las funciones devuelven un diccionario con estadísticos, p-valor,
tamaño del efecto (cuando procede) y otros resultados relevantes,
facilitando la integración con el sistema de reportes.

Uso típico:
    from evaluation.statistical_tests import t_test, effect_size
    result = t_test(group1, group2, paired=False)
    print(f"t({result['df']}) = {result['statistic']:.3f}, p = {result['p_value']:.4f}")
    cohen_d = effect_size('cohen_d', group1, group2)

Autor: Equipo GCD
Versión: 1.0.0
"""

import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import (
    ttest_ind, ttest_rel, mannwhitneyu, wilcoxon,
    f_oneway, chi2_contingency, chisquare,
    pearsonr, spearmanr,
    shapiro, kstest, levene, bartlett
)
from typing import Union, Tuple, Dict, Optional, List
import warnings

__all__ = [
    't_test',
    'mann_whitney',
    'wilcoxon_test',
    'anova_one_way',
    'anova_two_way',
    'chi_square_test',
    'correlation_test',
    'normality_test',
    'homoscedasticity_test',
    'effect_size',
    'confidence_interval'
]


# =============================================================================
# 1. Pruebas de comparación de medias
# =============================================================================

def t_test(group1: Union[np.ndarray, List[float]],
           group2: Union[np.ndarray, List[float]],
           paired: bool = False,
           equal_var: bool = True,
           alternative: str = 'two-sided') -> Dict[str, float]:
    """
    Realiza t-test (Student) para muestras independientes o pareadas.

    Args:
        group1: Primera muestra.
        group2: Segunda muestra.
        paired: Si es True, realiza t-test pareado (Wilcoxon si no normal).
        equal_var: Si es True, asume varianzas iguales (solo para independiente).
        alternative: 'two-sided', 'less', 'greater'.

    Returns:
        Diccionario con:
            - 'statistic': valor t
            - 'p_value': p-valor
            - 'df': grados de libertad
            - 'mean_diff': diferencia de medias (group1 - group2)
            - 'ci_lower', 'ci_upper': intervalo de confianza 95% para la diferencia
            - 'method': 't-test independent' o 't-test paired'

    Nota: Si paired=True y los datos no son normales, se recomienda usar wilcoxon_test.
    """
    group1 = np.asarray(group1)
    group2 = np.asarray(group2)

    if paired:
        # Verificar tamaño igual
        if len(group1) != len(group2):
            raise ValueError("Para prueba pareada, las muestras deben tener el mismo tamaño.")
        # Test pareado
        t_stat, p_val = ttest_rel(group1, group2, alternative=alternative)
        df = len(group1) - 1
        mean_diff = np.mean(group1 - group2)
        # IC 95% para la diferencia
        ci = stats.t.interval(0.95, df, loc=mean_diff,
                              scale=stats.sem(group1 - group2))
        method = 't-test paired'
    else:
        # Test independiente
        t_stat, p_val = ttest_ind(group1, group2, equal_var=equal_var,
                                  alternative=alternative)
        df = len(group1) + len(group2) - 2
        mean_diff = np.mean(group1) - np.mean(group2)
        # IC 95% para la diferencia de medias
        se = np.sqrt(np.var(group1, ddof=1)/len(group1) +
                     np.var(group2, ddof=1)/len(group2))
        ci = stats.t.interval(0.95, df, loc=mean_diff, scale=se)
        method = 't-test independent'

    return {
        'statistic': t_stat,
        'p_value': p_val,
        'df': df,
        'mean_diff': mean_diff,
        'ci_lower': ci[0],
        'ci_upper': ci[1],
        'method': method
    }


def mann_whitney(group1: Union[np.ndarray, List[float]],
                 group2: Union[np.ndarray, List[float]],
                 alternative: str = 'two-sided') -> Dict[str, float]:
    """
    Prueba U de Mann-Whitney (equivalente no paramétrico al t-test independiente).

    Args:
        group1: Primera muestra.
        group2: Segunda muestra.
        alternative: 'two-sided', 'less', 'greater'.

    Returns:
        Diccionario con:
            - 'statistic': U
            - 'p_value': p-valor
            - 'method': 'Mann-Whitney U'
    """
    u_stat, p_val = mannwhitneyu(group1, group2, alternative=alternative)
    return {
        'statistic': u_stat,
        'p_value': p_val,
        'method': 'Mann-Whitney U'
    }


def wilcoxon_test(group1: Union[np.ndarray, List[float]],
                  group2: Union[np.ndarray, List[float]],
                  alternative: str = 'two-sided') -> Dict[str, float]:
    """
    Prueba de Wilcoxon para muestras pareadas (no paramétrico).

    Args:
        group1: Primera muestra.
        group2: Segunda muestra (pareada con group1).
        alternative: 'two-sided', 'less', 'greater'.

    Returns:
        Diccionario con:
            - 'statistic': estadístico W
            - 'p_value': p-valor
            - 'method': 'Wilcoxon signed-rank'
    """
    if len(group1) != len(group2):
        raise ValueError("Para Wilcoxon, las muestras deben ser pareadas e igual tamaño.")
    w_stat, p_val = wilcoxon(group1, group2, alternative=alternative)
    return {
        'statistic': w_stat,
        'p_value': p_val,
        'method': 'Wilcoxon signed-rank'
    }


# =============================================================================
# 2. ANOVA
# =============================================================================

def anova_one_way(*groups) -> Dict[str, float]:
    """
    ANOVA de un factor (independiente).

    Args:
        *groups: Múltiples grupos como arrays o listas.

    Returns:
        Diccionario con:
            - 'statistic': F
            - 'p_value': p-valor
            - 'df_between': grados de libertad entre grupos
            - 'df_within': grados de libertad intra-grupos
            - 'method': 'ANOVA one-way'
    """
    if len(groups) < 2:
        raise ValueError("Se necesitan al menos dos grupos para ANOVA.")
    f_stat, p_val = f_oneway(*groups)
    df_between = len(groups) - 1
    df_within = sum(len(g) for g in groups) - len(groups)
    return {
        'statistic': f_stat,
        'p_value': p_val,
        'df_between': df_between,
        'df_within': df_within,
        'method': 'ANOVA one-way'
    }


def anova_two_way(data: pd.DataFrame, dv: str,
                  factor1: str, factor2: str) -> Dict:
    """
    ANOVA de dos factores (incluyendo interacción) usando statsmodels.
    Esta función requiere que se pase un DataFrame en formato largo.

    Args:
        data: DataFrame con columnas dv, factor1, factor2.
        dv: Nombre de la variable dependiente (continua).
        factor1: Nombre del primer factor (categórico).
        factor2: Nombre del segundo factor (categórico).

    Returns:
        Diccionario con tabla ANOVA (como DataFrame) y estadísticos.
        Incluye: source, SS, df, F, p-unc, eta_sq (eta cuadrado parcial).
    """
    try:
        import statsmodels.api as sm
        from statsmodels.formula.api import ols
        from statsmodels.stats.anova import anova_lm
    except ImportError:
        raise ImportError("statsmodels es necesario para ANOVA de dos factores.")

    model = ols(f'{dv} ~ C({factor1}) * C({factor2})', data=data).fit()
    anova_table = anova_lm(model, typ=2)
    # Añadir eta cuadrado parcial (aproximado)
    ss_total = anova_table['sum_sq'].sum()
    anova_table['eta_sq'] = anova_table['sum_sq'] / ss_total
    return {
        'anova_table': anova_table,
        'method': 'ANOVA two-way (Type II)',
        'model': model
    }


# =============================================================================
# 3. Pruebas Chi-cuadrado
# =============================================================================

def chi_square_test(observed: Union[np.ndarray, List],
                    expected: Optional[np.ndarray] = None,
                    correction: bool = True) -> Dict[str, float]:
    """
    Prueba chi-cuadrado de independencia (tabla de contingencia) o
    bondad de ajuste (si se proporcionan frecuencias esperadas).

    Args:
        observed: Tabla de contingencia (2D array) o vector de frecuencias observadas (1D).
        expected: Frecuencias esperadas (opcional, para bondad de ajuste).
        correction: Si es True, aplica corrección de Yates para tablas 2x2.

    Returns:
        Diccionario con:
            - 'statistic': chi-cuadrado
            - 'p_value': p-valor
            - 'df': grados de libertad
            - 'expected': frecuencias esperadas (si se calculan)
            - 'method': 'Chi-square independence' o 'Chi-square goodness-of-fit'
    """
    if expected is None:
        # Independencia
        chi2, p_val, dof, expected_freq = chi2_contingency(observed, correction=correction)
        method = 'Chi-square independence'
        return {
            'statistic': chi2,
            'p_value': p_val,
            'df': dof,
            'expected': expected_freq,
            'method': method
        }
    else:
        # Bondad de ajuste
        chi2, p_val = chisquare(observed, f_exp=expected)
        dof = len(observed) - 1
        return {
            'statistic': chi2,
            'p_value': p_val,
            'df': dof,
            'method': 'Chi-square goodness-of-fit'
        }


# =============================================================================
# 4. Correlación
# =============================================================================

def correlation_test(x: Union[np.ndarray, List],
                     y: Union[np.ndarray, List],
                     method: str = 'pearson') -> Dict[str, float]:
    """
    Calcula correlación de Pearson o Spearman.

    Args:
        x: Primera variable.
        y: Segunda variable.
        method: 'pearson' o 'spearman'.

    Returns:
        Diccionario con:
            - 'statistic': coeficiente de correlación (r o rho)
            - 'p_value': p-valor
            - 'n': número de pares
            - 'method': 'Pearson' o 'Spearman'
    """
    if len(x) != len(y):
        raise ValueError("x e y deben tener la misma longitud.")
    n = len(x)
    if method.lower() == 'pearson':
        r, p = pearsonr(x, y)
        method_name = 'Pearson'
    elif method.lower() == 'spearman':
        rho, p = spearmanr(x, y)
        method_name = 'Spearman'
    else:
        raise ValueError("Método debe ser 'pearson' o 'spearman'.")
    return {
        'statistic': r if method_name == 'Pearson' else rho,
        'p_value': p,
        'n': n,
        'method': method_name
    }


# =============================================================================
# 5. Pruebas de normalidad y homocedasticidad
# =============================================================================

def normality_test(data: Union[np.ndarray, List],
                   method: str = 'shapiro') -> Dict[str, float]:
    """
    Prueba de normalidad.

    Args:
        data: Muestra.
        method: 'shapiro' (Shapiro-Wilk) o 'ks' (Kolmogorov-Smirnov contra normal).

    Returns:
        Diccionario con:
            - 'statistic': estadístico de la prueba
            - 'p_value': p-valor
            - 'method': 'Shapiro-Wilk' o 'Kolmogorov-Smirnov'
    """
    data = np.asarray(data)
    if method.lower() == 'shapiro':
        stat, p = shapiro(data)
        method_name = 'Shapiro-Wilk'
    elif method.lower() == 'ks':
        # Kolmogorov-Smirnov contra distribución normal con media y std de la muestra
        from scipy.stats import kstest
        stat, p = kstest(data, 'norm', args=(np.mean(data), np.std(data, ddof=1)))
        method_name = 'Kolmogorov-Smirnov (against normal)'
    else:
        raise ValueError("Método debe ser 'shapiro' o 'ks'.")
    return {
        'statistic': stat,
        'p_value': p,
        'method': method_name
    }


def homoscedasticity_test(*groups, method: str = 'levene') -> Dict[str, float]:
    """
    Prueba de homogeneidad de varianzas (Levene o Bartlett).

    Args:
        *groups: Múltiples grupos.
        method: 'levene' (más robusto) o 'bartlett' (sensible a normalidad).

    Returns:
        Diccionario con:
            - 'statistic': estadístico
            - 'p_value': p-valor
            - 'method': 'Levene' o 'Bartlett'
    """
    if len(groups) < 2:
        raise ValueError("Se necesitan al menos dos grupos.")
    if method.lower() == 'levene':
        stat, p = levene(*groups)
        method_name = 'Levene'
    elif method.lower() == 'bartlett':
        stat, p = bartlett(*groups)
        method_name = 'Bartlett'
    else:
        raise ValueError("Método debe ser 'levene' o 'bartlett'.")
    return {
        'statistic': stat,
        'p_value': p,
        'method': method_name
    }


# =============================================================================
# 6. Tamaños del efecto
# =============================================================================

def effect_size(effect_type: str, *args, **kwargs) -> float:
    """
    Calcula diferentes medidas de tamaño del efecto.

    Tipos soportados:
        - 'cohen_d': Cohen's d para dos grupos independientes o pareados.
        - 'eta_squared': Eta cuadrado para ANOVA (necesita SS entre y SS total).
        - 'cramer_v': V de Cramer para tablas de contingencia.
        - 'r_pearson': Coeficiente de correlación (ya calculado).

    Uso:
        cohen_d = effect_size('cohen_d', grupo1, grupo2, paired=False)
        cohen_d_paired = effect_size('cohen_d', pre, post, paired=True)
        eta = effect_size('eta_squared', ss_between=10, ss_total=50)
        cramer = effect_size('cramer_v', chi2=5.0, n=100, df=1)

    Args:
        effect_type: 'cohen_d', 'eta_squared', 'cramer_v', 'r'.
        *args, **kwargs: Parámetros específicos.

    Returns:
        float: Tamaño del efecto calculado.
    """
    if effect_type == 'cohen_d':
        if len(args) >= 2:
            group1 = np.asarray(args[0])
            group2 = np.asarray(args[1])
            paired = kwargs.get('paired', False)
            if paired:
                diff = group1 - group2
                d = np.mean(diff) / np.std(diff, ddof=1)
            else:
                n1, n2 = len(group1), len(group2)
                var1 = np.var(group1, ddof=1)
                var2 = np.var(group2, ddof=1)
                pooled_var = ((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2)
                d = (np.mean(group1) - np.mean(group2)) / np.sqrt(pooled_var)
            return d
        else:
            raise ValueError("Para Cohen's d se necesitan dos grupos.")

    elif effect_type == 'eta_squared':
        ss_between = kwargs.get('ss_between')
        ss_total = kwargs.get('ss_total')
        if ss_between is None or ss_total is None:
            raise ValueError("Para eta cuadrado se necesitan ss_between y ss_total.")
        return ss_between / ss_total

    elif effect_type == 'cramer_v':
        chi2 = kwargs.get('chi2')
        n = kwargs.get('n')
        df = kwargs.get('df')
        if chi2 is None or n is None or df is None:
            raise ValueError("Para V de Cramer se necesitan chi2, n y df.")
        return np.sqrt(chi2 / (n * min(df + 1, 1)))  # df +1 para el número de filas/columnas

    elif effect_type == 'r':
        # Coeficiente de correlación ya calculado
        r = kwargs.get('r')
        if r is None:
            raise ValueError("Para efecto r, proporcionar el valor de r.")
        return r

    else:
        raise ValueError(f"Tipo de efecto '{effect_type}' no soportado.")


# =============================================================================
# 7. Intervalo de confianza para la media
# =============================================================================

def confidence_interval(data: Union[np.ndarray, List],
                        confidence: float = 0.95) -> Dict[str, float]:
    """
    Calcula el intervalo de confianza para la media de una muestra.

    Args:
        data: Muestra.
        confidence: Nivel de confianza (entre 0 y 1).

    Returns:
        Diccionario con:
            - 'mean': media muestral
            - 'std': desviación estándar
            - 'n': tamaño muestral
            - 'ci_lower': límite inferior del IC
            - 'ci_upper': límite superior del IC
            - 'margin_error': error marginal
    """
    data = np.asarray(data)
    n = len(data)
    mean = np.mean(data)
    std = np.std(data, ddof=1)
    sem = stats.sem(data)
    t_crit = stats.t.ppf(1 - (1 - confidence) / 2, df=n-1)
    margin = t_crit * sem
    return {
        'mean': mean,
        'std': std,
        'n': n,
        'ci_lower': mean - margin,
        'ci_upper': mean + margin,
        'margin_error': margin
    }


# =============================================================================
# 8. Ejemplos y pruebas rápidas
# =============================================================================

if __name__ == "__main__":
    # Generar datos de ejemplo
    np.random.seed(42)
    group1 = np.random.normal(0, 1, 30)
    group2 = np.random.normal(0.5, 1, 30)
    group3 = np.random.normal(1.2, 1, 30)
    paired1 = np.random.normal(0, 1, 30)
    paired2 = paired1 + np.random.normal(0.2, 0.5, 30)

    print("=== Pruebas estadísticas ===")
    # t-test independiente
    res = t_test(group1, group2)
    print(f"t-test: t={res['statistic']:.3f}, p={res['p_value']:.4f}, df={res['df']}")

    # Mann-Whitney
    res = mann_whitney(group1, group2)
    print(f"Mann-Whitney: U={res['statistic']:.3f}, p={res['p_value']:.4f}")

    # Wilcoxon
    res = wilcoxon_test(paired1, paired2)
    print(f"Wilcoxon: W={res['statistic']:.3f}, p={res['p_value']:.4f}")

    # ANOVA one-way
    res = anova_one_way(group1, group2, group3)
    print(f"ANOVA one-way: F={res['statistic']:.3f}, p={res['p_value']:.4f}")

    # Correlación
    x = np.random.normal(0, 1, 50)
    y = x + np.random.normal(0, 0.5, 50)
    res = correlation_test(x, y, 'pearson')
    print(f"Pearson: r={res['statistic']:.3f}, p={res['p_value']:.4f}")

    # Normalidad
    res = normality_test(group1, 'shapiro')
    print(f"Shapiro: stat={res['statistic']:.4f}, p={res['p_value']:.4f}")

    # Homocedasticidad
    res = homoscedasticity_test(group1, group2, group3, method='levene')
    print(f"Levene: stat={res['statistic']:.4f}, p={res['p_value']:.4f}")

    # Cohen's d
    d = effect_size('cohen_d', group1, group2, paired=False)
    print(f"Cohen's d = {d:.3f}")

    # Intervalo de confianza
    ci = confidence_interval(group1, confidence=0.95)
    print(f"IC 95% para la media: [{ci['ci_lower']:.3f}, {ci['ci_upper']:.3f}]")

    print("\nTodas las pruebas completadas con éxito.")
