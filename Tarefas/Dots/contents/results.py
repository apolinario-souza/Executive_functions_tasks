"""Per-subject scoring, run automatically right after a session finishes.
The measures follow Davidson, Amso, Anderson & Diamond (2006) — see contents/scoring.py and
the README for what each column means."""
import csv
import json
import tkinter as tk
from tkinter import filedialog

from .scoring import score_trials, summarize

# stimulus_A/B says which key is correct for a stimulus shown on the right (3,4)
# vs left (1,2) side; is_congruent says which of those trials count as congruent.
_CONDITION_RULES = {
    "congruent": dict(stimulus_A=(3, 4), stimulus_B=(1, 2), correct_A=1, correct_B=0,
                       is_congruent=lambda stim: True),
    "incongruent": dict(stimulus_A=(3, 4), stimulus_B=(1, 2), correct_A=0, correct_B=1,
                         is_congruent=lambda stim: False),
    "mixed": dict(stimulus_A=(1, 4), stimulus_B=(2, 3), correct_A=0, correct_B=1,
                   is_congruent=lambda stim: stim in (1, 3)),
}


def summarize_subject(session):
    rules = _CONDITION_RULES[session.condition]

    def rule(stim):
        correct = rules["correct_A"] if stim in rules["stimulus_A"] else rules["correct_B"]
        return correct, rules["is_congruent"](stim)

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
