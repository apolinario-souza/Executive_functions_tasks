"""Per-subject scoring, run automatically right after a session finishes.
The measures follow Davidson, Amso, Anderson & Diamond (2006) — see contents/scoring.py and
the README for what each column means."""
import csv
import json
import tkinter as tk
from tkinter import filedialog

from .scoring import score_trials, summarize

# Stimulus 1/3 = straight arrow (left/right side); 2/4 = diagonal arrow (left/right side).
# stimulus_A/B says which key is correct; condition_cong says which stimuli are congruent.
STIMULUS_A = (2, 3)
STIMULUS_B = (1, 4)
CORRECT_A, CORRECT_B = 1, 0
CONDITION_CONG = (1, 3)


def _rule(stim):
    return (CORRECT_A if stim in STIMULUS_A else CORRECT_B), stim in CONDITION_CONG


def summarize_subject(session):
    trials = score_trials(session.trials_dir, session.suj, session.n_trials, session.interstimulus, _rule)
    return summarize(trials, {"cod_suj": session.suj})


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
