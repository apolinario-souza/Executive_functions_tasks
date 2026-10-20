"""Per-subject scoring — the same file in every task's contents/ folder
(Arrows, Dots, Abstract_Shapes, Pictures, Flanker_Test).

Follows Davidson, Amso, Anderson & Diamond (2006), Neuropsychologia 44,
2037-2078:
  - a trial's response is the first key pressed after the stimulus
    appears; one within 200 ms of it is anticipatory;
  - % correct = correct / (correct + incorrect): anticipatory responses
    and omissions are left out;
  - RT = median of the correct responses (the mean is also reported);
  - % anticipatory = anticipatory / all trials;
  - a "switch" trial is one whose type (congruent/incongruent) differs
    from the previous trial's, taken from the sequence that was shown,
    whether or not the previous answer was right.
The README explains every output column."""
import numpy as np
import pandas as pd

ANTICIPATORY_MS = 200

# Columns of each group of trials: all of them get the full set; the
# congruent/incongruent groups and the switch groups get fewer, to keep
# the spreadsheet readable
FULL = ("n_tentativas", "n_corretas", "n_erradas", "n_antecipadas", "n_omissas",
        "pct_corretas", "pct_antecipadas", "tr_mediana", "tr_media")
BY_TYPE = ("n_tentativas", "pct_corretas", "pct_antecipadas", "tr_mediana", "tr_media")
BY_CONTEXT = ("n_tentativas", "pct_corretas", "tr_mediana")

NAN = float("nan")


def read_trial(path, interstimulus):
    """(stimulus, first key after stimulus onset, its RT in ms). Key and
    RT are None when nothing was pressed. The Time column is real ms since
    the trial began; the stimulus appears on the first sample at or after
    `interstimulus`."""
    df = np.array(pd.read_csv(str(path), sep=',', header=0))
    time, keys, stim = df[:, 0], df[:, 1], int(df[0, 2])
    shown = np.nonzero(time >= interstimulus)[0]
    if len(shown):
        onset = shown[0]
        for k in range(onset, len(keys)):
            if keys[k] in (0, 1):
                return stim, int(keys[k]), float(time[k] - time[onset])
    return stim, None, None


def score_trials(trials_dir, suj, n_trials, interstimulus, rule):
    """One dict per trial, in the order shown. rule(stim) gives (correct
    key: 0 left / 1 right, congruent: True/False, or None when the task
    has no congruent/incongruent trials)."""
    trials = []
    for i in range(n_trials):
        stim, key, rt = read_trial(trials_dir / f"SUJ{suj}_trial{i}.csv", interstimulus)
        correct_key, congruent = rule(stim)
        if key is None:
            outcome = "omissa"
        elif rt <= ANTICIPATORY_MS:
            outcome = "antecipada"
        elif key == correct_key:
            outcome = "correta"
        else:
            outcome = "errada"
        trials.append({"stim": stim, "side": correct_key, "congruent": congruent, "outcome": outcome, "rt": rt})
    return trials


def _round(value):
    return round(value, 1) if value == value else NAN  # NaN stays NaN


def _cell(trials):
    count = {o: sum(t["outcome"] == o for t in trials) for o in ("correta", "errada", "antecipada", "omissa")}
    answered = count["correta"] + count["errada"]
    rts = [t["rt"] for t in trials if t["outcome"] == "correta"]
    return {
        "n_tentativas": len(trials),
        "n_corretas": count["correta"],
        "n_erradas": count["errada"],
        "n_antecipadas": count["antecipada"],
        "n_omissas": count["omissa"],
        "pct_corretas": _round(100 * count["correta"] / answered) if answered else NAN,
        "pct_antecipadas": _round(100 * count["antecipada"] / len(trials)) if trials else NAN,
        "tr_mediana": _round(float(np.median(rts))) if rts else NAN,
        "tr_media": _round(float(np.mean(rts))) if rts else NAN,
    }


def _put(out, name, trials, columns):
    cell = _cell(trials)
    for col in columns:
        out[f"{col}_{name}" if name else col] = cell[col]
    return cell


def summarize(trials, info):
    """The summary row: `info` (subject code, condition...) followed by
    the scores — see the README for each column."""
    out = dict(info)
    _put(out, "", trials, FULL)
    if all(t["congruent"] is None for t in trials):
        return out

    cong = _put(out, "cong", [t for t in trials if t["congruent"]], BY_TYPE)
    inc = _put(out, "inc", [t for t in trials if t["congruent"] is False], BY_TYPE)
    out["efeito_congruencia_pct"] = _round(cong["pct_corretas"] - inc["pct_corretas"])
    out["efeito_congruencia_tr"] = _round(inc["tr_mediana"] - cong["tr_mediana"])
    out["efeito_congruencia_tr_rel"] = (_round(100 * (inc["tr_mediana"] - cong["tr_mediana"]) / cong["tr_mediana"])
                                        if cong["tr_mediana"] else NAN)

    # Local context: each trial against the one before it (the first trial
    # has none). "troca" = the type changed; "lado" = where the correct
    # answer was (same key as the previous trial, or the other one)
    pairs = [(trials[i - 1], trials[i]) for i in range(1, len(trials))]
    switch = lambda p, t: t["congruent"] != p["congruent"]
    same_side = lambda p, t: t["side"] == p["side"]
    groups = {
        "sem_troca": lambda p, t: not switch(p, t),
        "com_troca": switch,
        "sem_troca_cong": lambda p, t: not switch(p, t) and t["congruent"],
        "sem_troca_inc": lambda p, t: not switch(p, t) and not t["congruent"],
        "com_troca_cong": lambda p, t: switch(p, t) and t["congruent"],
        "com_troca_inc": lambda p, t: switch(p, t) and not t["congruent"],
        "sem_troca_mesmo_lado": lambda p, t: not switch(p, t) and same_side(p, t),
        "sem_troca_lado_oposto": lambda p, t: not switch(p, t) and not same_side(p, t),
        "com_troca_mesmo_lado": lambda p, t: switch(p, t) and same_side(p, t),
        "com_troca_lado_oposto": lambda p, t: switch(p, t) and not same_side(p, t),
    }
    cells = {name: _put(out, name, [t for p, t in pairs if test(p, t)], BY_CONTEXT)
             for name, test in groups.items()}
    out["custo_troca_local_pct"] = _round(cells["sem_troca"]["pct_corretas"] - cells["com_troca"]["pct_corretas"])
    out["custo_troca_local_tr"] = _round(cells["com_troca"]["tr_mediana"] - cells["sem_troca"]["tr_mediana"])
    return out
