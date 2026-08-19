import argparse
from pathlib import Path

import pygame

pygame.init()


def _parse_args():
    parser = argparse.ArgumentParser(description="Arrows Task")
    # None of these override the settings screen — they only pre-fill it.
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
    "n_trials": ARGS.n_trials,
    "presentation_time": ARGS.presentation_time,
    "interstimulus": ARGS.interstimulus,
}

#Fixed task parameters (not exposed in the settings screen)
PERC_SWITCHES = .5
N_CATEGORIES = 4  # down/downRight (left side), down/downLeft (right side)

#Data root: img/ and trials/ live next to this task's main.py
BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR = BASE_DIR / "img"
TRIALS_DIR = BASE_DIR / "trials"

#Configuration screen
screen = pygame.display.set_mode()
WIDTH, HEIGHT  = screen.get_size()

#Colors
BLACK = (0, 0, 0)
