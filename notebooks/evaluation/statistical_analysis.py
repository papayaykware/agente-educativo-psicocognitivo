#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
statistical_analysis.py - Análisis Inferencial Robusto

Propósito:
    Implementar los modelos estadísticos necesarios para validar (o refutar)
    cada hipótesis del proyecto (H1-H4) con el rigor científico requerido.

Funcionalidades:
    - ANOVA mixto (grupo × tiempo) para retención y velocidad de aprendizaje (H1)
    - Modelos de supervivencia (Kaplan-Meier, Cox) para abandono (H2)
    - Regresión logística múltiple para predictores de abandono (H2)
    - Modelos lineales mixtos (crecimiento multinivel) para trayectorias individuales (H1, H3)
    - Análisis de mediación para explorar mecanismos (ej. metacognición → persistencia → retención) (H3, H4)

Salidas:
    - Tablas de coeficientes, intervalos de confianza, p-valores (en formato CSV y HTML)
    - Diagnósticos de modelos (residuos, colinealidad) en gráficos y tablas
    - Archivos de resultados en formato pickle (para reproducibilidad) y RData (opcional)

Uso típico:
    from evaluation.statistical_analysis import run_analysis
    results = run_analysis(data="benchmark_results.csv", output_dir="./results")
"""

import os
import sys
import pickle
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, Optional, Tuple, List, Any
import warnings
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=UserWarning)

# Bibliotecas estadísticas
import scipy.stats as stats
from scipy.stats import shapiro, levene, ttest_ind, mannwhitneyu
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from statsmodels.graphics.regressionplots import plot_leverage_resid2
from statsmodels.stats.outliers_influence import variance_inflation_factor

# Modelos de supervivencia (lifelines)
try:
    from lifelines import KaplanMeierFitter, CoxPHFitter
    from lifelines.statistics import logrank_test
    LIFELINES_AVAILABLE = True
except ImportError:
    LIFELINES_AVAILABLE = False
    print("Advertencia: lifelines no instalado. Los análisis de supervivencia no estarán disponibles.",
          file=sys.stderr)

# Para ANOVA mixto y mediación (pingouin)
try:
    import pingouin as pg
    PINGOUIN_AVAILABLE = True
except ImportError:
    PINGOUIN_AVAILABLE = False
    print("Advertencia: pingouin no instalado. El ANOVA mixto y el análisis de mediación se realizarán con statsmodels.",
          file=sys.stderr)

# Para visualización
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score, roc_curve
from sklearn.preprocessing import StandardScaler

# Configuración de estilo
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("Set2")

# Logger simple
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# =============================================================================
# 1. Carga y preparación de datos
# =============================================================================

def load_and_prepare_data(csv_path: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Carga los datos crudos (por sesión) y calcula métricas por sujeto.
    Retorna: (df_long, df_subject)
        - df_long: datos en formato largo (sujeto, sesión, modelo, métricas)
        - df_subject: métricas agregadas por sujeto (incluyendo tiempo de abandono)
    """
    df = pd.read_csv(csv_path)
    logger.info(f"Datos cargados: {len(df)} filas")

    # Asegurar que las columnas necesarias existen
    required_cols = ['subject_id', 'model', 'session', 'knowledge', 'retention',
                     'attention', 'motivation', 'persistence_effort', 'dropout']
    if not all(col in df.columns for col in required_cols):
        raise ValueError(f"El CSV debe contener las columnas: {required_cols}")

    # Convertir tipos
    df['subject_id'] = df['subject_id'].astype('category')
    df['model'] = df['model'].astype('category')
    df['session'] = df['session'].astype(int)
    df['dropout'] = df['dropout'].astype(bool)

    # Calcular métricas por sujeto
    from evaluation.metrics_report import compute_subject_metrics
    subject_metrics = compute_subject_metrics(df)

    return df, subject_metrics


# =============================================================================
# 2. ANOVA mixto (grupo × tiempo) para retención y velocidad de aprendizaje (H1)
# =============================================================================

def mixed_anova(df_long: pd.DataFrame, dv: str = 'retention') -> Dict:
    """
    Realiza un ANOVA mixto de medidas repetidas con grupo (GCD vs Control)
    como factor entre-sujetos y tiempo (sesión) como factor intra-sujetos.

    Args:
        df_long: DataFrame en formato largo (subject_id, model, session, dv)
        dv: nombre de la variable dependiente (ej. 'retention', 'knowledge')

    Retorna:
        Diccionario con:
            - 'anova_table': tabla ANOVA (fuente, SS, df, F, p, etc.)
            - 'posthoc': tabla de comparaciones post-hoc (Tukey) para interacción
            - 'model': objeto de modelo ajustado (statsmodels)
    """
    logger.info(f"Ejecutando ANOVA mixto para {dv}...")

    # Asegurar que los datos están completos
    data = df_long[['subject_id', 'model', 'session', dv]].dropna()
    # Recodificar modelo como numérico para statsmodels
    data = data.copy()
    data['model_num'] = (data['model'] == 'gcd').astype(int)  # 1 = GCD, 0 = Control

    # ANOVA mixto usando statsmodels (método de mínimos cuadrados)
    # Modelo: dv ~ modelo * session + (1|subject_id)
    # Usamos la fórmula con efectos fijos y aleatorios
    try:
        model = smf.mixedlm(
            f"{dv} ~ model_num * session",
            data,
            groups=data["subject_id"],
            re_formula="~ session"  # pendiente aleatoria por sujeto
        ).fit(method='lbfgs')
    except Exception as e:
        logger.warning(f"Modelo mixto falló: {e}. Intentando modelo sin pendiente aleatoria.")
        model = smf.mixedlm(
            f"{dv} ~ model_num * session",
            data,
            groups=data["subject_id"],
            re_formula="~ 1"  # solo intercept aleatorio
        ).fit(method='lbfgs')

    # Tabla de efectos fijos
    fixed_effects = model.summary().tables[1]
    # Extraer p-valores, coeficientes, IC
    coef_df = pd.DataFrame({
        'coef': model.params,
        'std_err': model.bse,
        'z': model.tvalues,
        'p_value': model.pvalues
    })
    # Añadir intervalos de confianza (aproximados)
    ci = model.conf_int()
    coef_df['ci_lower'] = ci[0]
    coef_df['ci_upper'] = ci[1]

    # Si pingouin está disponible, podemos obtener la tabla ANOVA más completa
    if PINGOUIN_AVAILABLE:
        # Pingouin requiere formato ancho (cada sesión una columna)
        # Convertir a ancho
        pivot = data.pivot_table(index=['subject_id', 'model'],
                                 columns='session',
                                 values=dv).reset_index()
        pivot.columns = ['subject_id', 'model'] + [f'session_{c}' for c in pivot.columns[2:]]
        # Realizar ANOVA mixto
        aov = pg.mixed_anova(data=pivot, dv=dv, within='session',
                             between='model', subject='subject_id')
        # Realizar comparaciones post-hoc para la interacción
        if 'session:model' in aov['Source'].values:
            posthoc = pg.pairwise_tukey(data=data, dv=dv,
                                        between=['model', 'session'])
        else:
            posthoc = None
    else:
        # Sin pingouin, generamos una tabla ANOVA aproximada usando modelo anidado
        # Esto es menos robusto, pero funcional
        aov = None
        posthoc = None

    return {
        'anova_table': aov if aov is not None else coef_df,
        'posthoc': posthoc,
        'model': model,
        'coef_table': coef_df
    }


# =============================================================================
# 3. Modelos de supervivencia (Kaplan-Meier, Cox) para abandono (H2)
# =============================================================================

def survival_analysis(subject_metrics: pd.DataFrame, max_session: int) -> Dict:
    """
    Realiza análisis de supervivencia:
        - Curva de Kaplan-Meier por grupo
        - Prueba log-rank
        - Modelo de Cox con covariables (persistencia, rendimiento, etc.)

    Args:
        subject_metrics: DataFrame con columnas: subject_id, model, dropout_time,
                         dropout_occurred, avg_persistence, avg_attention, avg_motivation, etc.
        max_session: número máximo de sesiones (para censura)

    Retorna:
        Diccionario con: kaplan_meier_fig, logrank_p, cox_model, cox_summary
    """
    if not LIFELINES_AVAILABLE:
        logger.warning("lifelines no instalado. Saltando análisis de supervivencia.")
        return {}

    logger.info("Ejecutando análisis de supervivencia...")

    # Preparar datos de supervivencia
    surv_data = subject_metrics.copy()
    surv_data['time'] = surv_data['dropout_time'].fillna(max_session)
    surv_data['event'] = surv_data['dropout_occurred'].astype(int)

    # Kaplan-Meier por grupo
    kmf_gcd = KaplanMeierFitter()
    kmf_ctrl = KaplanMeierFitter()
    gcd = surv_data[surv_data['model'] == 'gcd']
    ctrl = surv_data[surv_data['model'] == 'control']

    fig, ax = plt.subplots(figsize=(10, 6))
    if len(gcd) > 0:
        kmf_gcd.fit(gcd['time'], gcd['event'], label='GCD')
        kmf_gcd.plot(ax=ax)
    if len(ctrl) > 0:
        kmf_ctrl.fit(ctrl['time'], ctrl['event'], label='Control')
        kmf_ctrl.plot(ax=ax)

    ax.set_xlabel('Sesión')
    ax.set_ylabel('Probabilidad de supervivencia')
    ax.set_title('Curva de Kaplan-Meier por grupo')
    ax.legend()
    sns.despine()

    # Log-rank test
    if len(gcd) > 0 and len(ctrl) > 0:
        results = logrank_test(gcd['time'], ctrl['time'],
                               gcd['event'], ctrl['event'])
        logrank_p = results.p_value
        ax.text(0.7, 0.9, f'Log-rank p = {logrank_p:.4f}',
                transform=ax.transAxes, fontsize=12,
                bbox=dict(facecolor='white', alpha=0.8))
    else:
        logrank_p = np.nan

    # Modelo de Cox con covariables
    # Seleccionar covariables relevantes (persistencia, atención, motivación, creatividad, etc.)
    cov_cols = ['avg_persistence', 'avg_attention', 'avg_motivation', 'creativity_final']
    # Filtrar columnas que existan y tengan datos
    cov_cols = [c for c in cov_cols if c in surv_data.columns and surv_data[c].notna().all()]
    if len(cov_cols) == 0:
        logger.warning("No hay covariables suficientes para modelo de Cox.")
        cox_model = None
        cox_summary = None
    else:
        cox_df = surv_data[['time', 'event', 'model'] + cov_cols].copy()
        # Codificar modelo como numérico
        cox_df['model_encoded'] = (cox_df['model'] == 'gcd').astype(int)
        # Escalar covariables continuas para estabilidad
        scaler = StandardScaler()
        for col in cov_cols:
            cox_df[col] = scaler.fit_transform(cox_df[[col]])

        # Ajustar modelo de Cox
        cph = CoxPHFitter()
        try:
            cph.fit(cox_df, duration_col='time', event_col='event',
                    formula='model_encoded + ' + ' + '.join(cov_cols))
            cox_model = cph
            cox_summary = cph.summary
        except Exception as e:
            logger.error(f"Error en modelo de Cox: {e}")
            cox_model = None
            cox_summary = None

    return {
        'km_fig': fig,
        'logrank_p': logrank_p,
        'cox_model': cox_model,
        'cox_summary': cox_summary
    }


# =============================================================================
# 4. Regresión logística para predictores de abandono (H2)
# =============================================================================

def logistic_regression_abandon(subject_metrics: pd.DataFrame) -> Dict:
    """
    Modelo de regresión logística para predecir abandono a partir de
    persistencia, rendimiento (retención final), atención, motivación, etc.

    Retorna:
        - modelo ajustado (sklearn o statsmodels)
        - tabla de coeficientes con OR, IC, p-valores
        - métricas de clasificación (AUC, precisión, recall)
        - figura ROC
    """
    logger.info("Ejecutando regresión logística para abandono...")

    # Seleccionar predictores
    predictors = ['avg_persistence', 'retention_final', 'avg_attention',
                  'avg_motivation', 'learning_speed']
    # Filtrar disponibles
    available = [p for p in predictors if p in subject_metrics.columns]
    if not available:
        logger.warning("No hay predictores disponibles para regresión logística.")
        return {}

    data = subject_metrics[['dropout_occurred'] + available].dropna()
    X = data[available]
    y = data['dropout_occurred'].astype(int)

    # Escalar variables
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_scaled_df = pd.DataFrame(X_scaled, columns=X.columns)

    # Usar statsmodels para obtener inferencia (p-valores, IC)
    X_sm = sm.add_constant(X_scaled_df)
    model_sm = sm.Logit(y, X_sm)
    result_sm = model_sm.fit(disp=0)  # silencioso
    coef_table = result_sm.summary2().tables[1]
    # Calcular Odds Ratios e IC
    params = result_sm.params
    conf = result_sm.conf_int()
    odds_ratios = np.exp(params)
    or_ci_lower = np.exp(conf[0])
    or_ci_upper = np.exp(conf[1])
    or_table = pd.DataFrame({
        'coef': params,
        'OR': odds_ratios,
        'OR_CI_lower': or_ci_lower,
        'OR_CI_upper': or_ci_upper,
        'p_value': result_sm.pvalues
    })

    # Evaluación del modelo
    y_pred_prob = result_sm.predict(X_sm)
    y_pred_class = (y_pred_prob > 0.5).astype(int)
    auc = roc_auc_score(y, y_pred_prob)
    report = classification_report(y, y_pred_class, output_dict=True)

    # Curva ROC
    fpr, tpr, _ = roc_curve(y, y_pred_prob)
    fig_roc, ax = plt.subplots(figsize=(8, 6))
    ax.plot(fpr, tpr, label=f'AUC = {auc:.3f}', linewidth=2)
    ax.plot([0, 1], [0, 1], 'k--')
    ax.set_xlabel('Tasa de falsos positivos')
    ax.set_ylabel('Tasa de verdaderos positivos')
    ax.set_title('Curva ROC para predicción de abandono')
    ax.legend()
    sns.despine()

    return {
        'logit_model': result_sm,
        'coef_table': or_table,
        'auc': auc,
        'classification_report': report,
        'roc_fig': fig_roc,
        'predictors': available
    }


# =============================================================================
# 5. Modelos lineales mixtos para trayectorias individuales (H1, H3)
# =============================================================================

def growth_curve_model(df_long: pd.DataFrame, dv: str = 'retention') -> Dict:
    """
    Ajusta un modelo lineal mixto de crecimiento (intercepto y pendiente aleatorios)
    para evaluar el efecto de grupo (GCD vs Control) sobre la trayectoria.

    Retorna:
        - modelo ajustado
        - tabla de efectos fijos
        - diagnóstico de residuos
    """
    logger.info(f"Ajustando modelo de crecimiento para {dv}...")

    data = df_long[['subject_id', 'model', 'session', dv]].dropna()
    data['model_num'] = (data['model'] == 'gcd').astype(int)

    # Modelo: intercept y slope aleatorios, efectos fijos para grupo y tiempo
    try:
        model = smf.mixedlm(
            f"{dv} ~ model_num * session",
            data,
            groups=data["subject_id"],
            re_formula="~ session"
        ).fit(method='lbfgs')
    except Exception as e:
        logger.warning(f"Modelo con pendiente aleatoria falló: {e}. Usando solo intercept aleatorio.")
        model = smf.mixedlm(
            f"{dv} ~ model_num * session",
            data,
            groups=data["subject_id"],
            re_formula="~ 1"
        ).fit(method='lbfgs')

    # Efectos fijos
    fixed = model.summary().tables[1]
    # Coeficientes con IC
    coef_df = pd.DataFrame({
        'coef': model.params,
        'std_err': model.bse,
        't': model.tvalues,
        'p_value': model.pvalues
    })
    ci = model.conf_int()
    coef_df['ci_lower'] = ci[0]
    coef_df['ci_upper'] = ci[1]

    # Diagnóstico: residuos vs ajustados
    fitted = model.fittedvalues
    resid = model.resid
    fig_diag, ax = plt.subplots(1, 2, figsize=(12, 5))
    ax[0].scatter(fitted, resid, alpha=0.5)
    ax[0].axhline(0, color='red', linestyle='--')
    ax[0].set_xlabel('Valores ajustados')
    ax[0].set_ylabel('Residuos')
    ax[0].set_title('Residuos vs Ajustados')
    # Q-Q plot
    stats.probplot(resid, dist="norm", plot=ax[1])
    ax[1].set_title('Q-Q plot de residuos')
    sns.despine()

    return {
        'model': model,
        'coef_table': coef_df,
        'diagnostic_fig': fig_diag
    }


# =============================================================================
# 6. Análisis de mediación (ej. metacognición → persistencia → retención) (H3)
# =============================================================================

def mediation_analysis(subject_metrics: pd.DataFrame,
                       mediator: str = 'avg_persistence',
                       predictor: str = 'avg_attention',
                       outcome: str = 'retention_final') -> Dict:
    """
    Realiza un análisis de mediación simple utilizando el método de Baron & Kenny
    o bootstrapping (si pingouin está disponible).

    Retorna:
        - efecto directo, indirecto, total
        - intervalos de confianza bootstrap
        - significancia
    """
    logger.info(f"Ejecutando análisis de mediación: {predictor} -> {mediator} -> {outcome}")

    data = subject_metrics[[predictor, mediator, outcome]].dropna()
    if len(data) < 20:
        logger.warning("Pocos datos para mediación. Los resultados pueden ser inestables.")
        return {}

    if PINGOUIN_AVAILABLE:
        # Usar pingouin para mediación con bootstrapping
        try:
            med = pg.mediation_analysis(data=data,
                                        x=predictor,
                                        m=mediator,
                                        y=outcome,
                                        n_boot=1000,
                                        seed=42)
            return {'mediation_result': med}
        except Exception as e:
            logger.error(f"Error en mediación con pingouin: {e}")

    # Método alternativo usando statsmodels (Baron & Kenny)
    # Paso 1: predictor -> outcome (total)
    model_total = smf.ols(f"{outcome} ~ {predictor}", data=data).fit()
    # Paso 2: predictor -> mediator
    model_med = smf.ols(f"{mediator} ~ {predictor}", data=data).fit()
    # Paso 3: predictor + mediator -> outcome (directo)
    model_direct = smf.ols(f"{outcome} ~ {predictor} + {mediator}", data=data).fit()

    # Efectos
    total_effect = model_total.params[predictor]
    direct_effect = model_direct.params[predictor]
    indirect_effect = model_med.params[predictor] * model_direct.params[mediator]

    # Bootstrapping simple para IC del indirecto
    n_boot = 1000
    boot_indirect = []
    np.random.seed(42)
    for _ in range(n_boot):
        idx = np.random.choice(len(data), len(data), replace=True)
        boot_data = data.iloc[idx]
        try:
            b_med = smf.ols(f"{mediator} ~ {predictor}", data=boot_data).fit()
            b_direct = smf.ols(f"{outcome} ~ {predictor} + {mediator}", data=boot_data).fit()
            boot_indirect.append(b_med.params[predictor] * b_direct.params[mediator])
        except:
            continue
    boot_indirect = np.array(boot_indirect)
    ci_lower, ci_upper = np.percentile(boot_indirect, [2.5, 97.5])

    return {
        'total_effect': total_effect,
        'direct_effect': direct_effect,
        'indirect_effect': indirect_effect,
        'indirect_ci_lower': ci_lower,
        'indirect_ci_upper': ci_upper,
        'p_value': (ci_lower < 0 < ci_upper)  # aproximado: si IC no contiene 0, significativo
    }


# =============================================================================
# 7. Función principal que ejecuta todos los análisis
# =============================================================================

def run_analysis(data_path: str, output_dir: str = "./results") -> Dict:
    """
    Ejecuta el pipeline completo de análisis estadístico y guarda los resultados.

    Args:
        data_path: ruta al archivo CSV con datos crudos (benchmark_results)
        output_dir: directorio donde guardar los resultados

    Retorna:
        Diccionario con todos los resultados de los análisis.
    """
    os.makedirs(output_dir, exist_ok=True)
    logger.info(f"Iniciando análisis completo. Datos: {data_path}")

    # Cargar datos
    df_long, subject_metrics = load_and_prepare_data(data_path)
    max_session = df_long['session'].max()

    results = {}

    # 1. ANOVA mixto para retención
    results['anova_retention'] = mixed_anova(df_long, 'retention')
    # 2. ANOVA mixto para conocimiento (opcional)
    results['anova_knowledge'] = mixed_anova(df_long, 'knowledge')

    # 3. Modelos de crecimiento
    results['growth_retention'] = growth_curve_model(df_long, 'retention')
    results['growth_knowledge'] = growth_curve_model(df_long, 'knowledge')

    # 4. Análisis de supervivencia
    results['survival'] = survival_analysis(subject_metrics, max_session)

    # 5. Regresión logística para abandono
    results['logistic'] = logistic_regression_abandon(subject_metrics)

    # 6. Análisis de mediación
    # Ejemplo: atención -> persistencia -> retención
    if 'avg_attention' in subject_metrics.columns and 'avg_persistence' in subject_metrics.columns:
        results['mediation_att_pers_ret'] = mediation_analysis(
            subject_metrics,
            mediator='avg_persistence',
            predictor='avg_attention',
            outcome='retention_final'
        )
    # Otro ejemplo: metacognición -> persistencia -> retención (usamos motivación como proxy de metacognición)
    if 'avg_motivation' in subject_metrics.columns:
        results['mediation_mot_pers_ret'] = mediation_analysis(
            subject_metrics,
            mediator='avg_persistence',
            predictor='avg_motivation',
            outcome='retention_final'
        )

    # Guardar resultados en formato pickle
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pickle_path = os.path.join(output_dir, f"statistical_results_{timestamp}.pkl")
    with open(pickle_path, 'wb') as f:
        pickle.dump(results, f)
    logger.info(f"Resultados guardados en {pickle_path}")

    # Guardar tablas de coeficientes en CSV
    for name, res in results.items():
        if isinstance(res, dict):
            for key, val in res.items():
                if key.endswith('_table') or key == 'coef_table' or key == 'cox_summary':
                    if isinstance(val, pd.DataFrame):
                        csv_path = os.path.join(output_dir, f"{name}_{key}_{timestamp}.csv")
                        val.to_csv(csv_path)
                        logger.info(f"Tabla guardada: {csv_path}")

    # También guardar una versión en RData (si rpy2 está disponible)
    try:
        import rpy2.robjects as ro
        from rpy2.robjects import pandas2ri
        pandas2ri.activate()
        rdata_path = os.path.join(output_dir, f"statistical_results_{timestamp}.RData")
        # Convertir resultados a objetos R y guardar
        # Esto es simplificado; idealmente se guardan todos los dataframes
        for name, res in results.items():
            if isinstance(res, dict) and 'coef_table' in res:
                ro.r.assign(f"{name}_coef", pandas2ri.py2rpy(res['coef_table']))
        ro.r(f"save(list=ls(), file='{rdata_path}')")
        logger.info(f"Resultados guardados en formato RData: {rdata_path}")
    except ImportError:
        logger.info("rpy2 no instalado. No se generó archivo RData.")

    return results


# =============================================================================
# 8. Ejemplo de uso (cuando se ejecuta como script)
# =============================================================================

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Ejecutar análisis estadístico completo.")
    parser.add_argument('data', help='Ruta al archivo CSV de benchmark')
    parser.add_argument('-o', '--output', default='./results', help='Directorio de salida')
    args = parser.parse_args()

    results = run_analysis(args.data, args.output)

    # Mostrar un resumen en consola
    print("\n" + "="*60)
    print("RESUMEN DE RESULTADOS")
    print("="*60)

    if 'anova_retention' in results and 'coef_table' in results['anova_retention']:
        print("\nANOVA mixto para retención:")
        print(results['anova_retention']['coef_table'])

    if 'survival' in results and 'logrank_p' in results['survival']:
        print(f"\nLog-rank p (abandono): {results['survival']['logrank_p']:.4f}")

    if 'logistic' in results and 'auc' in results['logistic']:
        print(f"\nRegresión logística - AUC: {results['logistic']['auc']:.3f}")

    if 'mediation_att_pers_ret' in results:
        med = results['mediation_att_pers_ret']
        if 'indirect_effect' in med:
            print(f"\nMediación (atención -> persistencia -> retención):")
            print(f"  Efecto indirecto = {med['indirect_effect']:.3f} (IC 95%: [{med['indirect_ci_lower']:.3f}, {med['indirect_ci_upper']:.3f}])")
    print("\nAnálisis completado. Revise el directorio de salida para tablas y gráficos.")
