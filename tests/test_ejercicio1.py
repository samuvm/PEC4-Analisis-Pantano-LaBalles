"""
Tests para el Ejercicio 1: Carga del dataset y EDA.

Este módulo contiene las pruebas unitarias para verificar el correcto
funcionamiento de las funciones del ejercicio 1.
"""

import unittest
import os
import sys
import pandas as pd
from unittest.mock import patch, MagicMock
import tempfile

# Agregar el directorio src al path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from src.ejercicio1 import (
    cargar_dataset, 
    mostrar_primeras_filas, 
    mostrar_columnas, 
    mostrar_informacion,
    ejecutar_ejercicio1
)


class TestEjercicio1(unittest.TestCase):
    """Clase de tests para el ejercicio 1."""
    
    @classmethod
    def setUpClass(cls):
        """Configuración inicial para todos los tests."""
        cls.score = 0
        cls.max_score = 10
        cls.test_results = []
    
    def setUp(self):
        """Configuración para cada test individual."""
        # Crear un DataFrame de prueba
        self.df_test = pd.DataFrame({
            'Dia': ['01/01/2024', '02/01/2024', '03/01/2024'],
            'Estació': ['Embassament de la Baells (Berga)', 
                       'Embassament de Sau (Vilanova de Sau)', 
                       'Embassament de la Baells (Berga)'],
            'Nivell absolut (msnm)': [632.5, 425.3, 633.1],
            'Percentatge volum embassat (%)': [75.2, 68.5, 76.8],
            'Volum embassat (hm3)': [82.3, 125.6, 84.1]
        })
    
    def test_01_archivo_existe(self):
        """Test 1: Verificar que el archivo ejercicio1.py existe."""
        try:
            filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                   'src', 'ejercicio1.py')
            self.assertTrue(os.path.exists(filepath), 
                           "El archivo ejercicio1.py no existe")
            self.__class__.score += 1
            self.__class__.test_results.append(("Archivo existe", True, 1))
        except AssertionError as e:
            self.__class__.test_results.append(("Archivo existe", False, 0))
            raise e
    
    def test_02_docstring_modulo(self):
        """Test 2: Verificar que el módulo tiene docstring."""
        try:
            import src.ejercicio1
            self.assertIsNotNone(src.ejercicio1.__doc__, 
                               "El módulo no tiene docstring")
            self.assertGreater(len(src.ejercicio1.__doc__.strip()), 20,
                             "El docstring del módulo es muy corto")
            self.__class__.score += 1
            self.__class__.test_results.append(("Docstring del módulo", True, 1))
        except AssertionError as e:
            self.__class__.test_results.append(("Docstring del módulo", False, 0))
            raise e
    
    def test_03_funciones_tienen_docstring(self):
        """Test 3: Verificar que todas las funciones tienen docstring."""
        try:
            funciones = [cargar_dataset, mostrar_primeras_filas, 
                        mostrar_columnas, mostrar_informacion]
            for func in funciones:
                self.assertIsNotNone(func.__doc__, 
                                   f"La función {func.__name__} no tiene docstring")
                self.assertGreater(len(func.__doc__.strip()), 10,
                                 f"El docstring de {func.__name__} es muy corto")
            self.__class__.score += 1
            self.__class__.test_results.append(("Funciones con docstring", True, 1))
        except AssertionError as e:
            self.__class__.test_results.append(("Funciones con docstring", False, 0))
            raise e
    
    def test_04_nombres_variables(self):
        """Test 4: Verificar que los nombres de variables tienen al menos 4 caracteres."""
        try:
            # Leer el archivo y buscar asignaciones de variables
            filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                   'src', 'ejercicio1.py')
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Buscar asignaciones simples (no es exhaustivo pero es ilustrativo)
            import re
            pattern = r'^(\s*)([a-zA-Z_]\w*)\s*='
            matches = re.findall(pattern, content, re.MULTILINE)
            
            short_vars = []
            for indent, var_name in matches:
                if len(var_name) < 4 and var_name not in ['i', 'j', 'n', 'df']:
                    short_vars.append(var_name)
            
            self.assertEqual(len(short_vars), 0, 
                           f"Variables con menos de 4 caracteres: {short_vars}")
            self.__class__.score += 1
            self.__class__.test_results.append(("Nombres de variables", True, 1))
        except AssertionError as e:
            self.__class__.test_results.append(("Nombres de variables", False, 0))
            raise e
    
    def test_05_cargar_dataset_con_archivo_temporal(self):
        """Test 5: Verificar que cargar_dataset funciona con un archivo temporal."""
        try:
            # Crear archivo temporal
            with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', 
                                            delete=False) as f:
                self.df_test.to_csv(f.name, index=False)
                temp_file = f.name
            
            # Cargar el archivo
            df_loaded = cargar_dataset(temp_file)
            
            # Verificaciones
            self.assertIsInstance(df_loaded, pd.DataFrame, 
                                "La función no devuelve un DataFrame")
            self.assertEqual(len(df_loaded), 3, 
                           "El DataFrame no tiene el número correcto de filas")
            self.assertEqual(len(df_loaded.columns), 5, 
                           "El DataFrame no tiene el número correcto de columnas")
            
            # Limpiar
            os.unlink(temp_file)
            
            self.__class__.score += 1
            self.__class__.test_results.append(("Cargar dataset", True, 1))
        except Exception as e:
            self.__class__.test_results.append(("Cargar dataset", False, 0))
            if 'temp_file' in locals():
                os.unlink(temp_file)
            raise e
    
    def test_06_cargar_dataset_archivo_inexistente(self):
        """Test 6: Verificar que cargar_dataset lanza excepción con archivo inexistente."""
        try:
            with self.assertRaises(FileNotFoundError):
                cargar_dataset('/ruta/inexistente/archivo.csv')
            self.__class__.score += 1
            self.__class__.test_results.append(("Manejo de errores", True, 1))
        except AssertionError as e:
            self.__class__.test_results.append(("Manejo de errores", False, 0))
            raise e
    
    def test_07_mostrar_primeras_filas(self):
        """Test 7: Verificar que mostrar_primeras_filas funciona correctamente."""
        try:
            # Capturar la salida
            from io import StringIO
            import sys
            
            captured_output = StringIO()
            sys.stdout = captured_output
            
            result = mostrar_primeras_filas(self.df_test, n=2)
            
            sys.stdout = sys.__stdout__
            
            # Verificaciones
            self.assertIsInstance(result, pd.DataFrame, 
                                "No devuelve un DataFrame")
            self.assertEqual(len(result), 2, 
                           "No devuelve el número correcto de filas")
            
            output = captured_output.getvalue()
            self.assertIn("Primeras", output, 
                         "No imprime el mensaje esperado")
            
            self.__class__.score += 1
            self.__class__.test_results.append(("Mostrar primeras filas", True, 1))
        except AssertionError as e:
            self.__class__.test_results.append(("Mostrar primeras filas", False, 0))
            raise e
    
    def test_08_mostrar_columnas(self):
        """Test 8: Verificar que mostrar_columnas funciona correctamente."""
        try:
            from io import StringIO
            import sys
            
            captured_output = StringIO()
            sys.stdout = captured_output
            
            result = mostrar_columnas(self.df_test)
            
            sys.stdout = sys.__stdout__
            
            # Verificaciones
            self.assertIsInstance(result, pd.Index, 
                                "No devuelve un pd.Index")
            self.assertEqual(len(result), 5, 
                           "No devuelve el número correcto de columnas")
            
            output = captured_output.getvalue()
            self.assertIn("Columnas", output, 
                         "No imprime el mensaje esperado")
            
            self.__class__.score += 1
            self.__class__.test_results.append(("Mostrar columnas", True, 1))
        except AssertionError as e:
            self.__class__.test_results.append(("Mostrar columnas", False, 0))
            raise e
    
    def test_09_ejecutar_ejercicio1_completo(self):
        """Test 9: Verificar que ejecutar_ejercicio1 funciona correctamente."""
        try:
            # Ejecutar con DataFrame de prueba
            from io import StringIO
            import sys
            
            captured_output = StringIO()
            sys.stdout = captured_output
            
            result = ejecutar_ejercicio1(self.df_test)
            
            sys.stdout = sys.__stdout__
            
            # Verificaciones
            self.assertIsInstance(result, pd.DataFrame, 
                                "No devuelve un DataFrame")
            
            output = captured_output.getvalue()
            self.assertIn("EJERCICIO 1", output, 
                         "No imprime el título del ejercicio")
            self.assertIn("Columnas", output, 
                         "No muestra las columnas")
            
            self.__class__.score += 1
            self.__class__.test_results.append(("Ejecución completa", True, 1))
        except AssertionError as e:
            self.__class__.test_results.append(("Ejecución completa", False, 0))
            raise e
    
    @classmethod
    def tearDownClass(cls):
        """Mostrar resumen de resultados al final."""
        print(f"\n{'='*50}")
        print(f"RESUMEN TEST EJERCICIO 1")
        print(f"{'='*50}")
        for test_name, passed, score in cls.test_results:
            status = "✓" if passed else "✗"
            print(f"{status} {test_name}: {score}/1")
        print(f"{'='*50}")
        print(f"PUNTUACIÓN TOTAL: {cls.score}/{cls.max_score}")
        print(f"{'='*50}\n")