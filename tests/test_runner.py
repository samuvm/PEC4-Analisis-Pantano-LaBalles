"""
Test Runner principal con interfaz HTML para ejecutar todos los tests.

Este módulo permite ejecutar todos los tests de manera interactiva
y genera un reporte HTML con los resultados.
"""

import unittest
import os
import sys
import argparse
import webbrowser
from datetime import datetime
import HtmlTestRunner

# Asegurar que el directorio src está en el path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)


# Parche para arreglar el bug de HtmlTestRunner
class PatchedHtmlTestResult(HtmlTestRunner.result.HtmlTestResult):
    """Versión parcheada de HtmlTestResult para arreglar el bug de _count_relevant_tb_levels."""
    
    def _count_relevant_tb_levels(self, tb):
        """Cuenta los niveles relevantes del traceback."""
        # Implementación simple basada en unittest estándar
        length = 0
        while tb is not None:
            if self._is_relevant_tb_level(tb):
                length += 1
            tb = tb.tb_next
        return length


# Reemplazar la clase original con la parcheada
HtmlTestRunner.result.HtmlTestResult = PatchedHtmlTestResult


class CustomTestResult(unittest.TestResult):
    """Clase personalizada para capturar resultados de tests."""
    
    def __init__(self):
        super().__init__()
        self.test_results = []
        self.exercise_scores = {
            'ejercicio1': 0,
            'ejercicio2': 0,
            'ejercicio3': 0,
            'ejercicio4': 0,
            'ejercicio5': 0
        }
    
    def addSuccess(self, test):
        super().addSuccess(test)
        self.test_results.append({
            'test': str(test),
            'status': 'PASS',
            'message': 'Test ejecutado correctamente'
        })
    
    def addError(self, test, err):
        super().addError(test, err)
        self.test_results.append({
            'test': str(test),
            'status': 'ERROR',
            'message': str(err[1])
        })
    
    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.test_results.append({
            'test': str(test),
            'status': 'FAIL',
            'message': str(err[1])
        })


def ejecutar_test_individual(ejercicio_num):
    """
    Ejecuta los tests de un ejercicio específico.
    
    Parameters
    ----------
    ejercicio_num : int
        Número del ejercicio a testear (1-5).
        
    Returns
    -------
    unittest.TestResult
        Resultado de los tests.
    """
    # Importar el módulo de test correspondiente
    module_name = f'tests.test_ejercicio{ejercicio_num}'
    try:
        test_module = __import__(module_name, fromlist=[''])
    except ImportError as e:
        print(f"Error importando {module_name}: {e}")
        return None
    
    # Crear suite de tests
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(test_module)
    
    # Ejecutar tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


def ejecutar_todos_tests_html(directorio_salida='test_reports'):
    """
    Ejecuta todos los tests y genera un reporte HTML.
    
    Parameters
    ----------
    directorio_salida : str
        Directorio donde guardar el reporte HTML.
    """
    # Crear directorio si no existe
    os.makedirs(directorio_salida, exist_ok=True)
    
    # Crear directorio img si no existe (para evitar errores en tests)
    img_dir = os.path.join(parent_dir, 'img')
    os.makedirs(img_dir, exist_ok=True)
    
    # Descubrir todos los tests
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(__file__)
    suite = loader.discover(start_dir, pattern='test_ejercicio*.py')
    
    try:
        # Configurar el runner HTML
        runner = HtmlTestRunner.HTMLTestRunner(
            output=directorio_salida,
            report_name='PEC4_TestReport',
            report_title='Reporte de Tests - PEC4 Análisis de Embalses',
            descriptions=True,
            verbosity=2,
            add_timestamp=True,
            combine_reports=True  # Combinar todos los tests en un solo reporte
        )
        
        # Ejecutar tests
        print("\n" + "="*60)
        print("EJECUTANDO TODOS LOS TESTS")
        print("="*60)
        
        result = runner.run(suite)
        
        # Mostrar resumen
        print("\n" + "="*60)
        print("RESUMEN DE RESULTADOS")
        print("="*60)
        print(f"Tests ejecutados: {result.testsRun}")
        print(f"Exitosos: {result.testsRun - len(result.failures) - len(result.errors)}")
        print(f"Fallos: {len(result.failures)}")
        print(f"Errores: {len(result.errors)}")
        
        # Calcular puntuación global
        puntuacion_total = 0
        puntuacion_maxima = 50  # 10 puntos por ejercicio
        
        # Obtener puntuaciones de cada ejercicio
        for i in range(1, 6):
            try:
                module_name = f'tests.test_ejercicio{i}'
                test_module = sys.modules.get(module_name)
                if test_module and hasattr(test_module, f'TestEjercicio{i}'):
                    test_class = getattr(test_module, f'TestEjercicio{i}')
                    if hasattr(test_class, 'score'):
                        puntuacion_total += test_class.score
            except:
                pass
        
        porcentaje = (puntuacion_total / puntuacion_maxima) * 100
        
        print(f"\nPUNTUACIÓN TOTAL: {puntuacion_total}/{puntuacion_maxima} ({porcentaje:.1f}%)")
        
        # Calcular nota
        if porcentaje >= 90:
            nota = "EXCELENTE (9-10)"
        elif porcentaje >= 80:
            nota = "MUY BIEN (8-9)"
        elif porcentaje >= 70:
            nota = "BIEN (7-8)"
        elif porcentaje >= 60:
            nota = "SUFICIENTE (6-7)"
        elif porcentaje >= 50:
            nota = "APROBADO (5-6)"
        else:
            nota = "SUSPENSO (<5)"
        
        print(f"CALIFICACIÓN: {nota}")
        print("="*60)
        
        # Abrir el reporte en el navegador
        report_path = os.path.join(os.path.abspath(directorio_salida), 'PEC4_TestReport.html')
        if os.path.exists(report_path):
            print(f"\n✓ Reporte HTML generado en: {report_path}")
            print("Abriendo en el navegador...")
            webbrowser.open(f'file://{report_path}')
        else:
            print(f"\n⚠️  No se encontró el reporte en: {report_path}")
        
        return result
        
    except Exception as e:
        print(f"\n❌ Error durante la ejecución de tests: {e}")
        print("\nEjecutando tests sin HTML...")
        
        # Fallback: ejecutar sin HTML
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        return result


def ejecutar_todos_tests_simple():
    """Ejecuta todos los tests sin generar HTML."""
    print("\n" + "="*60)
    print("EJECUTANDO TODOS LOS TESTS (sin HTML)")
    print("="*60)
    
    for i in range(1, 6):
        print(f"\n{'='*60}")
        print(f"Ejecutando tests del Ejercicio {i}")
        print('='*60)
        ejecutar_test_individual(i)
    
    # Mostrar resumen de puntuaciones
    print("\n" + "="*60)
    print("RESUMEN DE PUNTUACIONES")
    print("="*60)
    
    puntuacion_total = 0
    for i in range(1, 6):
        try:
            module_name = f'tests.test_ejercicio{i}'
            test_module = sys.modules.get(module_name)
            if test_module and hasattr(test_module, f'TestEjercicio{i}'):
                test_class = getattr(test_module, f'TestEjercicio{i}')
                if hasattr(test_class, 'score'):
                    print(f"Ejercicio {i}: {test_class.score}/10")
                    puntuacion_total += test_class.score
        except:
            print(f"Ejercicio {i}: No se pudo obtener puntuación")
    
    print(f"\nPUNTUACIÓN TOTAL: {puntuacion_total}/50")
    print("="*60)


def menu_interactivo():
    """Muestra un menú interactivo para ejecutar tests."""
    while True:
        print("\n" + "="*60)
        print("TEST RUNNER - PEC4")
        print("="*60)
        print("1. Ejecutar tests del Ejercicio 1")
        print("2. Ejecutar tests del Ejercicio 2")
        print("3. Ejecutar tests del Ejercicio 3")
        print("4. Ejecutar tests del Ejercicio 4")
        print("5. Ejecutar tests del Ejercicio 5")
        print("6. Ejecutar TODOS los tests (con reporte HTML)")
        print("7. Ejecutar TODOS los tests (sin HTML)")
        print("0. Salir")
        print("="*60)
        
        opcion = input("Selecciona una opción (0-7): ").strip()
        
        if opcion == '0':
            print("\n¡Hasta luego!")
            break
        elif opcion in ['1', '2', '3', '4', '5']:
            print(f"\n🔄 Ejecutando tests del Ejercicio {opcion}...")
            try:
                ejecutar_test_individual(int(opcion))
            except Exception as e:
                print(f"❌ Error ejecutando tests: {e}")
        elif opcion == '6':
            try:
                ejecutar_todos_tests_html()
            except Exception as e:
                print(f"❌ Error generando HTML: {e}")
                print("Intenta con la opción 7 para ejecutar sin HTML")
        elif opcion == '7':
            ejecutar_todos_tests_simple()
        else:
            print("❌ Opción no válida")
        
        if opcion != '0':
            input("\n⏸️  Presiona Enter para continuar...")


def main():
    """Función principal del test runner."""
    parser = argparse.ArgumentParser(
        description='Test Runner para PEC4 - Análisis de Embalses',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python test_runner.py                    # Menú interactivo
  python test_runner.py -e 1               # Ejecutar solo tests del ejercicio 1
  python test_runner.py -e all             # Ejecutar todos los tests
  python test_runner.py -e all --html      # Ejecutar todos con reporte HTML
  python test_runner.py -e all --no-html   # Ejecutar todos sin HTML
        """
    )
    
    parser.add_argument(
        '-e', '--ejercicio',
        choices=['1', '2', '3', '4', '5', 'all'],
        help='Ejercicio a testear (1-5 o all para todos)'
    )
    
    parser.add_argument(
        '--html',
        action='store_true',
        help='Generar reporte HTML (solo con -e all)'
    )
    
    parser.add_argument(
        '--no-html',
        action='store_true',
        help='NO generar reporte HTML (solo con -e all)'
    )
    
    parser.add_argument(
        '-o', '--output',
        default='test_reports',
        help='Directorio para el reporte HTML (default: test_reports)'
    )
    
    args = parser.parse_args()
    
    # Si no hay argumentos, mostrar menú interactivo
    if not args.ejercicio:
        menu_interactivo()
    else:
        if args.ejercicio == 'all':
            if args.no_html:
                ejecutar_todos_tests_simple()
            elif args.html:
                ejecutar_todos_tests_html(args.output)
            else:
                # Por defecto, ejecutar con HTML
                ejecutar_todos_tests_html(args.output)
        else:
            # Ejecutar ejercicio específico
            ejecutar_test_individual(int(args.ejercicio))


if __name__ == '__main__':
    main()



# =======================
# INSTRUCCIONES DE USO
# =======================

"""
INSTRUCCIONES PARA USAR EL SISTEMA DE TESTING:

1. INSTALACIÓN:
   ```bash
   # Instalar dependencias de testing
   pip install -r requirements_test.txt
   ```

2. EJECUTAR TESTS:

   a) Menú interactivo:
      ```bash
      python tests/test_runner.py
      ```

   b) Test específico:
      ```bash
      python tests/test_runner.py -e 1  # Solo ejercicio 1
      python tests/test_runner.py -e 2  # Solo ejercicio 2
      # etc...
      ```

   c) Todos los tests:
      ```bash
      python tests/test_runner.py -e all
      ```

   d) Todos los tests con reporte HTML:
      ```bash
      python tests/test_runner.py -e all --html
      ```

   e) Especificar directorio de salida:
      ```bash
      python tests/test_runner.py -e all --html -o mis_reportes
      ```

3. EJECUTAR TESTS INDIVIDUALES:
   ```bash
   python -m unittest tests.test_ejercicio1
   python -m unittest tests.test_ejercicio2
   # etc...
   ```

4. EJECUTAR CON COVERAGE:
   ```bash
   coverage run -m unittest discover tests
   coverage report
   coverage html  # Genera reporte HTML en htmlcov/
   ```

5. PUNTUACIÓN:
   - Cada ejercicio vale 10 puntos
   - Total: 50 puntos
   - La puntuación se muestra al final de cada test
   - El reporte HTML incluye un resumen completo

6. QUÉ SE EVALÚA:
   - Existencia de archivos
   - Docstrings en módulos y funciones
   - Nombres de variables (mínimo 4 caracteres)
   - Funcionalidad correcta
   - Generación de imágenes
   - Uso de librerías requeridas
   - Formato de salida correcto

7. ESTRUCTURA ESPERADA:
   ```
   proyecto/
   ├── src/
   │   ├── __init__.py
   │   ├── ejercicio1.py
   │   ├── ejercicio2.py
   │   ├── ejercicio3.py
   │   ├── ejercicio4.py
   │   └── ejercicio5.py
   ├── tests/
   │   ├── __init__.py
   │   ├── test_ejercicio1.py
   │   ├── test_ejercicio2.py
   │   ├── test_ejercicio3.py
   │   ├── test_ejercicio4.py
   │   ├── test_ejercicio5.py
   │   └── test_runner.py
   ├── data/
   │   └── [archivo CSV]
   ├── img/
   │   └── [imágenes generadas]
   ├── test_reports/
   │   └── [reportes HTML]
   ├── main.py
   ├── requirements.txt
   └── requirements_test.txt
   ```

NOTAS IMPORTANTES:
- Los tests verifican la funcionalidad completa de cada ejercicio
- Se incluyen tests de integración para verificar el flujo completo
- El sistema de puntuación es automático y objetivo
- Los reportes HTML proporcionan información detallada de cada test
"""