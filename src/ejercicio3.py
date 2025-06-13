"""
Módulo ejercicio3: Análisis temporal y visualización.

Este módulo contiene funciones para convertir fechas, calcular años decimales
y visualizar la evolución del volumen del embalse de La Baells.
"""

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os


def convertir_a_datetime(df):
    """
    Convierte la columna 'dia' a formato datetime.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame con la columna 'dia' en formato string.
        
    Returns
    -------
    pd.DataFrame
        DataFrame con la columna 'dia' convertida a datetime.
    """
    print("\n=== Convirtiendo columna 'dia' a datetime ===")
    
    # Crear una copia para no modificar el original
    df_datetime = df.copy()
    
    # Convertir a datetime
    df_datetime['dia'] = pd.to_datetime(df_datetime['dia'], format='%d/%m/%Y')
    
    print(f"Tipo de datos antes: {df['dia'].dtype}")
    print(f"Tipo de datos después: {df_datetime['dia'].dtype}")
    
    return df_datetime


def analizar_rango_temporal(df):
    """
    Ordena el dataframe por fecha y muestra el rango temporal de los datos.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame con la columna 'dia' en formato datetime.
        
    Returns
    -------
    tuple
        Tupla con (fecha_minima, fecha_maxima, numero_registros).
    """
    print("\n=== Análisis del rango temporal ===")
    
    # Ordenar por fecha
    df_ordenado = df.sort_values('dia', ascending=True).copy()
    
    # Obtener fechas extremas
    fecha_min = df_ordenado['dia'].min()
    fecha_max = df_ordenado['dia'].max()
    num_registros = len(df_ordenado)
    
    print(f"Número total de registros: {num_registros}")
    print(f"Fecha más antigua: {fecha_min.strftime('%d/%m/%Y')}")
    print(f"Fecha más reciente: {fecha_max.strftime('%d/%m/%Y')}")
    print(f"Período de tiempo: {(fecha_max - fecha_min).days} días")
    
    return fecha_min, fecha_max, num_registros


def toYearFraction(date):
    """
    Convierte una fecha a su valor decimal del año.
    
    Parameters
    ----------
    date : pd.Timestamp o datetime
        Fecha a convertir.
        
    Returns
    -------
    float
        Año decimal correspondiente a la fecha.
        
    Examples
    --------
    >>> toYearFraction(datetime(2025, 7, 1))
    2025.4958...
    """
    # Si es un Timestamp de pandas, convertir a datetime
    if hasattr(date, 'to_pydatetime'):
        date = date.to_pydatetime()
    
    # Calcular el inicio del año
    year_start = datetime(year=date.year, month=1, day=1)
    
    # Calcular el inicio del siguiente año
    year_end = datetime(year=date.year + 1, month=1, day=1)
    
    # Calcular la fracción del año
    year_part = date - year_start
    year_length = year_end - year_start
    
    return date.year + year_part.total_seconds() / year_length.total_seconds()


def crear_columna_dia_decimal(df):
    """
    Crea una nueva columna 'dia_decimal' con el año decimal.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame con la columna 'dia' en formato datetime.
        
    Returns
    -------
    pd.DataFrame
        DataFrame con la nueva columna 'dia_decimal'.
    """
    print("\n=== Creando columna 'dia_decimal' ===")
    
    # Crear copia
    df_decimal = df.copy()
    
    # Aplicar la función toYearFraction a cada fecha
    df_decimal['dia_decimal'] = df_decimal['dia'].apply(toYearFraction)
    
    # Mostrar algunos ejemplos
    print("Ejemplos de conversión:")
    ejemplos = df_decimal[['dia', 'dia_decimal']].head(3)
    for idx, row in ejemplos.iterrows():
        print(f"  {row['dia'].strftime('%d/%m/%Y')} -> {row['dia_decimal']:.6f}")
    
    return df_decimal


def visualizar_evolucion_volumen(df, nombre_alumno="Samuel Viciana"):
    """
    Crea y guarda una gráfica de la evolución del volumen del embalse.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame con las columnas 'dia_decimal' y 'nivell_perc'.
    nombre_alumno : str
        Nombre del alumno para incluir en el gráfico.
        
    Returns
    -------
    str
        Ruta del archivo guardado.
    """
    print("\n=== Creando visualización del volumen ===")
    
    # Ordenar por fecha
    df_plot = df.sort_values('dia_decimal').copy()
    
    # Crear la figura
    plt.figure(figsize=(12, 6))
    
    # Graficar
    plt.plot(df_plot['dia_decimal'], df_plot['nivell_perc'], 
             linewidth=0.8, color='blue', alpha=0.7)
    
    # Configurar el gráfico
    plt.title('Evolución del volumen del embalse de La Baells', fontsize=16, pad=20)
    plt.xlabel('Año', fontsize=12)
    plt.ylabel('Porcentaje de volumen embalsado (%)', fontsize=12)
    plt.grid(True, alpha=0.3)
    
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
    filename = f"labaells_{nombre_alumno.replace(' ', '_')}.png"
    filepath = os.path.join(img_dir, filename)
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Gráfico guardado en: {filepath}")
    return filepath


def ejecutar_ejercicio3(df_baells):
    """
    Función principal que ejecuta todas las tareas del ejercicio 3.
    
    Parameters
    ----------
    df_baells : pd.DataFrame
        DataFrame filtrado con los datos de La Baells del ejercicio 2.
        
    Returns
    -------
    pd.DataFrame
        DataFrame con las columnas adicionales creadas.
    """
    print("\n" + "="*50)
    print("EJERCICIO 3: Análisis temporal y visualización")
    print("="*50)
    
    # Convertir a datetime
    df_datetime = convertir_a_datetime(df_baells)
    
    # Analizar rango temporal
    fecha_min, fecha_max, num_registros = analizar_rango_temporal(df_datetime)
    
    # Crear columna dia_decimal
    df_decimal = crear_columna_dia_decimal(df_datetime)
    
    # Visualizar evolución
    visualizar_evolucion_volumen(df_decimal)
    
    # Mostrar resumen del dataframe resultante
    print("\n=== Resumen del DataFrame resultante ===")
    print(f"Columnas: {list(df_decimal.columns)}")
    print(f"Registros: {len(df_decimal)}")
    
    return df_decimal


if __name__ == "__main__":
    # Si se ejecuta este archivo directamente
    from ejercicio1 import cargar_dataset
    from ejercicio2 import ejecutar_ejercicio2
    
    df = cargar_dataset()
    df_baells = ejecutar_ejercicio2(df)
    df_final = ejecutar_ejercicio3(df_baells)