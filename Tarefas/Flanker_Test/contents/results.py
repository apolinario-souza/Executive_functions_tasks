"""Per-subject scoring, run automatically right after a session finishes.
Same measures as the other tasks (see contents/scoring.py and the
README); Flanker is not in Davidson et al. (2006), so here "congruent"
means all fish pointing the same way."""
import csv
import json
import tkinter as tk
from tkinter import filedialog

from .scoring import score_trials, summarize
from .session import stimulus_parts, correct_key, is_congruent


def summarize_subject(session):
    def rule(stim):
        _, local = stimulus_parts(session.condition, stim)
        return correct_key(local), is_congruent(local)

    trials = score_trials(session.trials_dir, session.suj, session.n_trials, session.interstimulus, rule)
    return summarize(trials, {"cod_suj": session.suj, "condicao": session.condition})


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
