import argparse
from pathlib import Path

import pygame

pygame.init()

CONDITIONS = ("congruent", "incongruent", "mixed")


def _parse_args():
    parser = argparse.ArgumentParser(description="Dots Task")
    # None of these override the settings screen — they only pre-fill it.
    parser.add_argument("--condition", choices=CONDITIONS, default=None)
    parser.add_argument("--suj", default="1")
    parser.add_argument("--n-trials", type=int, default=20)
    parser.add_argument("--presentation-time", type=int, default=750)
    parser.add_argument("--interstimulus", type=int, default=500)
    # Ignore unknown args so this also works fine if invoked from a future
    # battery launcher that passes extra shared flags.
    args, _unknown = parser.parse_known_args()
    return args


ARGS = _parse_args()

#Values pre-filled into the settings screen (see contents/settings_screen.py)
DEFAULTS = {
    "suj": ARGS.suj,
    "condition": ARGS.condition,
    "n_trials": ARGS.n_trials,
    "presentation_time": ARGS.presentation_time,
    "interstimulus": ARGS.interstimulus,
}

#Fixed task parameters (not exposed in the settings screen)
PERC_SWITCHES = .5
N_CATEGORIES = 4  # 2 screen sides x 2 dot textures
PRACTICE_TRIALS = 4  # trials run by the "Familiarização" button

#Data root: each condition's img/ and trials/ live one level below here
BASE_DIR = Path(__file__).resolve().parent.parent

#Configuration screen
screen = pygame.display.set_mode()
WIDTH, HEIGHT  = screen.get_size()

#Colors
BLACK = (0, 0, 0)
