"""
Setup.py para PEC4 - Análisis de Embalses de Catalunya

Este archivo permite instalar el proyecto y sus dependencias de forma automática.
Se recomienda usar dentro de un entorno virtual.

Instrucciones:
1. Crear entorno virtual: python -m venv venv
2. Activar entorno: source venv/bin/activate (Windows: venv\Scripts\activate)
3. Instalar: python setup.py install
"""

from setuptools import setup, find_packages
import os
import sys

# Verificar versión de Python
if sys.version_info < (3, 11):
    print("ERROR: Este proyecto requiere Python 3.11 o superior.")
    print(f"Tu versión actual es Python {sys.version_info.major}.{sys.version_info.minor}")
    sys.exit(1)

# Leer el contenido del README
try:
    with open('README.md', 'r', encoding='utf-8') as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = "PEC4 - Análisis de Embalses de Catalunya"

# Leer las dependencias del requirements.txt
try:
    with open('requirements.txt', 'r', encoding='utf-8') as fh:
        requirements = [line.strip() for line in fh if line.strip() and not line.startswith('#')]
except FileNotFoundError:
    print("ADVERTENCIA: No se encontró requirements.txt")
    requirements = ['pandas', 'matplotlib', 'scipy', 'numpy']

# Separar dependencias principales de las de testing
main_requirements = []
test_requirements = []

for req in requirements:
    req_lower = req.lower()
    if any(test_pkg in req_lower for test_pkg in ['unittest', 'coverage', 'pytest', 'html-testrunner']):
        test_requirements.append(req)
    else:
        main_requirements.append(req)

# Función para crear directorios necesarios
def create_project_directories():
    """Crear directorios necesarios para el proyecto."""
    directories = ['img', 'test_reports', 'doc', 'data']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✓ Directorio '{directory}' creado")

setup(
    name='pec4-embalses-catalunya',
    version='1.0.0',
    author='Samuel Viciana',
    author_email='',
    description='Análisis de datos de embalses de Catalunya - PEC4 UOC',
    long_description=long_description,
    long_description_content_type='text/markdown',
    
    # Paquetes a incluir
    packages=find_packages(include=['src', 'src.*', 'tests', 'tests.*']),
    
    # Archivos de datos a incluir
    package_data={
        '': ['*.txt', '*.md', '*.csv', '*.json'],
        'data': ['*.csv'],
        'img': ['*.png', '*.jpg'],
    },
    
    # Incluir archivos adicionales
    include_package_data=True,
    
    # Script principal
    entry_points={
        'console_scripts': [
            'pec4-embalses=main:main',
        ],
    },
    
    # Dependencias principales
    install_requires=main_requirements,
    
    # Dependencias opcionales para desarrollo y testing
    extras_require={
        'dev': test_requirements + ['pylint'],
        'test': test_requirements,
        'docs': ['sphinx', 'sphinx-rtd-theme'],
    },
    
    # Clasificadores
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Education',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Operating System :: OS Independent',
    ],
    
    # Versión mínima de Python
    python_requires='>=3.11',
    
    # Metadatos adicionales
    keywords='data-analysis water-reservoirs catalunya drought pandas visualization',
)

# Si se ejecuta directamente, mostrar información de instalación
if __name__ == '__main__':
    print("\n" + "="*60)
    print("INSTALACIÓN DE PEC4 - ANÁLISIS DE EMBALSES")
    print("="*60)
    
    # Verificar si estamos en un entorno virtual
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    
    if not in_venv:
        print("\n⚠️  ADVERTENCIA: No estás en un entorno virtual.")
        print("Se recomienda crear uno antes de instalar:")
        print("\n  python -m venv venv")
        print("  source venv/bin/activate  # En Windows: venv\\Scripts\\activate")
        print("\n¿Deseas continuar sin entorno virtual? (no recomendado)")
        respuesta = input("Continuar? (s/N): ").strip().lower()
        if respuesta != 's':
            print("\nInstalación cancelada.")
            print("Crea un entorno virtual y vuelve a ejecutar setup.py")
            sys.exit(0)
    
    print("\nEste script instalará el proyecto y todas sus dependencias.")
    print("\nOpciones de instalación:")
    print("  python setup.py install        # Instalación estándar")
    print("  pip install -e .               # Instalación en modo desarrollo")
    print("  pip install -e .[test]         # Con herramientas de testing")
    print("  pip install -e .[dev]          # Con todas las herramientas de desarrollo")
    
    # Crear directorios si se está instalando
    if len(sys.argv) > 1 and sys.argv[1] in ['install', 'develop']:
        print("\nCreando directorios del proyecto...")
        create_project_directories()
    
    print("\n" + "="*60)