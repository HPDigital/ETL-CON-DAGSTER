# Lagos de Sudamérica ETL Pipeline

Este proyecto implementa un pipeline ETL (Extract, Transform, Load) utilizando Dagster para recopilar y procesar información sobre los lagos más grandes de Sudamérica.

## 🌟 Características

- Web scraping de datos de lagos sudamericanos
- Extracción de nombres, países y superficies
- Geocodificación automática de ubicaciones
- Exportación de datos a CSV
- Pipeline orquestado con Dagster

## 🛠️ Requisitos Previos

- Python 3.8+
- pip (gestor de paquetes de Python)
- Conexión a Internet para web scraping y geocodificación

## 🚀 Instalación

1. Clonar el repositorio

2. Crear y activar un entorno virtual

3. Instalar dependencias

```
pip install -r requirements.txt
```

## 💻 Uso

1. Iniciar el servidor Dagster:
```bash
dagster dev
```

2. Abrir el navegador en `http://localhost:3000`

3. Ejecutar el pipeline desde la interfaz de Dagster

## 📊 Assets de Dagster

El pipeline incluye los siguientes assets:

- `fetch_webpage`: Obtiene la página web con información de lagos
- `extract_name_and_country`: Extrae nombres y países de los lagos
- `extract_surface_area`: Obtiene la superficie de cada lago
- `extract_coordinates`: Geocodifica la ubicación de cada lago
- `save_to_csv`: Guarda los datos procesados en un archivo CSV

## 📁 Estructura de Datos

El dataset final incluye:
- Nombre del lago
- País
- Superficie (km²)
- Latitud
- Longitud

## 🔧 Configuración

El archivo de salida CSV se guarda por defecto en:
```
C:/Users/HP/Desktop/DIPLOMADO MACHINE LEARNING/Modulo 1/DATOS_CSV/Tarea.csv
```

Para modificar la ruta, actualizar la constante `OUTPUT_PATH` en `ETL_DAGSTER.py`.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue primero para discutir los cambios que te gustaría hacer.

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 📞 Contacto

[Tu Nombre] - [tu@email.com]

Link del proyecto: https://github.com/[tu-usuario]/lagos-sudamerica-etl