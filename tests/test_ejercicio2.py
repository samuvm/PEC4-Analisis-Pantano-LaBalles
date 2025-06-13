# =======================
# ARCHIVO: tests/test_ejercicio2.py
# =======================

"""
Tests para el Ejercicio 2: Limpieza de datos y filtrado.

Este módulo contiene las pruebas unitarias para verificar el correcto
funcionamiento de las funciones del ejercicio 2.
"""

import unittest
import os
import sys
import pandas as pd
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

from src.ejercicio2 import (
    renombrar_columnas,
    mostrar_pantanos_unicos,
    limpiar_nombres_pantanos,
    filtrar_la_baells,
    ejecutar_ejercicio2
)


class TestEjercicio2(unittest.TestCase):
    """Clase de tests para el ejercicio 2."""
    
    @classmethod
    def setUpClass(cls):
        """Configuración inicial para todos los tests."""
        cls.score = 0
        cls.max_score = 10
        cls.test_results = []
    
    def setUp(self):
        """Configuración para cada test individual."""
        # Crear un DataFrame de prueba con nombres originales
        self.df_test = pd.DataFrame({
            'Dia': ['01/01/2024', '02/01/2024', '03/01/2024', '04/01/2024'],
            'Estació': ['Embassament de la Baells (Berga)', 
                       'Embassament de Sau (Vilanova de Sau)', 
                       'Embassament de la Baells (Berga)',
                       'Embassament de Susqueda (Susqueda)'],
            'Nivell absolut (msnm)': [632.5, 425.3, 633.1, 337.2],
            'Percentatge volum embassat (%)': [75.2, 68.5, 76.8, 82.1],
            'Volum embassat (hm3)': [82.3, 125.6, 84.1, 178.9]
        })
    
    def test_01_archivo_existe(self):
        """Test 1: Verificar que el archivo ejercicio2.py existe."""
        try:
            filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                   'src', 'ejercicio2.py')
            self.assertTrue(os.path.exists(filepath), 
                           "El archivo ejercicio2.py no existe")
            self.__class__.score += 1
            self.__class__.test_results.append(("Archivo existe", True, 1))
        except AssertionError as e:
            self.__class__.test_results.append(("Archivo existe", False, 0))
            raise e
    
    def test_02_docstring_modulo(self):
        """Test 2: Verificar que el módulo tiene docstring."""
        try:
            import src.ejercicio2
            self.assertIsNotNone(src.ejercicio2.__doc__, 
                               "El módulo no tiene docstring")
            self.assertGreater(len(src.ejercicio2.__doc__.strip()), 20,
                             "El docstring del módulo es muy corto")
            self.__class__.score += 1
            self.__class__.test_results.append(("Docstring del módulo", True, 1))
        except AssertionError as e:
            self.__class__.test_results.append(("Docstring del módulo", False, 0))
            raise e
    
    def test_03_renombrar_columnas(self):
        """Test 3: Verificar que renombrar_columnas funciona correctamente."""
        try:
            from io import StringIO
            import sys
            
            captured_output = StringIO()
            sys.stdout = captured_output
            
            df_renamed = renombrar_columnas(self.df_test.copy())
            
            sys.stdout = sys.__stdout__
            
            # Verificar nuevos nombres de columnas
            expected_columns = ['dia', 'estacio', 'nivell_msnm', 'nivell_perc', 'volum']
            self.assertListEqual(list(df_renamed.columns), expected_columns,
                               "Las columnas no se renombraron correctamente")
            
            # Verificar que los datos se mantienen
            self.assertEqual(len(df_renamed), len(self.df_test),
                           "Se perdieron filas al renombrar")
            
            self.__class__.score += 1
            self.__class__.test_results.append(("Renombrar columnas", True, 1))
        except AssertionError as e:
            self.__class__.test_results.append(("Renombrar columnas", False, 0))
            raise e
    
    def test_04_mostrar_pantanos_unicos(self):
        """Test 4: Verificar que mostrar_pantanos_unicos funciona correctamente."""
        try:
            # Primero renombrar columnas
            df_renamed = renombrar_columnas(self.df_test.copy())
            
            from io import StringIO
            import sys
            
            captured_output = StringIO()
            sys.stdout = captured_output
            
            pantanos = mostrar_pantanos_unicos(df_renamed)
            
            sys.stdout = sys.__stdout__
            output = captured_output.getvalue()
            
            # Verificaciones
            self.assertEqual(len(pantanos), 3,
                           "No se detectaron todos los pantanos únicos")
            self.assertIn("pantanos únicos", output.lower(),
                         "No se muestra el conteo de pantanos")
            
            self.__class__.score += 1
            self.__class__.test_results.append(("Pantanos únicos", True, 1))
        except AssertionError as e:
            self.__class__.test_results.append(("Pantanos únicos", False, 0))
            raise e
    
    def test_05_limpiar_nombres_pantanos(self):
        """Test 5: Verificar que limpiar_nombres_pantanos funciona correctamente."""
        try:
            # Preparar datos
            df_renamed = renombrar_columnas(self.df_test.copy())
            
            from io import StringIO
            import sys
            
            captured_output = StringIO()
            sys.stdout = captured_output
            
            df_limpio = limpiar_nombres_pantanos(df_renamed)
            
            sys.stdout = sys.__stdout__
            
            # Verificar nombres limpiados
            nombres_esperados = {'la Baells', 'Sau', 'Susqueda'}
            nombres_obtenidos = set(df_limpio['estacio'].unique())
            
            self.assertEqual(nombres_esperados, nombres_obtenidos,
                           "Los nombres no se limpiaron correctamente")
            
            self.__class__.score += 1
            self.__class__.test_results.append(("Limpiar nombres", True, 1))
        except AssertionError as e:
            self.__class__.test_results.append(("Limpiar nombres", False, 0))
            raise e
    
    def test_06_uso_expresiones_regulares(self):
        """Test 6: Verificar que se usan expresiones regulares."""
        try:
            # Verificar que el código usa re
            filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                   'src', 'ejercicio2.py')
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.assertIn('import re', content,
                         "No se importa el módulo re")
            self.assertIn('re.sub', content,
                         "No se usa re.sub para limpiar nombres")
            
            self.__class__.score += 1
            self.__class__.test_results.append(("Uso de regex", True, 1))
        except AssertionError as e:
            self.__class__.test_results.append(("Uso de regex", False, 0))
            raise e
    
    def test_07_filtrar_la_baells(self):
        """Test 7: Verificar que filtrar_la_baells funciona correctamente."""
        try:
            # Preparar datos
            df_renamed = renombrar_columnas(self.df_test.copy())
            df_limpio = limpiar_nombres_pantanos(df_renamed)
            
            from io import StringIO
            import sys
            
            captured_output = StringIO()
            sys.stdout = captured_output
            
            df_baells = filtrar_la_baells(df_limpio)
            
            sys.stdout = sys.__stdout__
            output = captured_output.getvalue()
            
            # Verificaciones
            self.assertEqual(len(df_baells), 2,
                           "No se filtraron correctamente los datos de La Baells")
            self.assertTrue(all(df_baells['estacio'] == 'la Baells'),
                          "Hay datos que no son de La Baells")
            self.assertIn("La Baells", output,
                         "No se muestra información sobre el filtrado")
            
            self.__class__.score += 1
            self.__class__.test_results.append(("Filtrar La Baells", True, 1))
        except AssertionError as e:
            self.__class__.test_results.append(("Filtrar La Baells", False, 0))
            raise e
    
    def test_08_ejecutar_ejercicio2_completo(self):
        """Test 8: Verificar que ejecutar_ejercicio2 funciona completamente."""
        try:
            from io import StringIO
            import sys
            
            captured_output = StringIO()
            sys.stdout = captured_output
            
            df_resultado = ejecutar_ejercicio2(self.df_test)
            
            sys.stdout = sys.__stdout__
            output = captured_output.getvalue()
            
            # Verificaciones
            self.assertIsInstance(df_resultado, pd.DataFrame,
                                "No devuelve un DataFrame")
            self.assertEqual(len(df_resultado), 2,
                           "No devuelve el número correcto de filas")
            self.assertIn("EJERCICIO 2", output,
                         "No imprime el título del ejercicio")
            
            # Verificar que las columnas están renombradas
            expected_columns = ['dia', 'estacio', 'nivell_msnm', 'nivell_perc', 'volum']
            self.assertListEqual(list(df_resultado.columns), expected_columns,
                               "Las columnas finales no son correctas")
            
            self.__class__.score += 2  # Vale doble
            self.__class__.test_results.append(("Ejecución completa", True, 2))
        except AssertionError as e:
            self.__class__.test_results.append(("Ejecución completa", False, 0))
            raise e
    
    @classmethod
    def tearDownClass(cls):
        """Mostrar resumen de resultados al final."""
        print(f"\n{'='*50}")
        print(f"RESUMEN TEST EJERCICIO 2")
        print(f"{'='*50}")
        for test_name, passed, score in cls.test_results:
            status = "✓" if passed else "✗"
            print(f"{status} {test_name}: {score}/1")
        print(f"{'='*50}")
        print(f"PUNTUACIÓN TOTAL: {cls.score}/{cls.max_score}")
        print(f"{'='*50}\n")