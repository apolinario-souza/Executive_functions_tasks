from .constants import IMG_DIR, TRIALS_DIR


class Session:
    """Resolves a validated config dict (from the settings screen, or from
    a future battery launcher) into the concrete parameters this run uses,
    and writes the trial legend for this run."""

    def __init__(self, config):
        self.suj = config["suj"]
        self.n_trials = config["n_trials"]
        self.presentation_time = config["presentation_time"]
        self.interstimulus = config["interstimulus"]

        self.img_dir = IMG_DIR
        self.trials_dir = TRIALS_DIR

        self._write_legend()

    def _write_legend(self):
        text = ("1 = arrow left; 2 = 45 right in left side; 3 = arrow right; 4 = 45 left in right side "
                "\n 0 = key left; 1 = key right; -1 = no key")
        with open(str(self.trials_dir / "legend.txt"), "w") as f:
            f.write(text)
