"""
Módulo ejercicio1: Carga del dataset y análisis exploratorio de datos (EDA).

Este módulo contiene las funciones necesarias para cargar el dataset de embalses
de las Cuencas Internas de Catalunya y realizar un análisis exploratorio básico.
"""

import pandas as pd
import os


def cargar_dataset(filepath=None):
    """
    Carga el dataset de embalses desde un archivo CSV.
    
    Parameters
    ----------
    filepath : str, optional
        Ruta al archivo CSV con los datos de los embalses.
        Si no se especifica, busca en la ruta por defecto.
        
    Returns
    -------
    pd.DataFrame
        DataFrame con los datos cargados.
        
    Raises
    ------
    FileNotFoundError
        Si el archivo no se encuentra en la ruta especificada.
    """
    if filepath is None:
        # Obtener la ruta del directorio actual del script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Ir al directorio padre (raíz del proyecto)
        project_root = os.path.dirname(script_dir)
        # Construir la ruta completa al archivo
        filepath = os.path.join(project_root, 'data', 
                               'Quantitat_d_aigua_als_embassaments_de_les_Conques_Internes_de_Catalunya_20250613.csv')
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"No se encuentra el archivo: {filepath}")
    
    df = pd.read_csv(filepath)
    return df


def mostrar_primeras_filas(df, n=5):
    """
    Muestra las primeras n filas del DataFrame.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame del cual mostrar las filas.
    n : int, optional
        Número de filas a mostrar (por defecto 5).
        
    Returns
    -------
    pd.DataFrame
        Las primeras n filas del DataFrame.
    """
    print(f"\n=== Primeras {n} filas del dataset ===")
    primeras_filas = df.head(n)
    print(primeras_filas)
    return primeras_filas


def mostrar_columnas(df):
    """
    Muestra las columnas del DataFrame.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame del cual mostrar las columnas.
        
    Returns
    -------
    pd.Index
        Index con los nombres de las columnas.
    """
    print("\n=== Columnas del dataset ===")
    columnas = df.columns
    for col in columnas:
        print(f"- {col}")
    return columnas


def mostrar_informacion(df):
    """
    Muestra información general del DataFrame usando el método info().
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame del cual mostrar la información.
        
    Returns
    -------
    None
    """
    print("\n=== Información del dataset ===")
    df.info()


def ejecutar_ejercicio1():
    """
    Función principal que ejecuta todas las tareas del ejercicio 1.
    
    Returns
    -------
    pd.DataFrame
        DataFrame con los datos cargados.
    """
    print("\n" + "="*50)
    print("EJERCICIO 1: Carga del dataset y EDA")
    print("="*50)
    
    # Cargar el dataset
    df = cargar_dataset()
    print(f"\nDataset cargado correctamente. Dimensiones: {df.shape}")
    
    # Mostrar las primeras 5 filas
    mostrar_primeras_filas(df)
    
    # Mostrar las columnas
    mostrar_columnas(df)
    
    # Mostrar información general
    mostrar_informacion(df)
    
    return df


if __name__ == "__main__":
    # Si se ejecuta este archivo directamente, ejecutar el ejercicio
    ejecutar_ejercicio1()