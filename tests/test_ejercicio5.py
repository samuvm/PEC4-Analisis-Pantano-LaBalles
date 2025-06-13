# =======================
# ARCHIVO: tests/test_ejercicio5.py
# =======================

"""
Tests para el Ejercicio 5: Identificación de períodos de sequía.

Este módulo contiene las pruebas unitarias para verificar el correcto
funcionamiento de las funciones del ejercicio 5.
"""

import unittest
import os
import sys
import pandas as pd
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

from src.ejercicio5 import (
    calcula_periodos,
    analizar_periodos_sequia,
    ejecutar_ejercicio5
)


class TestEjercicio5(unittest.TestCase):
    """Clase de tests para el ejercicio 5."""
    
    @classmethod
    def setUpClass(cls):
        """Configuración inicial para todos los tests."""
        cls.score = 0
        cls.max_score = 10
        cls.test_results = []
    
    def setUp(self):
        """Configuración para cada test individual."""
        # Crear datos con períodos claros de sequía
        n_points = 1000
        t = np.linspace(2020, 2024, n_points)
        
        # Crear señal con períodos bajo 60%
        signal = np.ones(n_points) * 70  # Base en 70%
        
        # Período de sequía 1: 2021.0 - 2021.5
        mask1 = (t >= 2021.0) & (t <= 2021.5)
        signal[mask1] = 45
        
        # Período de sequía 2: 2022.5 - 2023.0
        mask2 = (t >= 2022.5) & (t <= 2023.0)
        signal[mask2] = 50
        
        # Período de sequía 3: 2023.8 - 2024.0
        mask3 = (t >= 2023.8) & (t <= 2024.0)
        signal[mask3] = 55
        
        self.df_test = pd.DataFrame({
            'dia': pd.date_range('2020-01-01', periods=n_points, freq='D'),
            'dia_decimal': t,
            'estacio': ['la Baells'] * n_points,
            'nivell_msnm': np.random.uniform(630, 640, n_points),
            'nivell_perc': signal + np.random.normal(0, 0.5, n_points),
            'nivell_perc_suavizado': signal,  # Sin ruido para test
            'volum': signal * 1.1
        })
    
    def test_01_archivo_existe(self):
        """Test 1: Verificar que el archivo ejercicio5.py existe."""
        try:
            filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                   'src', 'ejercicio5.py')
            self.assertTrue(os.path.exists(filepath), 
                           "El archivo ejercicio5.py no existe")
            self.__class__.score += 1
            self.__class__.test_results.append(("Archivo existe", True, 1))
        except AssertionError as e:
            self.__class__.test_results.append(("Archivo existe", False, 0))
            raise e
    
    def test_02_calcula_periodos_basico(self):
        """Test 2: Verificar que calcula_periodos detecta períodos correctamente."""
        try:
            from io import StringIO
            import sys
            
            captured_output = StringIO()
            sys.stdout = captured_output
            
            periodos = calcula_periodos(self.df_test, umbral=60)
            
            sys.stdout = sys.__stdout__
            
            # Verificaciones
            self.assertIsInstance(periodos, list,
                                "No devuelve una lista")
            self.assertEqual(len(periodos), 3,
                           f"Debería detectar 3 períodos, detectó {len(periodos)}")
            
            # Verificar formato de períodos
            for periodo in periodos:
                self.assertIsInstance(periodo, list,
                                    "Cada período debe ser una lista")
                self.assertEqual(len(periodo), 2,
                               "Cada período debe tener inicio y fin")
                self.assertLess(periodo[0], periodo[1],
                              "El inicio debe ser menor que el fin")
            
            self.__class__.score += 2  # Vale doble
            self.__class__.test_results.append(("Calcular períodos", True, 2))
        except AssertionError as e:
            self.__class__.test_results.append(("Calcular períodos", False, 0))
            raise e
    
    def test_03_calcula_periodos_valores_correctos(self):
        """Test 3: Verificar que los valores de los períodos son correctos."""
        try:
            periodos = calcula_periodos(self.df_test, umbral=60)
            
            # Verificar que los períodos están en los rangos esperados
            # Permitir cierta tolerancia por el redondeo
            tolerancia = 0.1
            
            # Período 1: alrededor de 2021.0 - 2021.5
            periodo1 = periodos[0]
            self.assertAlmostEqual(periodo1[0], 2021.0, delta=tolerancia,
                                 msg="Inicio del período 1 incorrecto")
            self.assertAlmostEqual(periodo1[1], 2021.5, delta=tolerancia,
                                 msg="Fin del período 1 incorrecto")
            
            self.__class__.score += 1
            self.__class__.test_results.append(("Valores de períodos", True, 1))
        except AssertionError as e:
            self.__class__.test_results.append(("Valores de períodos", False, 0))
            raise e
    
    def test_04_analizar_periodos_sequia(self):
        """Test 4: Verificar que analizar_periodos_sequia funciona correctamente."""
        try:
            periodos = calcula_periodos(self.df_test, umbral=60)
            
            from io import StringIO
            import sys
            
            captured_output = StringIO()
            sys.stdout = captured_output
            
            df_info = analizar_periodos_sequia(self.df_test, periodos)
            
            sys.stdout = sys.__stdout__
            output = captured_output.getvalue()
            
            # Verificaciones
            self.assertIsInstance(df_info, pd.DataFrame,
                                "No devuelve un DataFrame")
            self.assertEqual(len(df_info), len(periodos),
                           "Debe haber una fila por período")
            
            # Verificar columnas esperadas
            columnas_esperadas = ['Período', 'Inicio (decimal)', 'Fin (decimal)', 
                                'Duración (años)', 'Duración (días)']
            for col in columnas_esperadas:
                self.assertIn(col, df_info.columns,
                            f"Falta la columna '{col}'")
            
            # Verificar que se imprime información
            self.assertIn("Período", output,
                         "No se muestra información de períodos")
            
            self.__class__.score += 1
            self.__class__.test_results.append(("Analizar períodos", True, 1))
        except AssertionError as e:
            self.__class__.test_results.append(("Analizar períodos", False, 0))
            raise e
    
    def test_05_formato_salida_periodos(self):
        """Test 5: Verificar el formato de salida de los períodos."""
        try:
            periodos = calcula_periodos(self.df_test, umbral=60)
            
            # Verificar formato [[inicio, fin], ...]
            ejemplo_str = str(periodos)
            self.assertIn("[[", ejemplo_str,
                         "El formato no empieza con [[")
            self.assertIn("]]", ejemplo_str,
                         "El formato no termina con ]]")
            
            # Verificar que son números decimales
            for periodo in periodos:
                self.assertIsInstance(periodo[0], (int, float),
                                    "El inicio debe ser numérico")
                self.assertIsInstance(periodo[1], (int, float),
                                    "El fin debe ser numérico")
                self.assertGreater(periodo[0], 2000,
                                 "Los años deben ser > 2000")
                self.assertLess(periodo[1], 2030,
                              "Los años deben ser < 2030")
            
            self.__class__.score += 1
            self.__class__.test_results.append(("Formato de salida", True, 1))
        except AssertionError as e:
            self.__class__.test_results.append(("Formato de salida", False, 0))
            raise e
    

    def test_06_ejecutar_ejercicio5_completo(self):
        """Test 6: Verificar que ejecutar_ejercicio5 funciona completamente."""
        try:
            from io import StringIO
            import sys
            
            captured_output = StringIO()
            sys.stdout = captured_output
            
            periodos, df_info = ejecutar_ejercicio5(self.df_test)
            
            sys.stdout = sys.__stdout__
            output = captured_output.getvalue()
            
            # Verificaciones
            self.assertIsInstance(periodos, list,
                                "No devuelve lista de períodos")
            self.assertIsInstance(df_info, pd.DataFrame,
                                "No devuelve DataFrame de información")
            self.assertIn("EJERCICIO 5", output,
                        "No imprime el título del ejercicio")
            self.assertIn("sequía", output.lower(),
                        "No menciona la palabra sequía")
            
            # Verificar que imprime información sobre los períodos
            # Buscar cualquier formato de número decimal (con o sin np.float64)
            import re
            for periodo in periodos:
                # Buscar el número en cualquier formato
                inicio_str = f"{periodo[0]:.2f}"
                # Verificar que aparece el número de alguna forma
                pattern = rf"{periodo[0]:.1f}|{periodo[0]:.2f}|{int(periodo[0])}"
                self.assertTrue(re.search(pattern, output),
                            f"No se encuentra información del período {periodo}")
            
            self.__class__.score += 2  # Vale doble
            self.__class__.test_results.append(("Ejecución completa", True, 2))
        except AssertionError as e:
            self.__class__.test_results.append(("Ejecución completa", False, 0))
            raise e

    
    def test_07_umbral_60_porciento(self):
        """Test 7: Verificar que se usa el umbral del 60%."""
        try:
            # Crear datos específicos para este test
            df_umbral = self.df_test.copy()
            df_umbral['nivell_perc_suavizado'] = 65  # Todo por encima del 60%
            
            periodos = calcula_periodos(df_umbral, umbral=60)
            self.assertEqual(len(periodos), 0,
                           "No debería detectar períodos si todo está sobre 60%")
            
            # Ahora todo por debajo
            df_umbral['nivell_perc_suavizado'] = 55
            periodos = calcula_periodos(df_umbral, umbral=60)
            self.assertEqual(len(periodos), 1,
                           "Debería detectar un solo período largo")
            
            self.__class__.score += 1
            self.__class__.test_results.append(("Umbral 60%", True, 1))
        except AssertionError as e:
            self.__class__.test_results.append(("Umbral 60%", False, 0))
            raise e
    
    @classmethod
    def tearDownClass(cls):
        """Mostrar resumen de resultados al final."""
        print(f"\n{'='*50}")
        print(f"RESUMEN TEST EJERCICIO 5")
        print(f"{'='*50}")
        for test_name, passed, score in cls.test_results:
            status = "✓" if passed else "✗"
            print(f"{status} {test_name}: {score}/1")
        print(f"{'='*50}")
        print(f"PUNTUACIÓN TOTAL: {cls.score}/{cls.max_score}")
        print(f"{'='*50}\n")