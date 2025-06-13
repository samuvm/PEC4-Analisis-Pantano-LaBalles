"""
Setup.py para PEC4 - Análisis de Embalses de Catalunya

Este archivo permite instalar el proyecto y sus dependencias
de forma automática usando pip o python setup.py install
"""

from setuptools import setup, find_packages
import os

# Leer el contenido del README
with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

# Leer las dependencias del requirements.txt
with open('requirements.txt', 'r', encoding='utf-8') as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith('#')]

# Separar dependencias principales de las de testing
main_requirements = []
test_requirements = []

for req in requirements:
    req_lower = req.lower()
    if any(test_pkg in req_lower for test_pkg in ['unittest', 'coverage', 'pytest', 'html-testrunner']):
        test_requirements.append(req)
    else:
        main_requirements.append(req)

setup(
    name='pec4-embalses-catalunya',
    version='1.0.0',
    author='Samuel Viciana',
    author_email='',
    description='Análisis de datos de embalses de Catalunya - PEC4 UOC',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/usuario/pec4-embalses',  # Actualizar si tienes repositorio
    
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
    project_urls={
        'Documentation': 'https://github.com/usuario/pec4-embalses/wiki',
        'Source': 'https://github.com/usuario/pec4-embalses',
        'Bug Reports': 'https://github.com/usuario/pec4-embalses/issues',
    },
)

# Crear directorios necesarios si no existen
def post_install():
    """Crear directorios necesarios después de la instalación."""
    directories = ['img', 'test_reports', 'doc']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✓ Directorio '{directory}' creado")

# Si se ejecuta directamente, mostrar información
if __name__ == '__main__':
    print("\n" + "="*60)
    print("INSTALACIÓN DE PEC4 - ANÁLISIS DE EMBALSES")
    print("="*60)
    print("\nEste script instalará el proyecto y todas sus dependencias.")
    print("\nPara instalar, ejecuta:")
    print("  python setup.py install")
    print("\nPara desarrollo (incluye herramientas de testing):")
    print("  pip install -e .[dev]")
    print("\nPara solo testing:")
    print("  pip install -e .[test]")
    print("\n" + "="*60)