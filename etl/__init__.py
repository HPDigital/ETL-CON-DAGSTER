"""Paquete ETL modular para scraping, transformacion, geocodificacion y persistencia."""

from .pipeline import run_etl

__all__ = ["run_etl"]
