"""Per-subject scoring, run automatically right after a session finishes.

This reuses the same scoring logic as the batch analysis scripts in
processar_dados/read_trials_Abstract_two.py and read_trials_Abstract_six.py
(mean RT of correct responses, counts of correct/incorrect/anticipatory/
omitted trials), but for the single subject that just completed a run, and
generalized to any N_SHAPES (those scripts hardcode 2 vs 6 separately) and
to whatever interstimulus value the settings screen was given (those
scripts assume a fixed 500 ms).
"""
import csv
import tkinter as tk
from tkinter import filedialog

import numpy as np
import pandas as pd

TIME_TO_RESPONSE_ANTICIPATORY = 200  # ms; below this, a "response" is discarded as anticipatory


def summarize_subject(session):
    half = session.n_shapes // 2
    stimulus_A = set(range(1, half + 1))              # shapes mapped to the left key
    stimulus_B = set(range(half + 1, session.n_shapes + 1))  # shapes mapped to the right key
    correct_A, correct_B = 0, 1                        # 0 = left key, 1 = right key

    time_for_stimulus = session.interstimulus
    skip_samples = session.interstimulus // 5           # samples are recorded every 5 ms

    anticipatory, correct_responses, errada_responses = [], [], []

    for i in range(session.n_trials):
        path = session.trials_dir / f"SUJ{session.suj}_trial{i}.csv"
        df = np.array(pd.read_csv(str(path), sep=',', header=0))
        time = df[:, 0]
        key_press = df[:, 1]
        stim = df[0, 2]

        for k in range(len(key_press) - skip_samples):
            if key_press[k + skip_samples] in (0, 1):
                rt = time[k + skip_samples] - time_for_stimulus
                if rt > TIME_TO_RESPONSE_ANTICIPATORY:
                    if stim in stimulus_A:
                        bucket = correct_responses if key_press[k + skip_samples] == correct_A else errada_responses
                    else:
                        bucket = correct_responses if key_press[k + skip_samples] == correct_B else errada_responses
                    bucket.append(rt)
                else:
                    anticipatory.append(rt)
                break

    n_corretas = len(correct_responses)
    n_erradas = len(errada_responses)
    n_antecipadas = len(anticipatory)
    n_omissas = session.n_trials - (n_corretas + n_erradas + n_antecipadas)
    resp_corretas = float(np.mean(correct_responses)) if correct_responses else float("nan")

    return {
        "cod_suj": session.suj,
        "resp_corretas": resp_corretas,
        "n_corretas": n_corretas,
        "n_erradas": n_erradas,
        "n_antecipadas": n_antecipadas,
        "n_omissas": n_omissas,
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
