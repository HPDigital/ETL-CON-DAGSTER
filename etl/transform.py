from __future__ import annotations

import re
import unicodedata
import pandas as pd
from bs4 import BeautifulSoup


def _normalize_text(text: str) -> str:
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join(c for c in nfkd if not unicodedata.combining(c)).lower()


def extract_name_and_country(soup: BeautifulSoup) -> pd.DataFrame:
    """Extrae nombre y pais desde etiquetas h2/span."""
    rows = []
    for h2 in soup.find_all("h2"):
        span = h2.find("span")
        if not span:
            continue
        text = span.get_text(strip=True)
        if "," not in text:
            continue
        nombre, pais = [part.strip() for part in text.split(",", 1)]
        rows.append({"Nombre": nombre, "Pais": pais})

    if len(rows) > 8:
        rows = rows[:8]

    return pd.DataFrame(rows)


def extract_surface_area(soup: BeautifulSoup, df: pd.DataFrame) -> pd.DataFrame:
    """Busca superficies en km2 y las agrega al DataFrame."""
    texts = [b.get_text(" ", strip=True) for b in soup.find_all("b")]
    normalized_text = " \n ".join(_normalize_text(t) for t in texts)

    pattern = re.compile(r"(\d[\d\.]*)\s*(?:km2|km\^?2|kilometros?)")
    matches = pattern.findall(normalized_text)

    surfaces = [int(m.replace(".", "")) for m in matches]

    if len(surfaces) < len(df):
        surfaces += [None] * (len(df) - len(surfaces))
    elif len(surfaces) > len(df):
        surfaces = surfaces[: len(df)]

    df = df.copy()
    df["Superficie"] = surfaces
    return df

