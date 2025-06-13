"""
Módulo ejercicio4: Suavizado de señal y análisis de tendencias.

Este módulo contiene funciones para aplicar filtros de suavizado a los datos
del embalse y visualizar las tendencias para identificar períodos de sequía.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
import os


def suavizar_serie_temporal(df, window_length=1500, polyorder=3):
    """
    Aplica el filtro Savitzky-Golay para suavizar la serie temporal del volumen.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame con las columnas 'dia_decimal' y 'nivell_perc'.
    window_length : int
        Longitud de la ventana del filtro (debe ser impar).
    polyorder : int
        Orden del polinomio para el ajuste.
        
    Returns
    -------
    pd.DataFrame
        DataFrame con la columna adicional 'nivell_perc_suavizado'.
    """
    print("\n=== Aplicando suavizado con savgol_filter ===")
    print(f"Parámetros: window_length={window_length}, polyorder={polyorder}")
    
    # Crear copia del dataframe
    df_suavizado = df.copy()
    
    # Ordenar por fecha para asegurar continuidad
    df_suavizado = df_suavizado.sort_values('dia_decimal').reset_index(drop=True)
    
    # Verificar que tenemos suficientes datos
    if len(df_suavizado) < window_length:
        print(f"Advertencia: Ajustando window_length de {window_length} a {len(df_suavizado)//2*2-1}")
        window_length = len(df_suavizado) // 2 * 2 - 1  # Asegurar que sea impar
    
    # Aplicar el filtro Savitzky-Golay
    y_suavizado = savgol_filter(df_suavizado['nivell_perc'].values, 
                                window_length=window_length, 
                                polyorder=polyorder)
    
    # Añadir la columna suavizada
    df_suavizado['nivell_perc_suavizado'] = y_suavizado
    
    # Mostrar estadísticas
    print(f"\nEstadísticas del suavizado:")
    print(f"  Media original: {df_suavizado['nivell_perc'].mean():.2f}%")
    print(f"  Media suavizada: {df_suavizado['nivell_perc_suavizado'].mean():.2f}%")
    print(f"  Desv. est. original: {df_suavizado['nivell_perc'].std():.2f}")
    print(f"  Desv. est. suavizada: {df_suavizado['nivell_perc_suavizado'].std():.2f}")
    
    return df_suavizado


def visualizar_serie_suavizada(df, nombre_alumno="Samuel Viciana"):
    """
    Crea una visualización comparando la serie original con la suavizada.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame con las columnas 'dia_decimal', 'nivell_perc' y 'nivell_perc_suavizado'.
    nombre_alumno : str
        Nombre del alumno para incluir en el gráfico.
        
    Returns
    -------
    str
        Ruta del archivo guardado.
    """
    print("\n=== Creando visualización con serie suavizada ===")
    
    # Ordenar por fecha
    df_plot = df.sort_values('dia_decimal').copy()
    
    # Crear la figura
    plt.figure(figsize=(14, 8))
    
    # Graficar serie original
    plt.plot(df_plot['dia_decimal'], df_plot['nivell_perc'], 
             linewidth=0.5, color='lightblue', alpha=0.6, label='Datos originales')
    
    # Graficar serie suavizada
    plt.plot(df_plot['dia_decimal'], df_plot['nivell_perc_suavizado'], 
             linewidth=3, color='darkblue', label='Señal suavizada')
    
    # Añadir línea de referencia al 60%
    plt.axhline(y=60, color='red', linestyle='--', alpha=0.5, 
                label='Umbral sequía (60%)')
    
    # Configurar el gráfico
    plt.title('Evolución del volumen del embalse de La Baells - Análisis de tendencias', 
              fontsize=16, pad=20)
    plt.xlabel('Año', fontsize=12)
    plt.ylabel('Porcentaje de volumen embalsado (%)', fontsize=12)
    plt.legend(loc='upper right', fontsize=10)
    plt.grid(True, alpha=0.3)
    
    # Establecer límites del eje Y
    plt.ylim(0, 105)
    
    # Añadir subtítulo con el nombre del alumno
    plt.text(0.5, 0.02, nombre_alumno, ha='center', transform=plt.gca().transAxes,
             fontsize=10, style='italic', color='gray')
    
    # Ajustar diseño
    plt.tight_layout()
    
    # Crear directorio img si no existe
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    img_dir = os.path.join(project_root, 'img')
    os.makedirs(img_dir, exist_ok=True)
    
    # Guardar la imagen
    filename = f"labaells_smoothed_{nombre_alumno.replace(' ', '_')}.png"
    filepath = os.path.join(img_dir, filename)
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Gráfico guardado en: {filepath}")
    return filepath


def analizar_tendencias(df):
    """
    Analiza las tendencias en la serie suavizada para identificar períodos críticos.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame con la columna 'nivell_perc_suavizado'.
        
    Returns
    -------
    dict
        Diccionario con estadísticas de las tendencias.
    """
    print("\n=== Análisis de tendencias ===")
    
    # Identificar períodos por debajo del 60%
    df_analisis = df.sort_values('dia_decimal').copy()
    periodos_sequia = df_analisis[df_analisis['nivell_perc_suavizado'] < 60]
    
    estadisticas = {
        'min_volumen': df_analisis['nivell_perc_suavizado'].min(),
        'fecha_min_volumen': df_analisis.loc[df_analisis['nivell_perc_suavizado'].idxmin(), 'dia'],
        'max_volumen': df_analisis['nivell_perc_suavizado'].max(),
        'fecha_max_volumen': df_analisis.loc[df_analisis['nivell_perc_suavizado'].idxmax(), 'dia'],
        'dias_bajo_60': len(periodos_sequia),
        'porcentaje_tiempo_sequia': len(periodos_sequia) / len(df_analisis) * 100
    }
    
    print(f"Volumen mínimo: {estadisticas['min_volumen']:.1f}% ({estadisticas['fecha_min_volumen'].strftime('%d/%m/%Y')})")
    print(f"Volumen máximo: {estadisticas['max_volumen']:.1f}% ({estadisticas['fecha_max_volumen'].strftime('%d/%m/%Y')})")
    print(f"Días por debajo del 60%: {estadisticas['dias_bajo_60']} ({estadisticas['porcentaje_tiempo_sequia']:.1f}% del tiempo)")
    
    return estadisticas


def ejecutar_ejercicio4(df_decimal):
    """
    Función principal que ejecuta todas las tareas del ejercicio 4.
    
    Parameters
    ----------
    df_decimal : pd.DataFrame
        DataFrame con los datos del ejercicio 3 incluyendo 'dia_decimal'.
        
    Returns
    -------
    pd.DataFrame
        DataFrame con la columna adicional de valores suavizados.
    """
    print("\n" + "="*50)
    print("EJERCICIO 4: Suavizado y análisis de tendencias")
    print("="*50)
    
    # Aplicar suavizado
    df_suavizado = suavizar_serie_temporal(df_decimal)
    
    # Visualizar serie suavizada
    visualizar_serie_suavizada(df_suavizado)
    
    # Analizar tendencias
    analizar_tendencias(df_suavizado)
    
    # Mostrar resumen
    print("\n=== Resumen del DataFrame resultante ===")
    print(f"Columnas: {list(df_suavizado.columns)}")
    print(f"Registros: {len(df_suavizado)}")
    
    return df_suavizado


if __name__ == "__main__":
    # Si se ejecuta este archivo directamente
    from ejercicio1 import cargar_dataset
    from ejercicio2 import ejecutar_ejercicio2
    from ejercicio3 import ejecutar_ejercicio3
    
    df = cargar_dataset()
    df_baells = ejecutar_ejercicio2(df)
    df_decimal = ejecutar_ejercicio3(df_baells)
    df_suavizado = ejecutar_ejercicio4(df_decimal)