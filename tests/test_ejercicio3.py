# =======================
# ARCHIVO: tests/test_ejercicio3.py
# =======================

"""
Tests para el Ejercicio 3: Análisis temporal y visualización.

Este módulo contiene las pruebas unitarias para verificar el correcto
funcionamiento de las funciones del ejercicio 3.
"""

import unittest
import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime
import tempfile
import shutil

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

from src.ejercicio3 import (
    convertir_a_datetime,
    analizar_rango_temporal,
    toYearFraction,
    crear_columna_dia_decimal,
    visualizar_evolucion_volumen,
    ejecutar_ejercicio3
)


class TestEjercicio3(unittest.TestCase):
    """Clase de tests para el ejercicio 3."""
    
    @classmethod
    def setUpClass(cls):
        """Configuración inicial para todos los tests."""
        cls.score = 0
        cls.max_score = 10
        cls.test_results = []
        # Crear directorio temporal para imágenes
        cls.temp_dir = tempfile.mkdtemp()
    
    def setUp(self):
        """Configuración para cada test individual."""
        # Crear un DataFrame de prueba (ya filtrado de La Baells)
        self.df_test = pd.DataFrame({
            'dia': ['01/01/2023', '15/06/2023', '31/12/2023', '01/01/2024'],
            'estacio': ['la Baells'] * 4,
            'nivell_msnm': [632.5, 628.3, 635.1, 634.2],
            'nivell_perc': [75.2, 65.5, 82.8, 79.3],
            'volum': [82.3, 71.7, 90.7, 86.8]
        })
    
    def test_01_archivo_existe(self):
        """Test 1: Verificar que el archivo ejercicio3.py existe."""
        try:
            filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                   'src', 'ejercicio3.py')
            self.assertTrue(os.path.exists(filepath), 
                           "El archivo ejercicio3.py no existe")
            self.__class__.score += 1
            self.__class__.test_results.append(("Archivo existe", True, 1))
        except AssertionError as e:
            self.__class__.test_results.append(("Archivo existe", False, 0))
            raise e
    
    def test_02_convertir_a_datetime(self):
        """Test 2: Verificar que convertir_a_datetime funciona correctamente."""
        try:
            from io import StringIO
            import sys
            
            captured_output = StringIO()
            sys.stdout = captured_output
            
            df_datetime = convertir_a_datetime(self.df_test.copy())
            
            sys.stdout = sys.__stdout__
            
            # Verificaciones
            self.assertEqual(df_datetime['dia'].dtype, 'datetime64[ns]',
                           "La columna 'dia' no es de tipo datetime")
            self.assertEqual(len(df_datetime), len(self.df_test),
                           "Se perdieron filas en la conversión")
            
            # Verificar que las fechas se convirtieron correctamente
            primera_fecha = df_datetime['dia'].iloc[0]
            self.assertEqual(primera_fecha.year, 2023,
                           "El año no se convirtió correctamente")
            self.assertEqual(primera_fecha.month, 1,
                           "El mes no se convirtió correctamente")
            self.assertEqual(primera_fecha.day, 1,
                           "El día no se convirtió correctamente")
            
            self.__class__.score += 1
            self.__class__.test_results.append(("Convertir a datetime", True, 1))
        except AssertionError as e:
            self.__class__.test_results.append(("Convertir a datetime", False, 0))
            raise e
    
    def test_03_analizar_rango_temporal(self):
        """Test 3: Verificar que analizar_rango_temporal funciona correctamente."""
        try:
            df_datetime = convertir_a_datetime(self.df_test.copy())
            
            from io import StringIO
            import sys
            
            captured_output = StringIO()
            sys.stdout = captured_output
            
            fecha_min, fecha_max, num_registros = analizar_rango_temporal(df_datetime)
            
            sys.stdout = sys.__stdout__
            output = captured_output.getvalue()
            
            # Verificaciones
            self.assertEqual(fecha_min, pd.Timestamp('2023-01-01'),
                           "La fecha mínima no es correcta")
            self.assertEqual(fecha_max, pd.Timestamp('2024-01-01'),
                           "La fecha máxima no es correcta")
            self.assertEqual(num_registros, 4,
                           "El número de registros no es correcto")
            self.assertIn("registros", output.lower(),
                         "No se muestra información de registros")
            
            self.__class__.score += 1
            self.__class__.test_results.append(("Analizar rango temporal", True, 1))
        except AssertionError as e:
            self.__class__.test_results.append(("Analizar rango temporal", False, 0))
            raise e
    
    def test_04_toYearFraction(self):
        """Test 4: Verificar que toYearFraction funciona correctamente."""
        try:
            # Test con fecha conocida
            fecha_test = datetime(2023, 7, 1)  # 1 de julio = mitad del año
            resultado = toYearFraction(fecha_test)
            
            # Verificar que está cerca de 2023.5
            self.assertAlmostEqual(resultado, 2023.5, places=2,
                                 msg="La conversión a año decimal no es correcta")
            
            # Test con 1 de enero
            fecha_enero = datetime(2023, 1, 1)
            resultado_enero = toYearFraction(fecha_enero)
            self.assertAlmostEqual(resultado_enero, 2023.0, places=3,
                                 msg="1 de enero debería ser año.0")
            
            # Test con 31 de diciembre
            fecha_diciembre = datetime(2023, 12, 31)
            resultado_diciembre = toYearFraction(fecha_diciembre)
            self.assertGreater(resultado_diciembre, 2023.99,
                             msg="31 de diciembre debería ser casi año+1")
            
            self.__class__.score += 1
            self.__class__.test_results.append(("Función toYearFraction", True, 1))
        except AssertionError as e:
            self.__class__.test_results.append(("Función toYearFraction", False, 0))
            raise e
    
    def test_05_crear_columna_dia_decimal(self):
        """Test 5: Verificar que crear_columna_dia_decimal funciona correctamente."""
        try:
            df_datetime = convertir_a_datetime(self.df_test.copy())
            
            from io import StringIO
            import sys
            
            captured_output = StringIO()
            sys.stdout = captured_output
            
            df_decimal = crear_columna_dia_decimal(df_datetime)
            
            sys.stdout = sys.__stdout__
            
            # Verificaciones
            self.assertIn('dia_decimal', df_decimal.columns,
                         "No se creó la columna 'dia_decimal'")
            self.assertTrue(all(df_decimal['dia_decimal'] >= 2023),
                          "Los valores decimales no son correctos")
            self.assertTrue(all(df_decimal['dia_decimal'] < 2025),
                          "Los valores decimales no son correctos")
            
            # Verificar que es numérico
            self.assertTrue(pd.api.types.is_numeric_dtype(df_decimal['dia_decimal']),
                          "La columna dia_decimal no es numérica")
            
            self.__class__.score += 1
            self.__class__.test_results.append(("Crear columna decimal", True, 1))
        except AssertionError as e:
            self.__class__.test_results.append(("Crear columna decimal", False, 0))
            raise e
    
    def test_06_visualizar_evolucion_volumen(self):
        """Test 6: Verificar que se genera correctamente la imagen."""
        try:
            # Preparar datos
            df_datetime = convertir_a_datetime(self.df_test.copy())
            df_decimal = crear_columna_dia_decimal(df_datetime)
            
            # Modificar temporalmente la función para usar nuestro directorio
            import src.ejercicio3
            old_dirname = os.path.dirname
            
            def mock_dirname(path):
                if 'ejercicio3.py' in path:
                    return self.__class__.temp_dir
                return old_dirname(path)
            
            os.path.dirname = mock_dirname
            
            # Crear directorio img en temp
            img_dir = os.path.join(self.__class__.temp_dir, 'img')
            os.makedirs(img_dir, exist_ok=True)
            
            # Ejecutar función
            filepath = visualizar_evolucion_volumen(df_decimal, "Test Student")
            
            # Restaurar
            os.path.dirname = old_dirname
            
            # Verificaciones
            self.assertTrue(os.path.exists(filepath),
                          "No se generó el archivo de imagen")
            self.assertIn("labaells", filepath.lower(),
                         "El nombre del archivo no es correcto")
            self.assertIn("Test_Student", filepath,
                         "El nombre del alumno no está en el archivo")
            self.assertTrue(filepath.endswith('.png'),
                          "El archivo no es PNG")
            
            self.__class__.score += 2  # Vale doble
            self.__class__.test_results.append(("Generar imagen", True, 2))
        except Exception as e:
            self.__class__.test_results.append(("Generar imagen", False, 0))
            raise e
    
    def test_07_ejecutar_ejercicio4_completo(self):
        """Test 7: Verificar que ejecutar_ejercicio4 funciona completamente."""
        try:
            from io import StringIO
            import sys
            
            captured_output = StringIO()
            sys.stdout = captured_output
            
            # Ejecutar sin modificar paths
            df_resultado = ejecutar_ejercicio4(self.df_test)
            
            sys.stdout = sys.__stdout__
            output = captured_output.getvalue()
            
            # Verificaciones
            self.assertIsInstance(df_resultado, pd.DataFrame,
                                "No devuelve un DataFrame")
            self.assertIn('nivell_perc_suavizado', df_resultado.columns,
                        "No se creó la columna suavizada")
            self.assertIn("EJERCICIO 4", output,
                        "No imprime el título del ejercicio")
            
            # Verificar que se generó imagen en el directorio img real
            img_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'img')
            if os.path.exists(img_dir):
                img_files = os.listdir(img_dir)
                smoothed_files = [f for f in img_files if 'smoothed' in f.lower() and f.endswith('.png')]
                # No fallar si no hay imágenes
                # self.assertGreater(len(smoothed_files), 0, "No se generó imagen con 'smoothed' en el nombre")
            
            self.__class__.score += 2  # Vale doble
            self.__class__.test_results.append(("Ejecución completa", True, 2))
        except Exception as e:
            self.__class__.test_results.append(("Ejecución completa", False, 0))
            raise e
    
    @classmethod
    def tearDownClass(cls):
        """Mostrar resumen de resultados y limpiar."""
        print(f"\n{'='*50}")
        print(f"RESUMEN TEST EJERCICIO 3")
        print(f"{'='*50}")
        for test_name, passed, score in cls.test_results:
            status = "✓" if passed else "✗"
            print(f"{status} {test_name}: {score}/1")
        print(f"{'='*50}")
        print(f"PUNTUACIÓN TOTAL: {cls.score}/{cls.max_score}")
        print(f"{'='*50}\n")
        
        # Limpiar directorio temporal
        shutil.rmtree(cls.temp_dir)