"""
Módulo ejercicio2: Limpieza de datos y filtrado.

Este módulo contiene las funciones para renombrar columnas, limpiar nombres
de embalses y filtrar datos específicos del embalse de La Baells.
"""

import pandas as pd
import re


def renombrar_columnas(df):
    """
    Renombra las columnas del DataFrame según el diccionario especificado.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame con las columnas originales.
        
    Returns
    -------
    pd.DataFrame
        DataFrame con las columnas renombradas.
    """
    # Diccionario de mapeo de nombres
    diccionario_columnas = {
        'Dia': 'dia',
        'Estació': 'estacio',
        'Nivell absolut (msnm)': 'nivell_msnm',
        'Percentatge volum embassat (%)': 'nivell_perc',
        'Volum embassat (hm3)': 'volum'
    }
    
    print("\n=== Renombrando columnas ===")
    print("Mapeo de columnas:")
    for old, new in diccionario_columnas.items():
        print(f"  '{old}' -> '{new}'")
    
    df_renamed = df.rename(columns=diccionario_columnas)
    return df_renamed


def mostrar_pantanos_unicos(df):
    """
    Muestra los valores únicos de los nombres de los pantanos.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame con la columna 'estacio'.
        
    Returns
    -------
    pd.Series
        Serie con los nombres únicos de los pantanos.
    """
    print("\n=== Valores únicos de pantanos ===")
    pantanos_unicos = df['estacio'].unique()
    for pantano in pantanos_unicos:
        print(f"- {pantano}")
    print(f"\nTotal de pantanos únicos: {len(pantanos_unicos)}")
    return pantanos_unicos


def limpiar_nombres_pantanos(df):
    """
    Limpia los nombres de los pantanos eliminando 'Embassament de' y el municipio entre paréntesis.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame con la columna 'estacio' a limpiar.
        
    Returns
    -------
    pd.DataFrame
        DataFrame con los nombres de pantanos limpiados.
    """
    print("\n=== Limpiando nombres de pantanos ===")
    
    def limpiar_nombre(nombre):
        """Función auxiliar para limpiar un nombre de pantano."""
        # Eliminar 'Embassament de ' del inicio
        nombre_limpio = re.sub(r'^Embassament de\s+', '', nombre)
        # Eliminar el municipio entre paréntesis
        nombre_limpio = re.sub(r'\s*\([^)]*\)', '', nombre_limpio)
        return nombre_limpio
    
    # Crear una copia para no modificar el original
    df_limpio = df.copy()
    
    # Aplicar la limpieza
    df_limpio['estacio'] = df_limpio['estacio'].apply(limpiar_nombre)
    
    # Mostrar algunos ejemplos de la transformación
    print("Ejemplos de transformación:")
    ejemplos = df[['estacio']].drop_duplicates().head(3)
    for idx, row in ejemplos.iterrows():
        original = row['estacio']
        limpio = limpiar_nombre(original)
        print(f"  '{original}' -> '{limpio}'")
    
    return df_limpio


def filtrar_la_baells(df):
    """
    Filtra los datos correspondientes al embalse de La Baells.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame con todos los datos de embalses.
        
    Returns
    -------
    pd.DataFrame
        DataFrame filtrado con solo los datos de La Baells.
    """
    print("\n=== Filtrando datos de La Baells ===")
    
    # Filtrar por La Baells
    df_baells = df[df['estacio'] == 'la Baells'].copy()
    
    print(f"Registros totales en el dataset: {len(df)}")
    print(f"Registros de La Baells: {len(df_baells)}")
    print(f"Porcentaje del total: {len(df_baells)/len(df)*100:.2f}%")
    
    # Reset del índice para tener un índice continuo
    df_baells.reset_index(drop=True, inplace=True)
    
    return df_baells


def ejecutar_ejercicio2(df):
    """
    Función principal que ejecuta todas las tareas del ejercicio 2.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame con los datos originales del ejercicio 1.
        
    Returns
    -------
    pd.DataFrame
        DataFrame filtrado con solo los datos de La Baells.
    """
    print("\n" + "="*50)
    print("EJERCICIO 2: Limpieza de datos y filtrado")
    print("="*50)
    
    # Renombrar columnas
    df_renamed = renombrar_columnas(df)
    
    # Mostrar valores únicos de pantanos
    mostrar_pantanos_unicos(df_renamed)
    
    # Limpiar nombres de pantanos
    df_limpio = limpiar_nombres_pantanos(df_renamed)
    
    # Mostrar valores únicos después de limpiar
    print("\n=== Pantanos después de limpieza ===")
    pantanos_limpios = df_limpio['estacio'].unique()
    for pantano in pantanos_limpios:
        print(f"- {pantano}")
    
    # Filtrar La Baells
    df_baells = filtrar_la_baells(df_limpio)
    
    # Mostrar algunas filas del resultado
    print("\n=== Primeras filas de La Baells ===")
    print(df_baells.head())
    
    return df_baells


if __name__ == "__main__":
    # Si se ejecuta este archivo directamente
    from ejercicio1 import cargar_dataset
    df = cargar_dataset()
    df_baells = ejecutar_ejercicio2(df)