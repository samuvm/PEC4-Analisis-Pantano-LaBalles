"""
Archivo principal para ejecutar los ejercicios de la PEC4.

Este script permite ejecutar todos los ejercicios de manera interactiva,
verificando la disponibilidad del dataset y permitiendo elegir qué ejercicios ejecutar.
"""

import os
import sys
from pathlib import Path

# Agregar el directorio src al path para importar los módulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.ejercicio1 import ejecutar_ejercicio1, cargar_dataset
from src.ejercicio2 import ejecutar_ejercicio2
from src.ejercicio3 import ejecutar_ejercicio3
from src.ejercicio4 import ejecutar_ejercicio4
from src.ejercicio5 import ejecutar_ejercicio5


def verificar_dataset():
    """
    Verifica si existe el archivo de dataset y permite configurar la ruta.
    
    Returns
    -------
    str
        Ruta al archivo de dataset verificada.
    """
    print("="*60)
    print("VERIFICACIÓN DEL DATASET")
    print("="*60)
    
    # Rutas posibles por defecto
    rutas_defecto = [
        'data/Quantitat_d_aigua_als_embassaments_de_les_Conques_Internes_de_Catalunya_20250613.csv',
        'data/dataset.csv',
        'Quantitat_d_aigua_als_embassaments_de_les_Conques_Internes_de_Catalunya_20250613.csv'
    ]
    
    # Verificar rutas por defecto
    for ruta in rutas_defecto:
        if os.path.exists(ruta):
            print(f"✓ Dataset encontrado en: {ruta}")
            return os.path.abspath(ruta)
    
    # Si no se encuentra, solicitar ruta
    print("⚠️  No se encontró el archivo de dataset en las rutas por defecto:")
    for ruta in rutas_defecto:
        print(f"   - {ruta}")
    
    print("\nOpciones:")
    print("1. Proporcionar ruta completa al archivo")
    print("2. Salir del programa")
    
    while True:
        opcion = input("\nSelecciona una opción (1-2): ").strip()
        
        if opcion == "1":
            while True:
                ruta_usuario = input("\nIntroduce la ruta completa al archivo CSV: ").strip()
                ruta_usuario = ruta_usuario.strip('"\'')  # Eliminar comillas si las hay
                
                if os.path.exists(ruta_usuario):
                    print(f"✓ Archivo verificado: {ruta_usuario}")
                    return os.path.abspath(ruta_usuario)
                else:
                    print(f"❌ No se encontró el archivo: {ruta_usuario}")
                    reintentar = input("¿Deseas intentar con otra ruta? (s/n): ").strip().lower()
                    if reintentar != 's':
                        break
        
        elif opcion == "2":
            print("Saliendo del programa...")
            sys.exit(0)
        else:
            print("Opción no válida. Por favor selecciona 1 o 2.")


def mostrar_menu():
    """
    Muestra el menú de opciones para ejecutar ejercicios.
    
    Returns
    -------
    str
        Opción seleccionada por el usuario.
    """
    print("\n" + "="*60)
    print("MENÚ DE EJERCICIOS - PEC4")
    print("="*60)
    print("1. Ejecutar Ejercicio 1 - Carga del dataset y EDA")
    print("2. Ejecutar Ejercicio 2 - Limpieza de datos y filtrado")
    print("3. Ejecutar Ejercicio 3 - Análisis temporal y visualización")
    print("4. Ejecutar Ejercicio 4 - Suavizado y análisis de tendencias")
    print("5. Ejecutar Ejercicio 5 - Identificación de períodos de sequía")
    print("6. Ejecutar TODOS los ejercicios en orden")
    print("0. Salir")
    print("="*60)
    
    while True:
        opcion = input("Selecciona una opción (0-6): ").strip()
        if opcion in ['0', '1', '2', '3', '4', '5', '6']:
            return opcion
        else:
            print("Opción no válida. Por favor selecciona un número del 0 al 6.")


def ejecutar_ejercicio_individual(numero, ruta_dataset, resultados_previos=None):
    """
    Ejecuta un ejercicio individual.
    
    Parameters
    ----------
    numero : str
        Número del ejercicio a ejecutar.
    ruta_dataset : str
        Ruta al archivo de dataset.
    resultados_previos : dict, optional
        Diccionario con los resultados de ejercicios anteriores.
        
    Returns
    -------
    dict
        Diccionario actualizado con los resultados.
    """
    if resultados_previos is None:
        resultados_previos = {}
    
    try:
        if numero == '1':
            print("\n🔄 Ejecutando Ejercicio 1...")
            df = cargar_dataset(ruta_dataset)
            df = ejecutar_ejercicio1(df)
            resultados_previos['df_original'] = df
            print("✅ Ejercicio 1 completado exitosamente")
            
        elif numero == '2':
            print("\n🔄 Ejecutando Ejercicio 2...")
            if 'df_original' not in resultados_previos:
                print("⚠️  Ejecutando Ejercicio 1 primero...")
                df = cargar_dataset(ruta_dataset)
                df = ejecutar_ejercicio1(df)
                resultados_previos['df_original'] = df
            
            df_baells = ejecutar_ejercicio2(resultados_previos['df_original'])
            resultados_previos['df_baells'] = df_baells
            print("✅ Ejercicio 2 completado exitosamente")
            
        elif numero == '3':
            print("\n🔄 Ejecutando Ejercicio 3...")
            # Ejecutar ejercicios previos si es necesario
            if 'df_baells' not in resultados_previos:
                if 'df_original' not in resultados_previos:
                    print("⚠️  Ejecutando Ejercicio 1 primero...")
                    df = cargar_dataset(ruta_dataset)
                    df = ejecutar_ejercicio1(df)
                    resultados_previos['df_original'] = df
                
                print("⚠️  Ejecutando Ejercicio 2 primero...")
                df_baells = ejecutar_ejercicio2(resultados_previos['df_original'])
                resultados_previos['df_baells'] = df_baells
            
            df_decimal = ejecutar_ejercicio3(resultados_previos['df_baells'])
            resultados_previos['df_decimal'] = df_decimal
            print("✅ Ejercicio 3 completado exitosamente")
            
        elif numero == '4':
            print("\n🔄 Ejecutando Ejercicio 4...")
            # Ejecutar ejercicios previos si es necesario
            if 'df_decimal' not in resultados_previos:
                if 'df_original' not in resultados_previos:
                    print("⚠️  Ejecutando Ejercicio 1 primero...")
                    df = cargar_dataset(ruta_dataset)
                    df = ejecutar_ejercicio1(df)
                    resultados_previos['df_original'] = df
                
                if 'df_baells' not in resultados_previos:
                    print("⚠️  Ejecutando Ejercicio 2 primero...")
                    df_baells = ejecutar_ejercicio2(resultados_previos['df_original'])
                    resultados_previos['df_baells'] = df_baells
                
                print("⚠️  Ejecutando Ejercicio 3 primero...")
                df_decimal = ejecutar_ejercicio3(resultados_previos['df_baells'])
                resultados_previos['df_decimal'] = df_decimal
            
            df_suavizado = ejecutar_ejercicio4(resultados_previos['df_decimal'])
            resultados_previos['df_suavizado'] = df_suavizado
            print("✅ Ejercicio 4 completado exitosamente")
            
        elif numero == '5':
            print("\n🔄 Ejecutando Ejercicio 5...")
            # Ejecutar ejercicios previos si es necesario
            if 'df_suavizado' not in resultados_previos:
                if 'df_original' not in resultados_previos:
                    print("⚠️  Ejecutando Ejercicio 1 primero...")
                    df = cargar_dataset(ruta_dataset)
                    df = ejecutar_ejercicio1(df)
                    resultados_previos['df_original'] = df
                
                if 'df_baells' not in resultados_previos:
                    print("⚠️  Ejecutando Ejercicio 2 primero...")
                    df_baells = ejecutar_ejercicio2(resultados_previos['df_original'])
                    resultados_previos['df_baells'] = df_baells
                
                if 'df_decimal' not in resultados_previos:
                    print("⚠️  Ejecutando Ejercicio 3 primero...")
                    df_decimal = ejecutar_ejercicio3(resultados_previos['df_baells'])
                    resultados_previos['df_decimal'] = df_decimal
                
                print("⚠️  Ejecutando Ejercicio 4 primero...")
                df_suavizado = ejecutar_ejercicio4(resultados_previos['df_decimal'])
                resultados_previos['df_suavizado'] = df_suavizado
            
            periodos, df_info = ejecutar_ejercicio5(resultados_previos['df_suavizado'])
            resultados_previos['periodos'] = periodos
            resultados_previos['df_info_periodos'] = df_info
            print("✅ Ejercicio 5 completado exitosamente")
            
    except Exception as e:
        print(f"❌ Error ejecutando Ejercicio {numero}: {str(e)}")
        print("Revisa que todos los archivos y dependencias estén correctamente configurados.")
        
    return resultados_previos


def ejecutar_todos_los_ejercicios(ruta_dataset):
    """
    Ejecuta todos los ejercicios en orden.
    
    Parameters
    ----------
    ruta_dataset : str
        Ruta al archivo de dataset.
    """
    print("\n" + "🚀" + "="*58)
    print("EJECUTANDO TODOS LOS EJERCICIOS")
    print("="*60)
    
    resultados = {}
    
    for i in range(1, 6):
        resultados = ejecutar_ejercicio_individual(str(i), ruta_dataset, resultados)
        
        # Pausa entre ejercicios
        if i < 5:
            input(f"\n⏸️  Presiona Enter para continuar con el Ejercicio {i+1}...")
    
    print("\n" + "🎉" + "="*58)
    print("TODOS LOS EJERCICIOS COMPLETADOS")
    print("="*60)
    
    # Mostrar resumen final
    print("\n📋 RESUMEN FINAL:")
    if 'periodos' in resultados:
        print(f"   • Total de períodos de sequía identificados: {len(resultados['periodos'])}")
        print(f"   • Períodos: {resultados['periodos']}")
    
    if 'df_info_periodos' in resultados:
        print(f"   • Archivos generados en directorio 'img/'")
        print(f"   • Datos procesados: {len(resultados.get('df_suavizado', []))} registros")


def main():
    """
    Función principal del programa.
    """
    print("="*60)
    print("PEC4 - ANÁLISIS DE DATOS DE EMBALSES DE CATALUNYA")
    print("Samuel Viciana")
    print("22.403 · Programación para la ciencia de datos")
    print("="*60)
    
    # Verificar dataset
    ruta_dataset = verificar_dataset()
    print(f"\n✅ Dataset configurado: {ruta_dataset}")
    
    # Crear directorios necesarios
    os.makedirs('img', exist_ok=True)
    
    # Bucle principal
    while True:
        opcion = mostrar_menu()
        
        if opcion == '0':
            print("\n👋 ¡Gracias por usar el análisis de embalses!")
            print("Desarrollado por Samuel Viciana para la UOC")
            break
            
        elif opcion == '6':
            ejecutar_todos_los_ejercicios(ruta_dataset)
            
        else:
            ejecutar_ejercicio_individual(opcion, ruta_dataset)
        
        # Preguntar si continuar
        if opcion != '0':
            continuar = input("\n¿Deseas ejecutar otra opción? (s/n): ").strip().lower()
            if continuar != 's':
                print("\n👋 ¡Gracias por usar el análisis de embalses!")
                print("Desarrollado por Samuel Viciana para la UOC")
                break


if __name__ == "__main__":
    main()

# =============================================================================
# CAMBIOS NECESARIOS EN LOS OTROS ARCHIVOS:
# =============================================================================

"""
ARCHIVO: src/ejercicio1.py
FRAGMENTO A REEMPLAZAR:
```python
def cargar_dataset(filepath=None):
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
```

REEMPLAZAR POR:
```python
def cargar_dataset(filepath=None):
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


def ejecutar_ejercicio1(df=None):
    if df is None:
        df = cargar_dataset()
    
    print("\n" + "="*50)
    print("EJERCICIO 1: Carga del dataset y EDA")
    print("="*50)
    
    print(f"\nDataset cargado correctamente. Dimensiones: {df.shape}")
    
    # Mostrar las primeras 5 filas
    mostrar_primeras_filas(df)
    
    # Mostrar las columnas
    mostrar_columnas(df)
    
    # Mostrar información general
    mostrar_informacion(df)
    
    return df
```

ARCHIVO: src/ejercicio1.py
FRAGMENTO A REEMPLAZAR:
```python
def ejecutar_ejercicio1():
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
```

REEMPLAZAR POR:
```python
def ejecutar_ejercicio1(df=None):
    if df is None:
        df = cargar_dataset()
    
    print("\n" + "="*50)
    print("EJERCICIO 1: Carga del dataset y EDA")
    print("="*50)
    
    print(f"\nDataset cargado correctamente. Dimensiones: {df.shape}")
    
    # Mostrar las primeras 5 filas
    mostrar_primeras_filas(df)
    
    # Mostrar las columnas
    mostrar_columnas(df)
    
    # Mostrar información general
    mostrar_informacion(df)
    
    return df
```

ARCHIVO: src/ejercicio1.py
FRAGMENTO A REEMPLAZAR:
```python
if __name__ == "__main__":
    # Si se ejecuta este archivo directamente, ejecutar el ejercicio
    ejecutar_ejercicio1()
```

REEMPLAZAR POR:
```python
if __name__ == "__main__":
    # Si se ejecuta este archivo directamente, ejecutar el ejercicio
    df = ejecutar_ejercicio1()
```

ARCHIVO: src/ejercicio2.py
FRAGMENTO A REEMPLAZAR:
```python
if __name__ == "__main__":
    # Si se ejecuta este archivo directamente
    from ejercicio1 import cargar_dataset
    df = cargar_dataset()
    df_baells = ejecutar_ejercicio2(df)
```

REEMPLAZAR POR:
```python
if __name__ == "__main__":
    # Si se ejecuta este archivo directamente
    from ejercicio1 import cargar_dataset, ejecutar_ejercicio1
    df = cargar_dataset()
    df = ejecutar_ejercicio1(df)
    df_baells = ejecutar_ejercicio2(df)
```

ARCHIVO: src/ejercicio3.py
FRAGMENTO A REEMPLAZAR:
```python
if __name__ == "__main__":
    # Si se ejecuta este archivo directamente
    from ejercicio1 import cargar_dataset
    from ejercicio2 import ejecutar_ejercicio2
    
    df = cargar_dataset()
    df_baells = ejecutar_ejercicio2(df)
    df_final = ejecutar_ejercicio3(df_baells)
```

REEMPLAZAR POR:
```python
if __name__ == "__main__":
    # Si se ejecuta este archivo directamente
    from ejercicio1 import cargar_dataset, ejecutar_ejercicio1
    from ejercicio2 import ejecutar_ejercicio2
    
    df = cargar_dataset()
    df = ejecutar_ejercicio1(df)
    df_baells = ejecutar_ejercicio2(df)
    df_final = ejecutar_ejercicio3(df_baells)
```

ARCHIVO: src/ejercicio4.py
FRAGMENTO A REEMPLAZAR:
```python
if __name__ == "__main__":
    # Si se ejecuta este archivo directamente
    from ejercicio1 import cargar_dataset
    from ejercicio2 import ejecutar_ejercicio2
    from ejercicio3 import ejecutar_ejercicio3
    
    df = cargar_dataset()
    df_baells = ejecutar_ejercicio2(df)
    df_decimal = ejecutar_ejercicio3(df_baells)
    df_suavizado = ejecutar_ejercicio4(df_decimal)
```

REEMPLAZAR POR:
```python
if __name__ == "__main__":
    # Si se ejecuta este archivo directamente
    from ejercicio1 import cargar_dataset, ejecutar_ejercicio1
    from ejercicio2 import ejecutar_ejercicio2
    from ejercicio3 import ejecutar_ejercicio3
    
    df = cargar_dataset()
    df = ejecutar_ejercicio1(df)
    df_baells = ejecutar_ejercicio2(df)
    df_decimal = ejecutar_ejercicio3(df_baells)
    df_suavizado = ejecutar_ejercicio4(df_decimal)
```

ARCHIVO: src/ejercicio5.py
FRAGMENTO A REEMPLAZAR:
```python
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
```

REEMPLAZAR POR:
```python
if __name__ == "__main__":
    # Si se ejecuta este archivo directamente
    from ejercicio1 import cargar_dataset, ejecutar_ejercicio1
    from ejercicio2 import ejecutar_ejercicio2
    from ejercicio3 import ejecutar_ejercicio3
    from ejercicio4 import ejecutar_ejercicio4
    
    df = cargar_dataset()
    df = ejecutar_ejercicio1(df)
    df_baells = ejecutar_ejercicio2(df)
    df_decimal = ejecutar_ejercicio3(df_baells)
    df_suavizado = ejecutar_ejercicio4(df_decimal)
    periodos, df_info = ejecutar_ejercicio5(df_suavizado)
```
"""