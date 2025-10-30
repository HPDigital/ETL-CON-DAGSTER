# ETL CON DAGTER Y TEKINTER

Pipeline ETL para obtener informacion de los lagos mas grandes de Sudamerica.
Incluye scraping, transformaciones y geocodificacion, con ejecucion desde Dagster
o mediante una interfaz grafica basada en Tkinter.

## Caracteristicas principales
- Extraccion de datos desde https://www.howlanders.com.
- Limpieza y normalizacion de nombres, paises y superficies en km2.
- Geocodificacion automatica (maps.co) para obtener latitud y longitud.
- Exportacion a CSV en `data/Tarea.csv` (ruta personalizable).
- Assets reutilizables para Dagster y una interfaz grafica simple.

## Requisitos
- Python 3.10 o superior.
- `pip install -r requirements.txt` para dependencias de scraping/ETL y Dagster.
- Acceso a internet para el scraping y la geocodificacion.

## Uso rapido del ETL desde Tkinter
1. Crear entorno virtual (opcional) e instalar dependencias.
2. Ejecutar la aplicacion grafica:
   ```bash
   python app.py
   ```
3. Presionar **Ejecutar ETL**. El resultado se muestra en pantalla y se guarda en el CSV.

## Ejecucion desde linea de comandos
```bash
python -m etl.pipeline
```

## Ejecucion con Dagster
1. Iniciar el servidor:
   ```bash
   dagster dev -m etl_dagster
   ```
2. Abrir `http://localhost:3000` y ejecutar la asset `save_csv_asset`.

## Estructura del proyecto
- `etl/` componentes modulares: scraper, transformaciones, geocodificacion y utilidades.
- `etl/pipeline.py` orquesta el flujo y declara assets para Dagster.
- `etl_dagster.py` expone `defs` para Dagster.
- `app.py` interfaz Tkinter.
- `data/` carpeta de salida para CSV (creada automaticamente).

## Notas
- La API gratuita de maps.co puede imponer limites. En ese caso aparecera latitud/longitud nula para ese registro.
- Tkinter viene incluido con las distribuciones estandar de Python en Windows y macOS. En Linux puede requerir `python3-tk`.

