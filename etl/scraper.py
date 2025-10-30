from __future__ import annotations

import requests
from bs4 import BeautifulSoup


DEFAULT_URL = "https://www.howlanders.com/blog/latam/lagos-mas-grandes-de-sudamerica/amp/"


def fetch_webpage(url: str = DEFAULT_URL, timeout: int = 20) -> BeautifulSoup:
    """Descarga la pagina y devuelve un objeto BeautifulSoup listo para parsing."""
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; ETL-Lagos/1.0; +https://github.com/)"
    }
    resp = requests.get(url, headers=headers, timeout=timeout)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "html.parser")

