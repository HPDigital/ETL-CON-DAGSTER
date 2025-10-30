from __future__ import annotations

import threading
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path

import pandas as pd

from etl.io_utils import DEFAULT_OUTPUT
from etl.pipeline import run_etl


class LakesETLApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Lagos de Sudamerica - ETL")
        self.geometry("950x600")
        self.minsize(760, 480)

        self.output_path = tk.StringVar(value=str(DEFAULT_OUTPUT))
        self.status_var = tk.StringVar(value="Listo")

        self._build_layout()

    def _build_layout(self) -> None:
        top_frame = ttk.Frame(self, padding=10)
        top_frame.pack(fill=tk.X)

        ttk.Label(top_frame, text="Archivo CSV de salida:").pack(anchor=tk.W)
        path_frame = ttk.Frame(top_frame)
        path_frame.pack(fill=tk.X, pady=(4, 8))

        path_entry = ttk.Entry(path_frame, textvariable=self.output_path)
        path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        ttk.Button(path_frame, text="Examinar", command=self._choose_output).pack(
            side=tk.LEFT, padx=(8, 0)
        )

        self.run_button = ttk.Button(
            top_frame,
            text="Ejecutar ETL",
            command=self._run_pipeline,
        )
        self.run_button.pack(pady=(0, 8))

        self.status_label = ttk.Label(top_frame, textvariable=self.status_var)
        self.status_label.pack(anchor=tk.W)

        columns = ("Nombre", "Pais", "Superficie", "Latitud", "Longitud")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            width = 180 if col in ("Nombre", "Pais") else 110
            self.tree.column(col, width=width, anchor=tk.CENTER)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.place(relx=0.97, rely=0.2, relheight=0.7)

    def _choose_output(self) -> None:
        initial = Path(self.output_path.get()).resolve()
        file_path = filedialog.asksaveasfilename(
            initialdir=initial.parent,
            initialfile=initial.name,
            defaultextension=".csv",
            filetypes=[("CSV", "*.csv"), ("Todos", "*.*")],
        )
        if file_path:
            self.output_path.set(file_path)

    def _run_pipeline(self) -> None:
        self._set_running_state(True)
        self.status_var.set("Ejecutando pipeline...")
        thread = threading.Thread(target=self._run_pipeline_thread, daemon=True)
        thread.start()

    def _run_pipeline_thread(self) -> None:
        try:
            path = Path(self.output_path.get())
            df, out_path = run_etl(output=path)
            self.after(0, lambda: self._on_pipeline_success(df, out_path))
        except Exception as exc:
            self.after(0, lambda: self._on_pipeline_error(exc))

    def _on_pipeline_success(self, df: pd.DataFrame, out_path: Path) -> None:
        self._populate_tree(df)
        self.status_var.set(f"Completado. Archivo guardado en {out_path}")
        self._set_running_state(False)

    def _on_pipeline_error(self, exc: Exception) -> None:
        self.status_var.set("Error al ejecutar el pipeline")
        messagebox.showerror("Error", f"No se pudo ejecutar el ETL: {exc}")
        self._set_running_state(False)

    def _populate_tree(self, df: pd.DataFrame) -> None:
        self.tree.delete(*self.tree.get_children())
        if df.empty:
            return
        for _, row in df.iterrows():
            self.tree.insert(
                "",
                tk.END,
                values=(
                    row.get("Nombre", ""),
                    row.get("Pais", ""),
                    row.get("Superficie", ""),
                    row.get("Latitud", ""),
                    row.get("Longitud", ""),
                ),
            )

    def _set_running_state(self, running: bool) -> None:
        state = tk.DISABLED if running else tk.NORMAL
        self.run_button.configure(state=state)


def main() -> None:
    app = LakesETLApp()
    app.mainloop()


if __name__ == "__main__":
    main()
