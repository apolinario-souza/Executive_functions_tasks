"""Per-subject scoring, run automatically right after a session finishes:
the number 6 is the "go" trial (press Space), every other number is
"no-go" (don't press)."""
import csv
import json
import tkinter as tk
from tkinter import filedialog

import pandas as pd

from .constants import BASE_DIR
from .trials import COLUMNS


def save_trials(session, data):
    """Trial-by-trial spreadsheet, next to main.py (same file as before:
    <subject>_resultados.xlsx)."""
    df = pd.DataFrame(data, columns=COLUMNS)
    df.to_excel(str(BASE_DIR / f"{session.suj}_resultados.xlsx"), index=False, engine="openpyxl")


def summarize_subject(session, data):
    go = [row for row in data if row[1] == "6"]
    no_go = [row for row in data if row[1] != "6"]
    rts = [row[4] * 1000 for row in go if row[2] == "Sim"]
    return {
        "cod_suj": session.suj,
        "n_tentativas": len(data),
        "n_go": len(go),
        "acertos_go": sum(row[2] == "Sim" for row in go),
        "omissoes_go": sum(row[2] == "Não" for row in go),
        "falsos_alarmes": sum(row[2] == "Sim" for row in no_go),
        "rejeicoes_corretas": sum(row[2] == "Não" for row in no_go),
        "tr_medio_go": sum(rts) / len(rts) if rts else float("nan"),
    }


def save_summary_dialog(summary, default_name):
    """Opens a native 'Save As' window so the experimenter picks where to
    save the processed summary. Returns the chosen path, or None if the
    dialog was cancelled."""
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    path = filedialog.asksaveasfilename(
        title="Salvar dados processados",
        defaultextension=".csv",
        initialfile=default_name,
        filetypes=[("CSV", "*.csv")],
    )
    root.destroy()

    if not path:
        return None

    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(summary.keys())
        writer.writerow(summary.values())
    return path


def save_summary_file(summary, path):
    """Writes the summary as JSON for the battery's guided mode, which
    collects every task of the session into one spreadsheet."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(summary, f, default=float)
