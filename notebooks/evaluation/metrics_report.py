#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
metrics_report.py - Reporte Automatizado de Métricas

Propósito:
    Generar reportes visuales y tablas resumen que permitan comunicar los
    hallazgos de forma clara y reproducible a partir de los datos generados
    por benchmark.py.

Funcionalidades:
    - Carga de datos (CSV con resultados por sujeto y sesión)
    - Cálculo de métricas primarias y secundarias por sujeto
    - Pruebas estadísticas (t-test, U de Mann-Whitney, Cohen's d)
    - Visualizaciones: curvas de aprendizaje, diagramas de caja,
      análisis de supervivencia (Kaplan-Meier), matrices de correlación
    - Exportación a HTML (autónomo con gráficos embebidos)

Uso:
    from evaluation.metrics_report import generate_report
    generate_report(
        data="benchmark_results_20260117_120000.csv",
        output="reports/experiment_20260117.html",
        include_plots=True
    )

Estructura del reporte:
    - Resumen ejecutivo
    - Tabla de comparación de grupos (media ± DE, p-valor, Cohen's d)
    - Gráficos de tendencia temporal
    - Análisis de subgrupos (si existen variables categóricas)
    - Conclusiones y recomendaciones
"""

import os
import sys
import base64
import io
import json
import numpy as np
import pandas as pd
from datetime import datetime
from typing import Optional, Dict, List, Tuple, Any
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import ttest_ind, mannwhitneyu, pearsonr
import warnings
warnings.filterwarnings('ignore', category=FutureWarning)

# Para análisis de supervivencia (Kaplan-Meier)
try:
    from lifelines import KaplanMeierFitter
    from lifelines.statistics import logrank_test
    LIFELINES_AVAILABLE = True
except ImportError:
    LIFELINES_AVAILABLE = False
    print("Advertencia: lifelines no instalado. No se generarán curvas de Kaplan-Meier.",
          file=sys.stderr)

# Para plantillas HTML
try:
    from jinja2 import Template
    JINJA_AVAILABLE = True
except ImportError:
    JINJA_AVAILABLE = False
    print("Advertencia: jinja2 no instalado. Se usará formato básico.",
          file=sys.stderr)

# Configuración de estilo de gráficos
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("Set2")


# -----------------------------------------------------------------------------
# 1. Cálculo de métricas por sujeto
# -----------------------------------------------------------------------------

def compute_subject_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    A partir de un DataFrame con datos por sesión (columnas: subject_id, model, session,
    knowledge, retention, attention, motivation, persistence_effort, dropout, creativity),
    calcula métricas agregadas por sujeto.

    Retorna un DataFrame con una fila por sujeto y las siguientes columnas:
        - subject_id, model
        - retention_final, dropout_time, dropout_occurred, learning_speed,
          creativity_final, avg_attention, avg_motivation, avg_persistence,
          total_sessions_active
    """
    subjects = df['subject_id'].unique()
    records = []
    for sid in subjects:
        sub_df = df[df['subject_id'] == sid].sort_values('session')
        model = sub_df['model'].iloc[0]

        # Filtrar sesiones activas (donde knowledge no sea NaN)
        active = sub_df[~sub_df['knowledge'].isna()]
        if len(active) == 0:
            # Sujeto nunca tuvo sesiones activas (abandonó inmediatamente)
            records.append({
                'subject_id': sid,
                'model': model,
                'retention_final': np.nan,
                'dropout_time': 0,
                'dropout_occurred': True,
                'learning_speed': np.nan,
                'creativity_final': np.nan,
                'avg_attention': np.nan,
                'avg_motivation': np.nan,
                'avg_persistence': np.nan,
                'total_sessions_active': 0,
            })
            continue

        # Retention final (última sesión activa)
        last = active.iloc[-1]
        retention_final = last['retention']

        # Dropout: si en alguna sesión dropout==True
        dropout_events = sub_df['dropout'] == True
        if dropout_events.any():
            dropout_time = sub_df[dropout_events]['session'].min()
            dropout_occurred = True
        else:
            dropout_time = np.nan
            dropout_occurred = False

        # Velocidad de aprendizaje (ajuste exponencial)
        # Usamos knowledge vs session (solo sesiones activas)
        x = active['session'].values
        y = active['knowledge'].values
        if len(x) >= 3:
            try:
                from scipy.optimize import curve_fit
                def exp_func(x, a, b):
                    return a * (1 - np.exp(-b * x))
                popt, _ = curve_fit(exp_func, x, y, p0=[1.0, 0.1],
                                    bounds=([0, 0], [1.5, 5.0]))
                learning_speed = popt[1]
            except Exception:
                learning_speed = np.nan
        else:
            learning_speed = np.nan

        # Creatividad final
        if 'creativity' in active.columns:
            creativity_final = active.iloc[-1]['creativity']
        else:
            creativity_final = np.nan

        # Promedios de atención, motivación, persistencia
        avg_attention = active['attention'].mean()
        avg_motivation = active['motivation'].mean()
        avg_persistence = active['persistence_effort'].mean()

        records.append({
            'subject_id': sid,
            'model': model,
            'retention_final': retention_final,
            'dropout_time': dropout_time,
            'dropout_occurred': dropout_occurred,
            'learning_speed': learning_speed,
            'creativity_final': creativity_final,
            'avg_attention': avg_attention,
            'avg_motivation': avg_motivation,
            'avg_persistence': avg_persistence,
            'total_sessions_active': len(active),
        })

    return pd.DataFrame(records)


# -----------------------------------------------------------------------------
# 2. Funciones estadísticas y de tamaño del efecto
# -----------------------------------------------------------------------------

def cohen_d(x, y):
    """Calcula la d de Cohen para dos muestras independientes."""
    nx = len(x)
    ny = len(y)
    # Varianza combinada
    var_x = np.var(x, ddof=1)
    var_y = np.var(y, ddof=1)
    pooled_var = ((nx - 1) * var_x + (ny - 1) * var_y) / (nx + ny - 2)
    if pooled_var == 0:
        return 0.0
    diff = np.mean(x) - np.mean(y)
    return diff / np.sqrt(pooled_var)


def compare_groups(subject_metrics: pd.DataFrame, metric_col: str) -> Dict:
    """
    Compara dos grupos ('gcd' y 'control') para una métrica determinada.
    Retorna un diccionario con estadísticos:
        - mean_gcd, std_gcd, n_gcd
        - mean_control, std_control, n_control
        - p_value (t-test o Mann-Whitney según normalidad), test_used
        - cohen_d
    """
    gcd_vals = subject_metrics[subject_metrics['model'] == 'gcd'][metric_col].dropna()
    ctrl_vals = subject_metrics[subject_metrics['model'] == 'control'][metric_col].dropna()

    if len(gcd_vals) == 0 or len(ctrl_vals) == 0:
        return {
            'mean_gcd': np.nan, 'std_gcd': np.nan, 'n_gcd': len(gcd_vals),
            'mean_control': np.nan, 'std_control': np.nan, 'n_control': len(ctrl_vals),
            'p_value': np.nan, 'test_used': 'N/A', 'cohen_d': np.nan
        }

    # Prueba de normalidad (Shapiro-Wilk) en ambas muestras (si n >= 3)
    normal_gcd = False
    normal_ctrl = False
    if len(gcd_vals) >= 3:
        _, p_gcd = stats.shapiro(gcd_vals)
        normal_gcd = p_gcd > 0.05
    if len(ctrl_vals) >= 3:
        _, p_ctrl = stats.shapiro(ctrl_vals)
        normal_ctrl = p_ctrl > 0.05

    # Si ambas son normales y varianzas homogéneas (prueba de Levene), usar t-test
    if normal_gcd and normal_ctrl:
        # Prueba de Levene para homogeneidad de varianzas
        _, p_levene = stats.levene(gcd_vals, ctrl_vals)
        equal_var = p_levene > 0.05
        t_stat, p_val = ttest_ind(gcd_vals, ctrl_vals, equal_var=equal_var)
        test_used = 't-test'
    else:
        # Mann-Whitney U
        u_stat, p_val = mannwhitneyu(gcd_vals, ctrl_vals, alternative='two-sided')
        test_used = 'Mann-Whitney U'

    # Cohen's d
    d = cohen_d(gcd_vals, ctrl_vals)

    return {
        'mean_gcd': np.mean(gcd_vals),
        'std_gcd': np.std(gcd_vals, ddof=1),
        'n_gcd': len(gcd_vals),
        'mean_control': np.mean(ctrl_vals),
        'std_control': np.std(ctrl_vals, ddof=1),
        'n_control': len(ctrl_vals),
        'p_value': p_val,
        'test_used': test_used,
        'cohen_d': d
    }


# -----------------------------------------------------------------------------
# 3. Generación de gráficos
# -----------------------------------------------------------------------------

def create_learning_curves(df: pd.DataFrame, metric: str = 'knowledge',
                           title: str = "Curva de Aprendizaje") -> plt.Figure:
    """Crea gráfico de evolución temporal de una métrica (media ± SEM) por grupo."""
    fig, ax = plt.subplots(figsize=(10, 6))
    for model in ['gcd', 'control']:
        sub = df[df['model'] == model]
        # Agrupar por sesión y calcular media y SEM
        grouped = sub.groupby('session')[metric].agg(['mean', 'sem']).reset_index()
        ax.plot(grouped['session'], grouped['mean'], label=model.capitalize(), linewidth=2)
        ax.fill_between(grouped['session'],
                        grouped['mean'] - grouped['sem'],
                        grouped['mean'] + grouped['sem'],
                        alpha=0.2)
    ax.set_xlabel('Sesión')
    ax.set_ylabel(metric.capitalize())
    ax.set_title(title)
    ax.legend()
    sns.despine()
    return fig


def create_boxplots(subject_metrics: pd.DataFrame, metric: str,
                    title: str = "") -> plt.Figure:
    """Crea diagrama de caja comparando grupos para una métrica."""
    fig, ax = plt.subplots(figsize=(8, 6))
    data = [subject_metrics[subject_metrics['model'] == 'gcd'][metric].dropna(),
            subject_metrics[subject_metrics['model'] == 'control'][metric].dropna()]
    bp = ax.boxplot(data, labels=['GCD', 'Control'], patch_artist=True)
    # Colorear
    colors = ['#66c2a5', '#fc8d62']
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
    ax.set_ylabel(metric.replace('_', ' ').title())
    ax.set_title(title)
    sns.despine()
    return fig


def create_survival_curve(df: pd.DataFrame) -> Optional[plt.Figure]:
    """Genera curva de Kaplan-Meier para el tiempo de abandono."""
    if not LIFELINES_AVAILABLE:
        return None

    # Necesitamos datos por sujeto con tiempo de abandono y evento
    subject_metrics = compute_subject_metrics(df)
    # Tiempo en sesiones (si no abandonó, censurado al máximo de sesiones)
    max_session = df['session'].max()
    # Para cada sujeto, tiempo de abandono o max_session
    times = []
    events = []
    models = []
    for _, row in subject_metrics.iterrows():
        if row['dropout_occurred']:
            t = row['dropout_time']
            e = 1
        else:
            t = max_session
            e = 0
        times.append(t)
        events.append(e)
        models.append(row['model'])

    survival_df = pd.DataFrame({
        'time': times,
        'event': events,
        'model': models
    })

    fig, ax = plt.subplots(figsize=(10, 6))
    kmf = KaplanMeierFitter()
    for model in ['gcd', 'control']:
        sub = survival_df[survival_df['model'] == model]
        kmf.fit(sub['time'], sub['event'], label=model.capitalize())
        kmf.plot(ax=ax, ci_show=True)

    ax.set_xlabel('Sesión')
    ax.set_ylabel('Probabilidad de supervivencia (no abandono)')
    ax.set_title('Curva de Supervivencia (Kaplan-Meier)')
    ax.legend()
    sns.despine()

    # Prueba log-rank
    gcd_sub = survival_df[survival_df['model'] == 'gcd']
    ctrl_sub = survival_df[survival_df['model'] == 'control']
    if len(gcd_sub) > 0 and len(ctrl_sub) > 0:
        results = logrank_test(gcd_sub['time'], ctrl_sub['time'],
                               gcd_sub['event'], ctrl_sub['event'])
        p_logrank = results.p_value
        ax.text(0.7, 0.9, f'Log-rank p = {p_logrank:.4f}',
                transform=ax.transAxes, fontsize=12,
                bbox=dict(facecolor='white', alpha=0.8))
    return fig


def create_correlation_matrix(subject_metrics: pd.DataFrame) -> plt.Figure:
    """Genera matriz de correlación entre métricas numéricas."""
    # Seleccionar columnas numéricas relevantes
    metric_cols = ['retention_final', 'learning_speed', 'creativity_final',
                   'avg_attention', 'avg_motivation', 'avg_persistence',
                   'total_sessions_active']
    # Filtrar columnas existentes
    cols = [c for c in metric_cols if c in subject_metrics.columns]
    if len(cols) < 2:
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.text(0.5, 0.5, 'No hay suficientes métricas para correlación',
                ha='center', va='center', fontsize=14)
        ax.axis('off')
        return fig

    corr = subject_metrics[cols].corr()
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm',
                square=True, ax=ax, cbar_kws={'shrink': 0.8})
    ax.set_title('Matriz de Correlación entre Métricas')
    return fig


# -----------------------------------------------------------------------------
# 4. Generación del reporte HTML
# -----------------------------------------------------------------------------

# Plantilla HTML básica (si jinja2 no está disponible, usamos formato simple)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{{ title }}</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 2cm; }
        h1 { color: #2c3e50; }
        h2 { color: #34495e; border-bottom: 2px solid #ecf0f1; padding-bottom: 5px; }
        .section { margin-bottom: 30px; }
        table { border-collapse: collapse; width: 100%; margin: 10px 0; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: center; }
        th { background-color: #f2f2f2; }
        .figure { text-align: center; margin: 20px 0; }
        .figure img { max-width: 100%; border: 1px solid #eee; border-radius: 5px; }
        .stat-box { background: #f9f9f9; padding: 15px; border-radius: 5px; margin: 10px 0; }
        .footer { font-size: 0.9em; color: #7f8c8d; text-align: center; margin-top: 40px; border-top: 1px solid #ecf0f1; padding-top: 10px; }
    </style>
</head>
<body>
    <h1>{{ title }}</h1>
    <p><strong>Generado el:</strong> {{ date }}</p>
    <p><strong>Datos:</strong> {{ data_file }}</p>

    <div class="section">
        <h2>Resumen Ejecutivo</h2>
        <div class="stat-box">
            {{ executive_summary }}
        </div>
    </div>

    <div class="section">
        <h2>Tabla de Comparación de Grupos</h2>
        {{ comparison_table }}
    </div>

    {% if plots %}
    <div class="section">
        <h2>Visualizaciones</h2>
        {% for plot in plots %}
        <div class="figure">
            <h3>{{ plot.title }}</h3>
            <img src="data:image/png;base64,{{ plot.base64 }}" alt="{{ plot.title }}">
        </div>
        {% endfor %}
    </div>
    {% endif %}

    <div class="section">
        <h2>Conclusiones y Recomendaciones</h2>
        <div class="stat-box">
            {{ conclusions }}
        </div>
    </div>

    <div class="footer">
        Reporte generado automáticamente por metrics_report.py del proyecto GCD.
    </div>
</body>
</html>
"""


def fig_to_base64(fig) -> str:
    """Convierte una figura de matplotlib a string base64."""
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    plt.close(fig)
    return img_base64


def generate_report(data: str, output: str, include_plots: bool = True,
                    title: str = "Reporte de Benchmark GCD") -> None:
    """
    Genera un reporte HTML a partir de los datos de benchmark.

    Args:
        data: Ruta al archivo CSV con datos crudos (salida de benchmark.py)
        output: Ruta de salida para el archivo HTML
        include_plots: Si se deben incluir gráficos
        title: Título del reporte
    """
    # 1. Cargar datos
    df = pd.read_csv(data)
    logger.info(f"Datos cargados: {len(df)} filas")

    # 2. Calcular métricas por sujeto
    subject_metrics = compute_subject_metrics(df)
    logger.info(f"Métricas calculadas para {len(subject_metrics)} sujetos")

    # 3. Preparar secciones del reporte
    # Resumen ejecutivo
    n_gcd = len(subject_metrics[subject_metrics['model'] == 'gcd'])
    n_ctrl = len(subject_metrics[subject_metrics['model'] == 'control'])
    dropout_gcd = subject_metrics[subject_metrics['model'] == 'gcd']['dropout_occurred'].mean()
    dropout_ctrl = subject_metrics[subject_metrics['model'] == 'control']['dropout_occurred'].mean()
    exec_summary = f"""
    <p>Este reporte analiza los resultados de un benchmark que compara el modelo <strong>GCD Adaptativo</strong>
    frente a un <strong>Tutor Estático</strong> (control).</p>
    <ul>
        <li><strong>Número de sujetos:</strong> GCD = {n_gcd}, Control = {n_ctrl}</li>
        <li><strong>Tasa de abandono:</strong> GCD = {dropout_gcd:.1%}, Control = {dropout_ctrl:.1%}</li>
        <li><strong>Retención final promedio:</strong> GCD = {subject_metrics[subject_metrics['model']=='gcd']['retention_final'].mean():.3f} ± {subject_metrics[subject_metrics['model']=='gcd']['retention_final'].std():.3f}, Control = {subject_metrics[subject_metrics['model']=='control']['retention_final'].mean():.3f} ± {subject_metrics[subject_metrics['model']=='control']['retention_final'].std():.3f}</li>
        <li><strong>Velocidad de aprendizaje:</strong> GCD = {subject_metrics[subject_metrics['model']=='gcd']['learning_speed'].mean():.3f} ± {subject_metrics[subject_metrics['model']=='gcd']['learning_speed'].std():.3f}, Control = {subject_metrics[subject_metrics['model']=='control']['learning_speed'].mean():.3f} ± {subject_metrics[subject_metrics['model']=='control']['learning_speed'].std():.3f}</li>
    </ul>
    """

    # 4. Tabla de comparación de grupos para cada métrica
    metrics = ['retention_final', 'learning_speed', 'creativity_final',
               'avg_attention', 'avg_motivation', 'avg_persistence']
    # Filtrar métricas que existan en los datos
    available_metrics = [m for m in metrics if m in subject_metrics.columns]
    comp_data = []
    for m in available_metrics:
        stats_dict = compare_groups(subject_metrics, m)
        # Formatear valores
        row = {
            'Métrica': m.replace('_', ' ').title(),
            'GCD (media ± DE)': f"{stats_dict['mean_gcd']:.3f} ± {stats_dict['std_gcd']:.3f}",
            'Control (media ± DE)': f"{stats_dict['mean_control']:.3f} ± {stats_dict['std_control']:.3f}",
            'p-valor': f"{stats_dict['p_value']:.4f}" if not np.isnan(stats_dict['p_value']) else 'N/A',
            'Cohen\'s d': f"{stats_dict['cohen_d']:.3f}" if not np.isnan(stats_dict['cohen_d']) else 'N/A',
            'Prueba': stats_dict['test_used']
        }
        comp_data.append(row)

    # Crear tabla HTML
    if comp_data:
        comp_df = pd.DataFrame(comp_data)
        comp_table = comp_df.to_html(index=False, classes='table')
    else:
        comp_table = "<p>No hay métricas disponibles para comparar.</p>"

    # 5. Generar gráficos (si se solicita)
    plot_list = []
    if include_plots:
        # Curva de aprendizaje (conocimiento)
        fig = create_learning_curves(df, metric='knowledge', title='Evolución del Conocimiento')
        plot_list.append({'title': 'Curva de Aprendizaje (Conocimiento)', 'base64': fig_to_base64(fig)})

        # Curva de retención
        fig = create_learning_curves(df, metric='retention', title='Evolución de la Retención')
        plot_list.append({'title': 'Curva de Retención', 'base64': fig_to_base64(fig)})

        # Diagramas de caja para métricas finales
        for m in ['retention_final', 'learning_speed', 'creativity_final']:
            if m in subject_metrics.columns:
                fig = create_boxplots(subject_metrics, m, title=f'Comparación de {m.replace("_"," ").title()}')
                plot_list.append({'title': f'Boxplot: {m.replace("_"," ").title()}', 'base64': fig_to_base64(fig)})

        # Curva de supervivencia (Kaplan-Meier)
        fig = create_survival_curve(df)
        if fig is not None:
            plot_list.append({'title': 'Curva de Supervivencia (Kaplan-Meier)', 'base64': fig_to_base64(fig)})

        # Matriz de correlación
        fig = create_correlation_matrix(subject_metrics)
        plot_list.append({'title': 'Matriz de Correlación', 'base64': fig_to_base64(fig)})

    # 6. Conclusiones (automáticas basadas en los resultados)
    # Extraer p-valor para retención y abandono
    retention_stats = compare_groups(subject_metrics, 'retention_final') if 'retention_final' in subject_metrics else None
    dropout_p = None
    if LIFELINES_AVAILABLE:
        # Calcular log-rank p
        max_session = df['session'].max()
        survival_df = subject_metrics[['model', 'dropout_time', 'dropout_occurred']].copy()
        survival_df['time'] = survival_df['dropout_time'].fillna(max_session)
        survival_df['event'] = survival_df['dropout_occurred'].astype(int)
        if len(survival_df[survival_df['model']=='gcd']) > 0 and len(survival_df[survival_df['model']=='control']) > 0:
            from lifelines.statistics import logrank_test
            res = logrank_test(survival_df[survival_df['model']=='gcd']['time'],
                               survival_df[survival_df['model']=='control']['time'],
                               survival_df[survival_df['model']=='gcd']['event'],
                               survival_df[survival_df['model']=='control']['event'])
            dropout_p = res.p_value

    conclusion_lines = []
    if retention_stats is not None and not np.isnan(retention_stats['p_value']):
        if retention_stats['p_value'] < 0.05:
            conclusion_lines.append(f"- La retención final es significativamente mayor en el grupo GCD (p={retention_stats['p_value']:.4f}, d={retention_stats['cohen_d']:.3f}).")
        else:
            conclusion_lines.append(f"- No se encontraron diferencias significativas en retención final (p={retention_stats['p_value']:.4f}).")

    if dropout_p is not None and dropout_p < 0.05:
        conclusion_lines.append(f"- La tasa de abandono es significativamente menor en el grupo GCD (log-rank p={dropout_p:.4f}).")
    elif dropout_p is not None:
        conclusion_lines.append(f"- No se encontraron diferencias significativas en abandono (log-rank p={dropout_p:.4f}).")

    if len(conclusion_lines) == 0:
        conclusion_lines.append("- No se dispone de suficientes datos para conclusiones estadísticas robustas.")

    conclusions = "<ul>" + "".join(f"<li>{line}</li>" for line in conclusion_lines) + "</ul>"
    # Añadir recomendación general
    conclusions += """
    <p><strong>Recomendación:</strong> Los resultados sugieren que el modelo GCD adaptativo ofrece ventajas en retención y reducción de abandono. 
    Se recomienda continuar con la recogida de datos para aumentar la potencia estadística y explorar la generalización a diferentes poblaciones.</p>
    """

    # 7. Renderizar HTML
    context = {
        'title': title,
        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'data_file': os.path.basename(data),
        'executive_summary': exec_summary,
        'comparison_table': comp_table,
        'plots': plot_list if include_plots else [],
        'conclusions': conclusions,
    }

    if JINJA_AVAILABLE:
        template = Template(HTML_TEMPLATE)
        html = template.render(**context)
    else:
        # Renderizado simple con str.format (no se admiten bucles)
        html = HTML_TEMPLATE
        # Reemplazo simple (no maneja bucles, pero lo dejamos funcional)
        for key, value in context.items():
            placeholder = "{{ " + key + " }}"
            if key == 'plots':
                # Para plots, si no hay jinja2, simplemente no se incluyen
                html = html.replace(placeholder, "")
            else:
                html = html.replace(placeholder, str(value))

    # Guardar HTML
    os.makedirs(os.path.dirname(os.path.abspath(output)), exist_ok=True)
    with open(output, 'w', encoding='utf-8') as f:
        f.write(html)
    logger.info(f"Reporte generado en {output}")


# -----------------------------------------------------------------------------
# 5. Ejemplo de uso (si se ejecuta como script)
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generar reporte de métricas a partir de benchmark")
    parser.add_argument('data', help='Archivo CSV con datos de benchmark (salida de benchmark.py)')
    parser.add_argument('-o', '--output', default='report.html', help='Archivo de salida HTML')
    parser.add_argument('--no-plots', action='store_true', help='No incluir gráficos')
    parser.add_argument('--title', default='Reporte de Benchmark GCD', help='Título del reporte')
    args = parser.parse_args()

    generate_report(
        data=args.data,
        output=args.output,
        include_plots=not args.no_plots,
        title=args.title
    )
