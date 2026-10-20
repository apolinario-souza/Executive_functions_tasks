"""Per-subject scoring, run automatically right after a session finishes.

Reuses the same scoring logic as the batch analysis scripts
processar_dados/read_trials_Dots_{cong,inc,mixed}.py (correct/incorrect/
anticipatory/omitted counts, congruent vs incongruent RT, switch-cost RT),
but for the single subject that just completed a run, and parametrized by
this session's own interstimulus/n_trials instead of the hardcoded 500 ms
/ 20 trials those batch scripts assume.

Per condition (from those scripts):
- congruent:   stimulus is always congruent (striped dots, respond same side)
- incongruent: stimulus is always incongruent (solid dots, respond opposite side)
- mixed:       stim 1/3 (striped) are congruent, 2/4 (solid) are incongruent
"""
import csv
import json
import tkinter as tk
from tkinter import filedialog

import numpy as np
import pandas as pd

TIME_TO_RESPONSE_ANTICIPATORY = 200  # ms; below this, a "response" is discarded as anticipatory

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


def _safe_mean(values):
    return float(np.mean(values)) if values else float("nan")


def _switch_costs(trial_indices, rts):
    """Given the trial indices (in original sequence order) and RTs of
    correct responses within one congruency condition, splits RTs into
    'switch' (previous same-condition trial wasn't immediately before) and
    'no switch' (it was)."""
    switch_cost, no_switch_cost = [], []
    for i in range(len(trial_indices) - 1):
        if abs(trial_indices[i] - trial_indices[i + 1]) == 1:
            no_switch_cost.append(rts[i + 1])
        else:
            switch_cost.append(rts[i + 1])
    return switch_cost, no_switch_cost


def summarize_subject(session):
    rules = _CONDITION_RULES[session.condition]
    stimulus_A, stimulus_B = rules["stimulus_A"], rules["stimulus_B"]
    correct_A, correct_B = rules["correct_A"], rules["correct_B"]
    is_congruent = rules["is_congruent"]

    time_for_stimulus = session.interstimulus
    skip_samples = session.interstimulus // 5  # samples are recorded every 5 ms

    anticipatory, correct_responses, errada_responses = [], [], []
    rt_cong, rt_unc, rt_cong_inc, rt_unc_inc = [], [], [], []
    index_cong, index_unc = [], []

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
                    congruent = is_congruent(stim)
                    correct = (key_press[k + skip_samples] == correct_A if stim in stimulus_A
                               else key_press[k + skip_samples] == correct_B)
                    if correct:
                        correct_responses.append(rt)
                        if congruent:
                            index_cong.append(i)
                            rt_cong.append(rt)
                        else:
                            index_unc.append(i)
                            rt_unc.append(rt)
                    else:
                        errada_responses.append(rt)
                        if congruent:
                            rt_cong_inc.append(rt)
                        else:
                            rt_unc_inc.append(rt)
                else:
                    anticipatory.append(rt)
                break

    switch_cost_cong, no_switch_cost_cong = _switch_costs(index_cong, rt_cong)
    switch_cost_unc, no_switch_cost_unc = _switch_costs(index_unc, rt_unc)

    n_corretas = len(correct_responses)
    n_erradas = len(errada_responses)
    n_antecipadas = len(anticipatory)
    n_omissas = session.n_trials - (n_corretas + n_erradas + n_antecipadas)

    return {
        "cod_suj": session.suj,
        "resp_corretas": _safe_mean(correct_responses),
        "n_corretas": n_corretas,
        "n_erradas": n_erradas,
        "n_antecipadas": n_antecipadas,
        "n_omissas": n_omissas,
        "congruente": _safe_mean(rt_cong),
        "incogruente": _safe_mean(rt_unc),
        "n_congruente": len(rt_cong),
        "n_incogruente": len(rt_unc),
        "com_mudanca_cong": _safe_mean(switch_cost_cong),
        "sem_mudanca_cong": _safe_mean(no_switch_cost_cong),
        "com_mudanca_inc": _safe_mean(switch_cost_unc),
        "sem_mudanca_inc": _safe_mean(no_switch_cost_unc),
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
