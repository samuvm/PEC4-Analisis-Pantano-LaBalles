# =======================
# ARCHIVO: tests/test_ejercicio4.py CORREGIDO
# =======================

"""
Tests para el Ejercicio 4: Suavizado de señal y análisis de tendencias.

Este módulo contiene las pruebas unitarias para verificar el correcto
funcionamiento de las funciones del ejercicio 4.
"""

import unittest
import os
import sys
import pandas as pd
import numpy as np
import tempfile
import shutil

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

from src.ejercicio4 import (
    suavizar_serie_temporal,
    visualizar_serie_suavizada,
    analizar_tendencias,
    ejecutar_ejercicio4
)


class TestEjercicio4(unittest.TestCase):
    """Clase de tests para el ejercicio 4."""
    
    @classmethod
    def setUpClass(cls):
        """Configuración inicial para todos los tests."""
        cls.score = 0
        cls.max_score = 10
        cls.test_results = []
        cls.temp_dir = tempfile.mkdtemp()
    
    def setUp(self):
        """Configuración para cada test individual."""
        # Crear serie temporal con ruido para test de suavizado
        np.random.seed(42)
        n_points = 2000
        t = np.linspace(2020, 2024, n_points)
        
        # Señal base con tendencia y estacionalidad
        signal = 70 + 10 * np.sin(2 * np.pi * t) + 5 * np.sin(4 * np.pi * t)
        # Añadir ruido
        noise = np.random.normal(0, 2, n_points)
        noisy_signal = signal + noise
        
        # Crear períodos de sequía (valores bajos)
        drought_mask1 = (t >= 2021) & (t <= 2021.5)
        drought_mask2 = (t >= 2023) & (t <= 2023.3)
        noisy_signal[drought_mask1] = 45 + noise[drought_mask1]
        noisy_signal[drought_mask2] = 50 + noise[drought_mask2]
        
        self.df_test = pd.DataFrame({
            'dia': pd.date_range('2020-01-01', periods=n_points, freq='D'),
            'dia_decimal': t,
            'estacio': ['la Baells'] * n_points,
            'nivell_msnm': np.random.uniform(630, 640, n_points),
            'nivell_perc': noisy_signal,
            'volum': noisy_signal * 1.1
        })
    
    def test_01_archivo_existe(self):
        """Test 1: Verificar que el archivo ejercicio4.py existe."""
        try:
            filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                   'src', 'ejercicio4.py')
            self.assertTrue(os.path.exists(filepath), 
                           "El archivo ejercicio4.py no existe")
            self.__class__.score += 1
            self.__class__.test_results.append(("Archivo existe", True, 1))
        except AssertionError as e:
            self.__class__.test_results.append(("Archivo existe", False, 0))
            raise e
    
    def test_02_importa_scipy(self):
        """Test 2: Verificar que se importa scipy correctamente."""
        try:
            filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                   'src', 'ejercicio4.py')
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.assertIn('from scipy', content,
                         "No se importa scipy")
            self.assertIn('savgol_filter', content,
                         "No se importa savgol_filter")
            
            self.__class__.score += 1
            self.__class__.test_results.append(("Importa scipy", True, 1))
        except AssertionError as e:
            self.__class__.test_results.append(("Importa scipy", False, 0))
            raise e
    
    def test_03_suavizar_serie_temporal(self):
        """Test 3: Verificar que suavizar_serie_temporal funciona correctamente."""
        try:
            from io import StringIO
            import sys
            
            captured_output = StringIO()
            sys.stdout = captured_output
            
            df_suavizado = suavizar_serie_temporal(self.df_test.copy(), 
                                                  window_length=101, 
                                                  polyorder=3)
            
            sys.stdout = sys.__stdout__
            
            # Verificaciones
            self.assertIn('nivell_perc_suavizado', df_suavizado.columns,
                         "No se creó la columna suavizada")
            
            # Verificar que el suavizado reduce la variabilidad
            std_original = self.df_test['nivell_perc'].std()
            std_suavizado = df_suavizado['nivell_perc_suavizado'].std()
            self.assertLess(std_suavizado, std_original,
                          "El suavizado no reduce la variabilidad")
            
            # Verificar que se mantiene el rango general de valores
            self.assertAlmostEqual(
                df_suavizado['nivell_perc_suavizado'].mean(),
                self.df_test['nivell_perc'].mean(),
                delta=5,
                msg="El suavizado altera demasiado la media"
            )
            
            self.__class__.score += 1
            self.__class__.test_results.append(("Suavizar serie", True, 1))
        except AssertionError as e:
            self.__class__.test_results.append(("Suavizar serie", False, 0))
            raise e
    
    def test_04_parametros_savgol(self):
        """Test 4: Verificar que se usan los parámetros correctos de savgol_filter."""
        try:
            filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                   'src', 'ejercicio4.py')
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Verificar que se mencionan los parámetros
            self.assertIn('window_length=1500', content,
                         "No se usa window_length=1500")
            self.assertIn('polyorder=3', content,
                         "No se usa polyorder=3")
            
            self.__class__.score += 1
            self.__class__.test_results.append(("Parámetros savgol", True, 1))
        except AssertionError as e:
            self.__class__.test_results.append(("Parámetros savgol", False, 0))
            raise e
    
    def test_05_visualizar_serie_suavizada(self):
        """Test 5: Verificar que se genera la imagen con serie suavizada."""
        try:
            # Preparar datos
            df_suavizado = suavizar_serie_temporal(self.df_test.copy(), 
                                                  window_length=101, 
                                                  polyorder=3)
            
            # Modificar temporalmente para usar directorio temporal
            import src.ejercicio4
            old_dirname = os.path.dirname
            
            def mock_dirname(path):
                if 'ejercicio4.py' in path:
                    return self.__class__.temp_dir
                return old_dirname(path)
            
            os.path.dirname = mock_dirname
            
            # Crear directorio img
            img_dir = os.path.join(self.__class__.temp_dir, 'img')
            os.makedirs(img_dir, exist_ok=True)
            
            filepath = visualizar_serie_suavizada(df_suavizado, "Test Student")
            
            os.path.dirname = old_dirname
            
            # Verificaciones
            self.assertTrue(os.path.exists(filepath),
                          "No se generó el archivo de imagen")
            self.assertIn("smoothed", filepath.lower(),
                         "El nombre del archivo no contiene 'smoothed'")
            self.assertTrue(filepath.endswith('.png'),
                          "El archivo no es PNG")
            
            self.__class__.score += 2  # Vale doble
            self.__class__.test_results.append(("Generar imagen suavizada", True, 2))
        except Exception as e:
            self.__class__.test_results.append(("Generar imagen suavizada", False, 0))
            raise e
    
    def test_06_analizar_tendencias(self):
        """Test 6: Verificar que analizar_tendencias funciona correctamente."""
        try:
            df_suavizado = suavizar_serie_temporal(self.df_test.copy(), 
                                                  window_length=101, 
                                                  polyorder=3)
            
            from io import StringIO
            import sys
            
            captured_output = StringIO()
            sys.stdout = captured_output
            
            estadisticas = analizar_tendencias(df_suavizado)
            
            sys.stdout = sys.__stdout__
            output = captured_output.getvalue()
            
            # Verificaciones
            self.assertIsInstance(estadisticas, dict,
                                "No devuelve un diccionario")
            
            keys_esperadas = ['min_volumen', 'fecha_min_volumen', 
                            'max_volumen', 'fecha_max_volumen',
                            'dias_bajo_60', 'porcentaje_tiempo_sequia']
            
            for key in keys_esperadas:
                self.assertIn(key, estadisticas,
                            f"Falta la clave '{key}' en estadísticas")
            
            self.assertIn("60%", output,
                         "No se menciona el umbral del 60%")
            
            self.__class__.score += 1
            self.__class__.test_results.append(("Analizar tendencias", True, 1))
        except AssertionError as e:
            self.__class__.test_results.append(("Analizar tendencias", False, 0))
            raise e
    
    def test_07_ejecutar_ejercicio4_completo(self):
        """Test 7: Verificar que ejecutar_ejercicio4 funciona completamente."""
        try:
            from io import StringIO
            import sys
            
            captured_output = StringIO()
            sys.stdout = captured_output
            
            # Simplemente ejecutar sin mocking - el test verificará la funcionalidad
            df_resultado = ejecutar_ejercicio4(self.df_test)
            
            sys.stdout = sys.__stdout__
            output = captured_output.getvalue()
            
            # Verificaciones básicas
            self.assertIsInstance(df_resultado, pd.DataFrame,
                                "No devuelve un DataFrame")
            self.assertIn('nivell_perc_suavizado', df_resultado.columns,
                         "No se creó la columna suavizada")
            self.assertIn("EJERCICIO 4", output,
                         "No imprime el título del ejercicio")
            
            # Verificar que menciona que se guardó la imagen
            self.assertIn("guardado", output.lower(),
                         "No menciona que se guardó la imagen")
            
            self.__class__.score += 2  # Vale doble
            self.__class__.test_results.append(("Ejecución completa", True, 2))
        except Exception as e:
            self.__class__.test_results.append(("Ejecución completa", False, 0))
            raise e
    
    @classmethod
    def tearDownClass(cls):
        """Mostrar resumen de resultados y limpiar."""
        print(f"\n{'='*50}")
        print(f"RESUMEN TEST EJERCICIO 4")
        print(f"{'='*50}")
        for test_name, passed, score in cls.test_results:
            status = "✓" if passed else "✗"
            print(f"{status} {test_name}: {score}/1")
        print(f"{'='*50}")
        print(f"PUNTUACIÓN TOTAL: {cls.score}/{cls.max_score}")
        print(f"{'='*50}\n")
        
        # Limpiar directorio temporal
        try:
            shutil.rmtree(cls.temp_dir)
        except:
            pass  # No es crítico si falla la limpieza
