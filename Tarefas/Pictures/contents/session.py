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
        text = ("1 = frog left; 2 = butterfly left; 3 = frog right; 4 = butterfly right "
                "\n 0 = key left; 1 = key right; -1 = no key")
        with open(str(self.trials_dir / "legend.txt"), "w") as f:
            f.write(text)
