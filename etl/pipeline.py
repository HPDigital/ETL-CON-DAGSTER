from __future__ import annotations

from pathlib import Path
import pandas as pd

from .scraper import fetch_webpage, DEFAULT_URL
from .transform import extract_name_and_country, extract_surface_area
from .geocode import geocode_dataframe
from .io_utils import save_csv, DEFAULT_OUTPUT


def run_etl(url: str = DEFAULT_URL, output: Path | str = DEFAULT_OUTPUT) -> tuple[pd.DataFrame, Path]:
    soup = fetch_webpage(url)
    df = extract_name_and_country(soup)
    df = extract_surface_area(soup, df)
    df = geocode_dataframe(df)
    out_path = save_csv(df, output)
    return df, out_path


try:
    from dagster import asset, Definitions

    @asset
    def fetch_webpage_asset():
        return fetch_webpage(DEFAULT_URL)

    @asset
    def extract_name_country_asset(fetch_webpage_asset):
        return extract_name_and_country(fetch_webpage_asset)

    @asset
    def extract_surface_asset(fetch_webpage_asset, extract_name_country_asset):
        return extract_surface_area(fetch_webpage_asset, extract_name_country_asset)

    @asset
    def geocode_asset(extract_surface_asset):
        return geocode_dataframe(extract_surface_asset)

    @asset
    def save_csv_asset(geocode_asset):
        df = geocode_asset
        save_csv(df, DEFAULT_OUTPUT)
        return df

    DAGSTER_ASSETS = [
        fetch_webpage_asset,
        extract_name_country_asset,
        extract_surface_asset,
        geocode_asset,
        save_csv_asset,
    ]
    defs = Definitions(assets=DAGSTER_ASSETS)
except Exception:
    DAGSTER_ASSETS = []
    defs = None


if __name__ == "__main__":
    dataframe, output_path = run_etl()
    print(f"Datos exportados a {output_path}")
    print(dataframe)
