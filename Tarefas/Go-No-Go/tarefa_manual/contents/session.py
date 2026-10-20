import random

from .constants import PERC_6


class Session:
    """Resolves a validated config dict (from the settings screen, or from
    the battery's guided mode) into the concrete parameters this run uses,
    including the shuffled sequence of numbers."""

    def __init__(self, config):
        self.suj = config["suj"]
        self.n_trials = config["n_trials"]
        self.lim_time = config["lim_time"]
        self.interstimulus = config["interstimulus"]
        self.practice = config.get("practice", False)

        # At least one 6, so even the short practice block has a "go" trial
        num_sixes = max(1, int(self.n_trials * PERC_6))
        others = [str(random.choice([1, 2, 3, 4, 5, 7, 8, 9])) for _ in range(self.n_trials - num_sixes)]
        self.sequence = ["6"] * num_sixes + others
        random.shuffle(self.sequence)
