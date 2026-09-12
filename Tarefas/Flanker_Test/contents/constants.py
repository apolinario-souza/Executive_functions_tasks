import argparse
from pathlib import Path

import pygame

pygame.init()

CONDITIONS = ("azul", "rosa", "mixed")

# Number of stimulus categories per condition: azul/rosa show one color (4
# categories: all-left, side-left, all-right, side-right); mixed shows both
# colors back to back (8 categories: rosa 1-4, azul 5-8).
N_CATEGORIES = {"azul": 4, "rosa": 4, "mixed": 8}

# Trials run by the "Familiarização" button: one per category, so the
# balanced generator (see contents/background.py) always has enough trials
# to place at least one of each category.
PRACTICE_TRIALS = dict(N_CATEGORIES)


def _parse_args():
    parser = argparse.ArgumentParser(description="Flanker Test")
    # None of these override the settings screen — they only pre-fill it.
    parser.add_argument("--condition", choices=CONDITIONS, default=None)
    parser.add_argument("--suj", default="1")
    parser.add_argument("--n-trials", type=int, default=24)
    parser.add_argument("--presentation-time", type=int, default=2500)
    parser.add_argument("--interstimulus", type=int, default=500)
    parser.add_argument("--feedback-time", type=int, default=1500)
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
    "feedback_time": ARGS.feedback_time,
}

#Fixed task parameters (not exposed in the settings screen)
PERC_SWITCHES = .5

#Data root: each condition's img/ and trials/ live one level below here
BASE_DIR = Path(__file__).resolve().parent.parent

# Instruction videos, offered as buttons on the instructions screen
# (contents/instructions_screen.py) so the experimenter can play any of
# them just before starting. Kept here (instead of only in the Battery
# launcher) so they're reachable from Flanker's own screen; order matches
# how they're shown: geral, rosa, azul.
VIDEO_DIR = BASE_DIR.parent.parent / "instrucao"
INSTRUCTION_VIDEOS = {
    "geral": VIDEO_DIR / "gerais_flaker.mp4",
    "rosa": VIDEO_DIR / "Flaker_rosa.mp4",
    "azul": VIDEO_DIR / "Flaker_azul.mp4",
}

#Configuration screen
screen = pygame.display.set_mode()
WIDTH, HEIGHT = screen.get_size()

#Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
