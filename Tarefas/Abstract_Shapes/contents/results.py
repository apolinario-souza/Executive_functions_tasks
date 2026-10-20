"""Per-subject scoring, run automatically right after a session finishes.
The measures follow Davidson, Amso, Anderson & Diamond (2006) — see contents/scoring.py and
the README for what each column means. Shapes appear at the center, so
there are no congruent/incongruent trials here."""
import csv
import json
import tkinter as tk
from tkinter import filedialog

from .scoring import score_trials, summarize


def summarize_subject(session):
    half = session.n_shapes // 2
    left_shapes = set(range(1, half + 1))  # the other half is answered with the right key

    def rule(stim):
        return (0 if stim in left_shapes else 1), None

    trials = score_trials(session.trials_dir, session.suj, session.n_trials, session.interstimulus, rule)
    return summarize(trials, {"cod_suj": session.suj, "n_formas": session.n_shapes})


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
