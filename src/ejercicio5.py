"""
Módulo ejercicio5: Identificación de períodos de sequía.

Este módulo contiene funciones para identificar y calcular los períodos
de sequía basándose en la serie temporal suavizada del embalse.
"""

import pandas as pd
import numpy as np


def calcula_periodos(df, umbral=60):
    """
    Calcula los períodos de sequía cuando el volumen suavizado está por debajo del umbral.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame con las columnas 'dia_decimal' y 'nivell_perc_suavizado'.
    umbral : float
        Porcentaje umbral para definir sequía (por defecto 60%).
        
    Returns
    -------
    list
        Lista de períodos de sequía, donde cada período es [inicio, fin] en años decimales.
        
    Examples
    --------
    >>> calcula_periodos(df)
    [[2000.63, 2002.52], [2005.21, 2008.42], [2022.11, 2024.95]]
    """
    print(f"\n=== Calculando períodos de sequía (umbral: {umbral}%) ===")
    
    # Ordenar por fecha
    df_ordenado = df.sort_values('dia_decimal').copy()
    
    # Identificar puntos bajo el umbral
    bajo_umbral = df_ordenado['nivell_perc_suavizado'] < umbral
    
    # Encontrar cambios (inicio y fin de períodos)
    # diff() encuentra donde cambia de False a True (inicio) o True a False (fin)
    cambios = bajo_umbral.astype(int).diff()
    
    # Inicio de sequía: cambio de 0 a 1 (False a True)
    inicios = df_ordenado[cambios == 1]['dia_decimal'].values
    
    # Fin de sequía: cambio de 1 a 0 (True a False)
    finales = df_ordenado[cambios == -1]['dia_decimal'].values
    
    # Manejar casos especiales
    # Si empieza en sequía, añadir el primer valor como inicio
    if bajo_umbral.iloc[0]:
        inicios = np.insert(inicios, 0, df_ordenado['dia_decimal'].iloc[0])
    
    # Si termina en sequía, añadir el último valor como final
    if bajo_umbral.iloc[-1]:
        finales = np.append(finales, df_ordenado['dia_decimal'].iloc[-1])
    
    # Crear lista de períodos
    periodos = []
    for inicio, fin in zip(inicios, finales):
        periodos.append([round(inicio, 2), round(fin, 2)])
    
    return periodos


def analizar_periodos_sequia(df, periodos):
    """
    Analiza y muestra información detallada sobre los períodos de sequía identificados.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame con los datos completos.
    periodos : list
        Lista de períodos de sequía.
        
    Returns
    -------
    pd.DataFrame
        DataFrame con información detallada de cada período.
    """
    print("\n=== Análisis detallado de períodos de sequía ===")
    
    # Crear DataFrame con información de períodos
    info_periodos = []
    
    for i, (inicio, fin) in enumerate(periodos, 1):
        # Filtrar datos del período
        mask = (df['dia_decimal'] >= inicio) & (df['dia_decimal'] <= fin)
        datos_periodo = df[mask]
        
        if len(datos_periodo) > 0:
            # Calcular estadísticas
            duracion_años = fin - inicio
            duracion_dias = int(duracion_años * 365.25)
            volumen_min = datos_periodo['nivell_perc_suavizado'].min()
            volumen_medio = datos_periodo['nivell_perc_suavizado'].mean()
            
            # Encontrar fechas aproximadas
            fecha_inicio = datos_periodo.iloc[0]['dia']
            fecha_fin = datos_periodo.iloc[-1]['dia']
            
            info = {
                'Período': i,
                'Inicio (decimal)': inicio,
                'Fin (decimal)': fin,
                'Inicio (fecha)': fecha_inicio.strftime('%d/%m/%Y'),
                'Fin (fecha)': fecha_fin.strftime('%d/%m/%Y'),
                'Duración (años)': round(duracion_años, 2),
                'Duración (días)': duracion_dias,
                'Volumen mínimo (%)': round(volumen_min, 1),
                'Volumen medio (%)': round(volumen_medio, 1)
            }
            info_periodos.append(info)
    
    df_info = pd.DataFrame(info_periodos)
    
    # Mostrar información
    for _, periodo in df_info.iterrows():
        print(f"\nPeríodo {periodo['Período']}:")
        print(f"  Duración: {periodo['Duración (años)']} años ({periodo['Duración (días)']} días)")
        print(f"  Desde: {periodo['Inicio (fecha)']} ({periodo['Inicio (decimal)']})")
        print(f"  Hasta: {periodo['Fin (fecha)']} ({periodo['Fin (decimal)']})")
        print(f"  Volumen mínimo alcanzado: {periodo['Volumen mínimo (%)']}%")
        print(f"  Volumen medio durante el período: {periodo['Volumen medio (%)']}%")
    
    return df_info


def ejecutar_ejercicio5(df_suavizado):
    """
    Función principal que ejecuta todas las tareas del ejercicio 5.
    
    Parameters
    ----------
    df_suavizado : pd.DataFrame
        DataFrame con los datos suavizados del ejercicio 4.
        
    Returns
    -------
    tuple
        Tupla con (lista_periodos, dataframe_info_periodos).
    """
    print("\n" + "="*50)
    print("EJERCICIO 5: Identificación de períodos de sequía")
    print("="*50)
    
    # Calcular períodos de sequía
    periodos = calcula_periodos(df_suavizado)
    
    # Mostrar períodos encontrados
    print(f"\n=== Períodos de sequía encontrados ===")
    print(f"Total de períodos identificados: {len(periodos)}")
    print("\nPeríodos (formato decimal):")
    for periodo in periodos:
        print(f"  {periodo}")
    
    # Analizar períodos en detalle
    df_info_periodos = analizar_periodos_sequia(df_suavizado, periodos)
    
    # Estadísticas generales
    print("\n=== Estadísticas generales de sequías ===")
    if len(periodos) > 0:
        total_dias_sequia = df_info_periodos['Duración (días)'].sum()
        total_dias_datos = (df_suavizado['dia_decimal'].max() - df_suavizado['dia_decimal'].min()) * 365.25
        porcentaje_tiempo_sequia = (total_dias_sequia / total_dias_datos) * 100
        
        print(f"Número total de períodos de sequía: {len(periodos)}")
        print(f"Duración total en sequía: {total_dias_sequia} días")
        print(f"Porcentaje del tiempo en sequía: {porcentaje_tiempo_sequia:.1f}%")
        print(f"Duración media de las sequías: {df_info_periodos['Duración (días)'].mean():.0f} días")
        print(f"Volumen mínimo histórico: {df_info_periodos['Volumen mínimo (%)'].min():.1f}%")
    
    return periodos, df_info_periodos


if __name__ == "__main__":
    # Si se ejecuta este archivo directamente
    from ejercicio1 import cargar_dataset
    from ejercicio2 import ejecutar_ejercicio2
    from ejercicio3 import ejecutar_ejercicio3
    from ejercicio4 import ejecutar_ejercicio4
    
    df = cargar_dataset()
    df_baells = ejecutar_ejercicio2(df)
    df_decimal = ejecutar_ejercicio3(df_baells)
    df_suavizado = ejecutar_ejercicio4(df_decimal)
    periodos, df_info = ejecutar_ejercicio5(df_suavizado)