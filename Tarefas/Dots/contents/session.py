from .constants import BASE_DIR

# Per-condition legend text (matches what each condition's main.py used to
# write by hand).
_LEGEND_TEXT = {
    "congruent": ("1 = dots stripes left; 2 = dots stripes left; 3 = dots stripes right; 4 = dots stripes right "
                  "\n 0 = key left; 1 = key right; -1 = no key"),
    "incongruent": ("1 = dots solid left; 2 = dots solid left; 3 = dots solid right; 4 = dots solid right "
                     "\n 0 = key left; 1 = key right; -1 = no key"),
    "mixed": ("1 = dots stripes left; 2 = dots solid left; 3 = dots stripes right; 4 = dots solid right "
              "\n 0 = key left; 1 = key right; -1 = no key"),
}


def stimulus_texture(condition, value):
    """Which dot texture image to show for a given stimulus value (1-4),
    under the given condition."""
    if condition == "congruent":
        return "dots_stripes.png"
    if condition == "incongruent":
        return "dots_solid.png"
    # mixed: odd values (1, 3) are striped, even values (2, 4) are solid
    return "dots_stripes.png" if value in (1, 3) else "dots_solid.png"


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

        self.condition_dir = BASE_DIR / self.condition
        self.img_dir = self.condition_dir / "img"
        self.trials_dir = self.condition_dir / "trials"

        self._write_legend()

    def _write_legend(self):
        with open(str(self.trials_dir / "legend.txt"), "w") as f:
            f.write(_LEGEND_TEXT[self.condition])
