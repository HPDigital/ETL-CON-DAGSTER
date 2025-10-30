"""Integracion con Dagster para el pipeline de lagos sudamericanos."""

from __future__ import annotations

from etl.pipeline import DAGSTER_ASSETS, defs


if defs is None:
    raise ImportError(
        "Dagster no esta disponible. Instala dagster y dagster-webserver para usar estas assets."
    )


__all__ = ["defs", "DAGSTER_ASSETS"]

