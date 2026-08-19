from .constants import BASE_DIR


class Session:
    """Resolves a validated config dict (from the settings screen, or from
    a future battery launcher) into the concrete parameters and paths the
    task runs with, and writes the trial legend for this run."""

    def __init__(self, config):
        self.suj = config["suj"]
        self.n_shapes = config["variant"]
        self.n_trials = config["n_trials"]
        self.presentation_time = config["presentation_time"]
        self.interstimulus = config["interstimulus"]

        variant_folder = "two_shapes" if self.n_shapes == 2 else "six_shapes"
        self.variant_dir = BASE_DIR / variant_folder
        self.img_dir = self.variant_dir / "img"
        self.trials_dir = self.variant_dir / "trials"

        self._write_legend()

    def _write_legend(self):
        half = self.n_shapes // 2
        left = [f"{i} = shape left {i}" for i in range(1, half + 1)]
        right = [f"{half + i} = shape right{i}" for i in range(1, half + 1)]
        text = "; ".join(left + right) + " \n 0 = key left; 1 = key right; -1 = no key"
        with open(str(self.trials_dir / "legend.txt"), "w") as f:
            f.write(text)
