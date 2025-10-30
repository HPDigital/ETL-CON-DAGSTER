from __future__ import annotations

from pathlib import Path
import pandas as pd


DEFAULT_OUTPUT = Path("data/Tarea.csv")


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def save_csv(df: pd.DataFrame, output_path: Path | str = DEFAULT_OUTPUT) -> Path:
    path = Path(output_path)
    ensure_parent(path)
    df.to_csv(path, index=False, encoding="utf-8")
    return path

