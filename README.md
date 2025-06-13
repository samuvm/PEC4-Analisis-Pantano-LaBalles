# PEC4 - Análisis de Embalses de Catalunya 💧

Proyecto de análisis de datos de los embalses de las Cuencas Internas de Catalunya, desarrollado como parte de la asignatura **22.403 · Programación para la ciencia de datos** de la Universitat Oberta de Catalunya (UOC).

## 📋 Descripción

Este proyecto analiza la evolución del volumen de agua en el embalse de La Baells, identificando períodos de sequía mediante técnicas de procesamiento de señales. El análisis incluye 5 ejercicios progresivos:

1. **Carga y exploración inicial de datos**
2. **Limpieza y filtrado de datos**
3. **Análisis temporal y visualización**
4. **Suavizado de señales y análisis de tendencias**
5. **Identificación de períodos de sequía**

## 📁 Estructura del Proyecto

```
PEC4/
├── data/               # Datos de los embalses (CSV)
├── src/                # Código fuente de los ejercicios
│   ├── ejercicio1.py   # Carga y EDA
│   ├── ejercicio2.py   # Limpieza y filtrado
│   ├── ejercicio3.py   # Análisis temporal
│   ├── ejercicio4.py   # Suavizado de señales
│   └── ejercicio5.py   # Detección de sequías
├── img/                # Imágenes generadas
├── tests/              # Tests unitarios
│   └── test_runner.py  # Ejecutor principal de tests
├── test_reports/       # Reportes HTML de tests
├── main.py            # Punto de entrada principal
├── setup.py           # Instalador del proyecto
├── requirements.txt   # Dependencias
├── LICENSE            # Licencia MIT
└── README.md          # Este archivo
```

## 🚀 Instalación

### Requisitos
- Python 3.11 o superior

### Opción 1: Instalación con setup.py (Recomendado)
```bash
# Clonar o descargar el proyecto
cd PEC4/

# Instalar con setup.py
python setup.py install
```

### Opción 2: Instalación manual
```bash
# Crear entorno virtual (recomendado)
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

## 💻 Uso

### Ejecutar todos los ejercicios
```bash
python main.py
```

### Ejecutar ejercicios individuales
```bash
python main.py -e 1  # Solo ejercicio 1
python main.py -e 3  # Ejercicios 1 al 3
```

### Ayuda
```bash
python main.py -h
```

## 🧪 Tests

Para ejecutar los tests, navega a la carpeta tests y ejecuta:

```bash
cd tests/
python test_runner.py
```

Se mostrará un menú interactivo con opciones:
- Opción 1-5: Tests individuales por ejercicio
- **Opción 6**: Ejecutar todos los tests con reporte HTML
- Opción 7: Ejecutar todos los tests sin HTML

El reporte HTML se guardará en `test_reports/PEC4_TestReport.html`

## 📊 Datos

Los datos provienen del portal de transparencia de Catalunya:
- **Fuente**: [Quantitat d'aigua als embassaments](https://analisi.transparenciacatalunya.cat/)
- **Formato**: CSV
- **Ubicación**: carpeta `data/`

## 📝 Licencia

Este proyecto está bajo licencia MIT. Ver archivo [LICENSE](LICENSE) para más detalles.

## 👤 Autor

**Samuel Viciana**  
Universitat Oberta de Catalunya (UOC)  
Grado en Ciencia de Datos Aplicada