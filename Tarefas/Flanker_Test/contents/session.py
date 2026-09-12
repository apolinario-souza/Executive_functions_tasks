from .constants import BASE_DIR, N_CATEGORIES

# Which color(s) a condition draws stimuli from, and in what order. `mixed`
# draws stimulus values 1-4 from rosa and 5-8 from azul — confirmed by
# reading the pre-modernization Tarefa_3/contents/background.py.
_COLOR_BLOCKS = {
    "azul": ("azul",),
    "rosa": ("rosa",),
    "mixed": ("rosa", "azul"),
}

# Image-suffix per local position (1-4) within a color block:
# 1 = all pointing left, 2 = side-left (center diverges), 3 = all right,
# 4 = side-right (center diverges). azul and rosa swap the DE/ED suffix for
# 2/4 — that's just which art asset was drawn for each color, preserved
# as-is from the original task.
_SUFFIX_BY_COLOR_LOCAL = {
    "azul": {1: "E", 2: "DE", 3: "D", 4: "ED"},
    "rosa": {1: "E", 2: "ED", 3: "D", 4: "DE"},
}


def stimulus_parts(condition, value):
    """Splits a 1-based stimulus value into (color, local) where local is
    1-4 (position within that color's block)."""
    colors = _COLOR_BLOCKS[condition]
    block = (value - 1) // 4
    local = (value - 1) % 4 + 1
    return colors[block], local


def stimulus_suffix(condition, value):
    """Image filename suffix (E/D/DE/ED) for a stimulus value."""
    color, local = stimulus_parts(condition, value)
    return color, _SUFFIX_BY_COLOR_LOCAL[color][local]


def correct_key(local):
    """0 (left) for local 1/2, 1 (right) for local 3/4."""
    return 0 if local in (1, 2) else 1


def is_congruent(local):
    """Odd local (all pointing the same way) = congruent; even local
    (center diverges from the sides) = incongruent."""
    return local % 2 == 1


def _legend_text(condition):
    lines = []
    for value in range(1, N_CATEGORIES[condition] + 1):
        color, local = stimulus_parts(condition, value)
        side = "esquerda" if correct_key(local) == 0 else "direita"
        shape = "todos" if is_congruent(local) else "lateral (centro diverge)"
        lines.append(f"{value} = {color}, {shape}, {side}")
    lines.append("0 = tecla esquerda; 1 = tecla direita; -1 = sem resposta")
    return "\n".join(lines)


class Session:
    """Resolves a validated config dict (from the settings screen, or from
    a future battery launcher) into the concrete parameters and paths this
    run uses, and writes the trial legend for this run."""

    def __init__(self, config):
        self.suj = config["suj"]
        self.condition = config["condition"]
        self.n_trials = config["n_trials"]
        self.presentation_time = config["presentation_time"]
        self.interstimulus = config["interstimulus"]
        self.feedback_time = config["feedback_time"]

        self.condition_dir = BASE_DIR / self.condition
        self.img_dir = self.condition_dir / "img"
        self.trials_dir = self.condition_dir / "trials"

        self._write_legend()

    def _write_legend(self):
        with open(str(self.trials_dir / "legend.txt"), "w") as f:
            f.write(_legend_text(self.condition))
