from __future__ import annotations

import time
from typing import Optional

import pandas as pd
import requests


def geocode_name_country(name: str, country: str, timeout: int = 15) -> Optional[tuple[float, float]]:
    """Geocodifica nombre y pais usando maps.co."""
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; ETL-Lagos/1.0; +https://github.com/)"
    }
    query = f"{name}, {country}"
    url = f"https://geocode.maps.co/search?q={requests.utils.quote(query)}"
    try:
        resp = requests.get(url, headers=headers, timeout=timeout)
        resp.raise_for_status()
        data = resp.json()
        if not data:
            return None
        lat = float(data[0].get("lat"))
        lon = float(data[0].get("lon"))
        return lat, lon
    except Exception:
        return None


def geocode_dataframe(df: pd.DataFrame, delay_sec: float = 1.0) -> pd.DataFrame:
    """Agrega columnas de latitud y longitud al DataFrame."""
    lats: list[Optional[float]] = []
    lons: list[Optional[float]] = []

    for _, row in df.iterrows():
        name = str(row.get("Nombre", ""))
        country = str(row.get("Pais", ""))

        coords = geocode_name_country(name, country)
        if coords is None:
            time.sleep(delay_sec)
            coords = geocode_name_country(name, country)

        if coords is None:
            lats.append(None)
            lons.append(None)
        else:
            lat, lon = coords
            lats.append(lat)
            lons.append(lon)

        time.sleep(delay_sec)

    result = df.copy()
    result["Latitud"] = lats
    result["Longitud"] = lons
    return result
