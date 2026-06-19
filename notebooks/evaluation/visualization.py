#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
visualization.py - Módulo de Visualización para GCD

Propósito:
    Proporcionar funciones modulares para generar gráficos estándar utilizados
    en el análisis de datos del proyecto GCD. Todas las funciones devuelven
    figuras de matplotlib para su integración con el pipeline de reportes.

Funciones principales:
    - plot_learning_curve: Curvas de aprendizaje (media ± SEM) por grupo.
    - plot_boxplot: Diagrama de caja (opcional con puntos).
    - plot_violinplot: Diagrama de violín.
    - plot_correlation_matrix: Matriz de correlación (heatmap).
    - plot_survival_curve: Curva de Kaplan-Meier (requiere lifelines).
    - plot_scatter: Gráfico de dispersión con línea de regresión.
    - plot_radar: Gráfico de radar para comparar múltiples dimensiones.
    - plot_bar_comparison: Gráfico de barras con barras de error.

Todas las funciones aceptan parámetros de personalización (título, etiquetas,
paleta de colores, guardado automático) y devuelven (fig, ax).

Uso típico:
    from evaluation.visualization import plot_learning_curve
    fig, ax = plot_learning_curve(df, x='session', y='knowledge', group='model')
    fig.savefig('learning_curve.png', dpi=300)
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Optional, List, Tuple, Dict, Union
import warnings
from scipy import stats

# Configuración de estilo por defecto
sns.set_style("whitegrid")
sns.set_palette("Set2")

# Colores personalizados para grupos (GCD vs Control)
COLORS_GCD = {'gcd': '#66c2a5', 'control': '#fc8d62'}
DEFAULT_PALETTE = sns.color_palette("Set2")

# =============================================================================
# 1. Curvas de aprendizaje
# =============================================================================

def plot_learning_curve(
    data: pd.DataFrame,
    x_col: str,
    y_col: str,
    group_col: str,
    title: str = "",
    xlabel: str = "",
    ylabel: str = "",
    palette: Optional[Dict[str, str]] = None,
    show_sem: bool = True,
    figsize: Tuple[int, int] = (10, 6),
    save_path: Optional[str] = None,
    dpi: int = 150,
    **kwargs
) -> Tuple[plt.Figure, plt.Axes]:
    """
    Dibuja curvas de aprendizaje (media ± SEM) agrupadas por una variable.

    Args:
        data: DataFrame con los datos.
        x_col: Nombre de la columna para el eje X (ej. 'session').
        y_col: Nombre de la columna para el eje Y (ej. 'knowledge').
        group_col: Nombre de la columna para agrupar (ej. 'model').
        title: Título del gráfico.
        xlabel: Etiqueta del eje X (si vacío, usa x_col).
        ylabel: Etiqueta del eje Y (si vacío, usa y_col).
        palette: Diccionario con colores para cada grupo (ej. {'gcd':'#66c2a5', ...}).
        show_sem: Si se muestra la banda de error estándar.
        figsize: Tamaño de la figura.
        save_path: Ruta para guardar la figura (opcional).
        dpi: Resolución para guardar.
        **kwargs: Parámetros adicionales para ax.plot.

    Returns:
        fig, ax: Objetos de matplotlib.
    """
    fig, ax = plt.subplots(figsize=figsize)

    groups = data[group_col].unique()
    if palette is None:
        # Usar colores por defecto para 'gcd' y 'control'
        palette = {}
        for g in groups:
            if g.lower() in COLORS_GCD:
                palette[g] = COLORS_GCD[g.lower()]
            else:
                palette[g] = None

    for group in groups:
        sub = data[data[group_col] == group]
        # Agrupar por x_col y calcular media y SEM
        grouped = sub.groupby(x_col)[y_col].agg(['mean', 'sem', 'count']).reset_index()
        x_vals = grouped[x_col]
        y_mean = grouped['mean']
        y_sem = grouped['sem']
        color = palette.get(group, None)

        ax.plot(x_vals, y_mean, label=group.capitalize(), color=color, linewidth=2,
                marker='o', markersize=6, **kwargs)
        if show_sem:
            ax.fill_between(x_vals, y_mean - y_sem, y_mean + y_sem,
                            alpha=0.2, color=color)

    ax.set_xlabel(xlabel if xlabel else x_col)
    ax.set_ylabel(ylabel if ylabel else y_col)
    ax.set_title(title if title else f'{y_col} by {x_col}')
    ax.legend()
    sns.despine()

    if save_path:
        fig.savefig(save_path, dpi=dpi, bbox_inches='tight')
        plt.close(fig)  # Opcional: cerrar para liberar memoria

    return fig, ax


# =============================================================================
# 2. Diagrama de caja
# =============================================================================

def plot_boxplot(
    data: pd.DataFrame,
    x_col: str,
    y_col: str,
    group_col: Optional[str] = None,
    title: str = "",
    xlabel: str = "",
    ylabel: str = "",
    palette: Optional[Dict[str, str]] = None,
    show_points: bool = True,
    figsize: Tuple[int, int] = (8, 6),
    save_path: Optional[str] = None,
    dpi: int = 150,
    **kwargs
) -> Tuple[plt.Figure, plt.Axes]:
    """
    Dibuja diagrama de caja, con posibilidad de agrupar por una variable.

    Args:
        data: DataFrame.
        x_col: Columna para el eje X (categórica).
        y_col: Columna para el eje Y (continua).
        group_col: Si se especifica, se usa como hue (agrupación dentro de x).
        title, xlabel, ylabel: Títulos y etiquetas.
        palette: Diccionario de colores para los grupos.
        show_points: Si se superponen puntos (strip plot).
        figsize: Tamaño.
        save_path: Ruta para guardar.
        dpi: Resolución.

    Returns:
        fig, ax
    """
    fig, ax = plt.subplots(figsize=figsize)

    if group_col:
        # Gráfico con hue
        sns.boxplot(data=data, x=x_col, y=y_col, hue=group_col,
                    palette=palette, ax=ax, **kwargs)
        if show_points:
            sns.stripplot(data=data, x=x_col, y=y_col, hue=group_col,
                          palette=palette, dodge=True, alpha=0.5, ax=ax)
        # Mover leyenda si está solapada
        ax.legend(title=group_col)
    else:
        # Gráfico simple
        sns.boxplot(data=data, x=x_col, y=y_col, palette=palette, ax=ax, **kwargs)
        if show_points:
            sns.stripplot(data=data, x=x_col, y=y_col, palette=palette,
                          alpha=0.5, ax=ax)

    ax.set_xlabel(xlabel if xlabel else x_col)
    ax.set_ylabel(ylabel if ylabel else y_col)
    ax.set_title(title)
    sns.despine()

    if save_path:
        fig.savefig(save_path, dpi=dpi, bbox_inches='tight')

    return fig, ax


def plot_violinplot(
    data: pd.DataFrame,
    x_col: str,
    y_col: str,
    group_col: Optional[str] = None,
    title: str = "",
    xlabel: str = "",
    ylabel: str = "",
    palette: Optional[Dict[str, str]] = None,
    show_points: bool = True,
    figsize: Tuple[int, int] = (8, 6),
    save_path: Optional[str] = None,
    dpi: int = 150,
    **kwargs
) -> Tuple[plt.Figure, plt.Axes]:
    """
    Diagrama de violín (similar a boxplot pero con densidad).

    Parámetros similares a plot_boxplot.
    """
    fig, ax = plt.subplots(figsize=figsize)

    if group_col:
        sns.violinplot(data=data, x=x_col, y=y_col, hue=group_col,
                       palette=palette, split=False, ax=ax, **kwargs)
        if show_points:
            sns.stripplot(data=data, x=x_col, y=y_col, hue=group_col,
                          palette=palette, dodge=True, alpha=0.4, ax=ax)
        ax.legend(title=group_col)
    else:
        sns.violinplot(data=data, x=x_col, y=y_col, palette=palette, ax=ax, **kwargs)
        if show_points:
            sns.stripplot(data=data, x=x_col, y=y_col, palette=palette,
                          alpha=0.4, ax=ax)

    ax.set_xlabel(xlabel if xlabel else x_col)
    ax.set_ylabel(ylabel if ylabel else y_col)
    ax.set_title(title)
    sns.despine()

    if save_path:
        fig.savefig(save_path, dpi=dpi, bbox_inches='tight')

    return fig, ax


# =============================================================================
# 3. Matriz de correlación (heatmap)
# =============================================================================

def plot_correlation_matrix(
    data: pd.DataFrame,
    columns: Optional[List[str]] = None,
    title: str = "Matriz de Correlación",
    method: str = 'pearson',
    annot: bool = True,
    fmt: str = '.2f',
    cmap: str = 'coolwarm',
    figsize: Tuple[int, int] = (10, 8),
    save_path: Optional[str] = None,
    dpi: int = 150,
    **kwargs
) -> Tuple[plt.Figure, plt.Axes]:
    """
    Dibuja un heatmap de correlación.

    Args:
        data: DataFrame.
        columns: Lista de columnas a incluir (si None, se usan todas las numéricas).
        title: Título.
        method: 'pearson' o 'spearman'.
        annot: Mostrar valores.
        fmt: Formato de los valores.
        cmap: Mapa de colores.
        figsize: Tamaño.
        save_path: Ruta para guardar.
        dpi: Resolución.
        **kwargs: adicionales para sns.heatmap.

    Returns:
        fig, ax
    """
    if columns is None:
        # Seleccionar columnas numéricas
        columns = data.select_dtypes(include=[np.number]).columns.tolist()
    corr = data[columns].corr(method=method)
    fig, ax = plt.subplots(figsize=figsize)
    sns.heatmap(corr, annot=annot, fmt=fmt, cmap=cmap, ax=ax,
                square=True, cbar_kws={'shrink': 0.8}, **kwargs)
    ax.set_title(title)
    if save_path:
        fig.savefig(save_path, dpi=dpi, bbox_inches='tight')
    return fig, ax


# =============================================================================
# 4. Curva de supervivencia (Kaplan-Meier)
# =============================================================================

def plot_survival_curve(
    df: pd.DataFrame,
    time_col: str,
    event_col: str,
    group_col: Optional[str] = None,
    title: str = "Curva de Supervivencia",
    xlabel: str = "Tiempo",
    ylabel: str = "Probabilidad de supervivencia",
    palette: Optional[Dict[str, str]] = None,
    figsize: Tuple[int, int] = (10, 6),
    save_path: Optional[str] = None,
    dpi: int = 150,
    **kwargs
) -> Tuple[plt.Figure, plt.Axes]:
    """
    Dibuja curvas de Kaplan-Meier usando lifelines. Si lifelines no está
    instalado, lanza un ImportError.

    Args:
        df: DataFrame con columnas de tiempo, evento y grupo.
        time_col: Columna con el tiempo hasta evento o censura.
        event_col: Columna binaria (1=evento, 0=censura).
        group_col: Columna para agrupar (opcional, si no, una sola curva).
        title, xlabel, ylabel: Títulos.
        palette: Diccionario de colores.
        figsize: Tamaño.
        save_path: Ruta para guardar.
        dpi: Resolución.

    Returns:
        fig, ax
    """
    try:
        from lifelines import KaplanMeierFitter
        from lifelines.statistics import logrank_test
    except ImportError:
        raise ImportError("lifelines es necesario para curvas de supervivencia. Instálelo con: pip install lifelines")

    fig, ax = plt.subplots(figsize=figsize)
    kmf = KaplanMeierFitter()

    if group_col:
        groups = df[group_col].unique()
        if palette is None:
            palette = {g: COLORS_GCD.get(g.lower(), None) for g in groups}
        for group in groups:
            sub = df[df[group_col] == group]
            kmf.fit(sub[time_col], sub[event_col], label=group.capitalize())
            kmf.plot(ax=ax, color=palette.get(group), **kwargs)
        # Log-rank test
        if len(groups) == 2:
            g1 = df[df[group_col] == groups[0]]
            g2 = df[df[group_col] == groups[1]]
            result = logrank_test(g1[time_col], g2[time_col],
                                  g1[event_col], g2[event_col])
            p_val = result.p_value
            ax.text(0.7, 0.9, f'Log-rank p = {p_val:.4f}',
                    transform=ax.transAxes, fontsize=12,
                    bbox=dict(facecolor='white', alpha=0.8))
    else:
        kmf.fit(df[time_col], df[event_col], label='Todos')
        kmf.plot(ax=ax, **kwargs)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend()
    sns.despine()

    if save_path:
        fig.savefig(save_path, dpi=dpi, bbox_inches='tight')

    return fig, ax


# =============================================================================
# 5. Gráfico de dispersión con regresión
# =============================================================================

def plot_scatter(
    data: pd.DataFrame,
    x_col: str,
    y_col: str,
    hue_col: Optional[str] = None,
    title: str = "",
    xlabel: str = "",
    ylabel: str = "",
    add_regression: bool = True,
    palette: Optional[Dict[str, str]] = None,
    figsize: Tuple[int, int] = (8, 6),
    save_path: Optional[str] = None,
    dpi: int = 150,
    **kwargs
) -> Tuple[plt.Figure, plt.Axes]:
    """
    Gráfico de dispersión, con opción de línea de regresión y agrupación.

    Args:
        data: DataFrame.
        x_col: Columna para eje X.
        y_col: Columna para eje Y.
        hue_col: Columna para colorear puntos (opcional).
        title, xlabel, ylabel: Títulos.
        add_regression: Añadir línea de regresión (si hue_col es None, una sola; si hay hue, una por grupo).
        palette: Colores para hue.
        figsize: Tamaño.
        save_path: Ruta para guardar.

    Returns:
        fig, ax
    """
    fig, ax = plt.subplots(figsize=figsize)

    if hue_col:
        # Dispersión con hue
        sns.scatterplot(data=data, x=x_col, y=y_col, hue=hue_col,
                        palette=palette, ax=ax, **kwargs)
        if add_regression:
            for group in data[hue_col].unique():
                sub = data[data[hue_col] == group]
                if len(sub) > 1:
                    try:
                        slope, intercept = np.polyfit(sub[x_col], sub[y_col], 1)
                        x_vals = np.linspace(sub[x_col].min(), sub[x_col].max(), 100)
                        y_vals = slope * x_vals + intercept
                        color = palette.get(group) if palette else None
                        ax.plot(x_vals, y_vals, '--', linewidth=1.5, color=color,
                                alpha=0.7, label=f'{group} (regression)')
                    except:
                        pass
    else:
        # Dispersión simple
        sns.scatterplot(data=data, x=x_col, y=y_col, ax=ax, **kwargs)
        if add_regression:
            if len(data) > 1:
                slope, intercept = np.polyfit(data[x_col], data[y_col], 1)
                x_vals = np.linspace(data[x_col].min(), data[x_col].max(), 100)
                y_vals = slope * x_vals + intercept
                ax.plot(x_vals, y_vals, 'r--', linewidth=2, label='Regresión')
                # Añadir R²
                r, p = stats.pearsonr(data[x_col], data[y_col])
                ax.text(0.7, 0.9, f'R² = {r**2:.3f}', transform=ax.transAxes,
                        fontsize=12, bbox=dict(facecolor='white', alpha=0.8))

    ax.set_xlabel(xlabel if xlabel else x_col)
    ax.set_ylabel(ylabel if ylabel else y_col)
    ax.set_title(title)
    ax.legend()
    sns.despine()

    if save_path:
        fig.savefig(save_path, dpi=dpi, bbox_inches='tight')

    return fig, ax


# =============================================================================
# 6. Gráfico de radar (para comparar múltiples dimensiones)
# =============================================================================

def plot_radar(
    data: Dict[str, Dict[str, float]],
    categories: List[str],
    title: str = "Comparativa por dimensiones",
    colors: Optional[List[str]] = None,
    figsize: Tuple[int, int] = (8, 8),
    save_path: Optional[str] = None,
    dpi: int = 150
) -> Tuple[plt.Figure, plt.Axes]:
    """
    Genera un gráfico de radar para comparar varios grupos en múltiples categorías.

    Args:
        data: Diccionario {grupo: {categoria: valor}}.
        categories: Lista de nombres de categorías (orden).
        title: Título.
        colors: Lista de colores para los grupos.
        figsize: Tamaño.
        save_path: Ruta para guardar.

    Returns:
        fig, ax (proyección polar)
    """
    import math

    N = len(categories)
    angles = [n / float(N) * 2 * math.pi for n in range(N)]
    angles += angles[:1]  # cerrar el polígono

    fig, ax = plt.subplots(figsize=figsize, subplot_kw=dict(polar=True))

    if colors is None:
        colors = sns.color_palette("Set2", len(data))

    for i, (group, values) in enumerate(data.items()):
        # Extraer valores en el orden de categories
        vals = [values.get(cat, 0) for cat in categories]
        vals += vals[:1]  # cerrar
        ax.plot(angles, vals, 'o-', linewidth=2, label=group, color=colors[i])
        ax.fill(angles, vals, alpha=0.1, color=colors[i])

    # Etiquetas de categorías
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)
    ax.set_title(title, size=16, y=1.1)
    ax.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))

    if save_path:
        fig.savefig(save_path, dpi=dpi, bbox_inches='tight')

    return fig, ax


# =============================================================================
# 7. Gráfico de barras con barras de error
# =============================================================================

def plot_bar_comparison(
    data: pd.DataFrame,
    x_col: str,
    y_col: str,
    group_col: Optional[str] = None,
    title: str = "",
    xlabel: str = "",
    ylabel: str = "",
    palette: Optional[Dict[str, str]] = None,
    error_type: str = 'sem',  # 'sem', 'sd', 'ci'
    ci: float = 0.95,
    figsize: Tuple[int, int] = (8, 6),
    save_path: Optional[str] = None,
    dpi: int = 150,
    **kwargs
) -> Tuple[plt.Figure, plt.Axes]:
    """
    Gráfico de barras para comparar medias con barras de error.

    Args:
        data: DataFrame.
        x_col: Columna categórica para el eje X.
        y_col: Columna continua para el eje Y.
        group_col: Columna para agrupar (hue).
        title, xlabel, ylabel: Títulos.
        palette: Colores para grupos.
        error_type: 'sem', 'sd', o 'ci' (intervalo de confianza).
        ci: Nivel de confianza si error_type='ci'.
        figsize: Tamaño.
        save_path: Ruta para guardar.

    Returns:
        fig, ax
    """
    fig, ax = plt.subplots(figsize=figsize)

    # Calcular estadísticas por grupo y x
    if group_col:
        stats_df = data.groupby([x_col, group_col])[y_col].agg(['mean', 'std', 'sem', 'count']).reset_index()
        # Calcular intervalo de confianza si se pide
        if error_type == 'ci':
            stats_df['ci_lower'] = stats_df['mean'] - stats.t.ppf(1 - (1 - ci)/2, stats_df['count']-1) * stats_df['sem']
            stats_df['ci_upper'] = stats_df['mean'] + stats.t.ppf(1 - (1 - ci)/2, stats_df['count']-1) * stats_df['sem']
            err_lower = stats_df['mean'] - stats_df['ci_lower']
            err_upper = stats_df['ci_upper'] - stats_df['mean']
        elif error_type == 'sem':
            err_lower = stats_df['sem']
            err_upper = stats_df['sem']
        else:  # sd
            err_lower = stats_df['std']
            err_upper = stats_df['std']

        # Dibujar barras agrupadas
        sns.barplot(data=stats_df, x=x_col, y='mean', hue=group_col,
                    palette=palette, ax=ax, **kwargs)
        # Añadir barras de error manualmente
        for i, bar in enumerate(ax.patches):
            # Encontrar el índice en stats_df correspondiente
            # Esto es complicado; mejor usar seaborn con estimador y errorbar
            pass
        # Alternativa: usar seaborn directamente con errorbar
        # Pero seaborn no soporta CI personalizado fácilmente.
        # En su lugar, usamos pointplot con errorbar.
    else:
        # Sin group_col, barplot simple con errorbar automático
        sns.barplot(data=data, x=x_col, y=y_col, palette=palette,
                    errorbar=('ci', ci) if error_type=='ci' else ('sem' if error_type=='sem' else 'sd'),
                    ax=ax, **kwargs)

    ax.set_xlabel(xlabel if xlabel else x_col)
    ax.set_ylabel(ylabel if ylabel else y_col)
    ax.set_title(title)
    if group_col:
        ax.legend(title=group_col)
    sns.despine()

    if save_path:
        fig.savefig(save_path, dpi=dpi, bbox_inches='tight')

    return fig, ax


# =============================================================================
# 8. Ejemplo de uso (si se ejecuta como script)
# =============================================================================

if __name__ == "__main__":
    # Generar datos de ejemplo
    np.random.seed(42)
    n = 30
    data = pd.DataFrame({
        'session': np.tile(np.arange(1, 9), n),
        'subject_id': np.repeat(np.arange(1, n+1), 8),
        'model': np.repeat(['gcd', 'control'], n*4),
        'knowledge': np.random.normal(0.5, 0.2, n*8) + np.tile(np.linspace(0, 0.3, 8), n)*0.5,
        'retention': np.random.normal(0.4, 0.15, n*8) + np.tile(np.linspace(0, 0.2, 8), n)*0.4,
        'creativity': np.random.normal(50, 10, n*8),
    })
    # Añadir columna de grupo
    data['model'] = data['model'].astype('category')

    print("Generando gráficos de ejemplo...")

    # 1. Curva de aprendizaje
    plot_learning_curve(data, 'session', 'knowledge', 'model',
                        title="Curva de Aprendizaje", save_path="test_learning_curve.png")
    print("Guardado: test_learning_curve.png")

    # 2. Boxplot
    plot_boxplot(data, 'model', 'retention', title="Retención por grupo",
                 save_path="test_boxplot.png")
    print("Guardado: test_boxplot.png")

    # 3. Correlación (usamos datos simulados)
    corr_data = data[['knowledge', 'retention', 'creativity']].sample(100)
    plot_correlation_matrix(corr_data, title="Correlaciones", save_path="test_corr.png")
    print("Guardado: test_corr.png")

    # 4. Dispersión
    plot_scatter(data, 'knowledge', 'retention', hue_col='model',
                 title="Retención vs Conocimiento", add_regression=True,
                 save_path="test_scatter.png")
    print("Guardado: test_scatter.png")

    print("Todos los gráficos de ejemplo generados.")
