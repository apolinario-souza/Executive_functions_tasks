import argparse
from pathlib import Path

import pygame

pygame.init()


def _parse_args():
    parser = argparse.ArgumentParser(description="Go/No-Go Task")
    # None of these override the settings screen — they only pre-fill it.
    parser.add_argument("--suj", default="1")
    parser.add_argument("--n-trials", type=int, default=20)
    parser.add_argument("--lim-time", type=int, default=750)
    parser.add_argument("--interstimulus", type=int, default=500)
    # Used by the battery's guided mode (Tarefas/Battery): skip the
    # settings screen, run straight from the values above and hand the
    # summary to the battery in --result-file instead of a "Save as" window.
    parser.add_argument("--guided", action="store_true")
    parser.add_argument("--practice", action="store_true")
    parser.add_argument("--result-file", default=None)
    # Ignore unknown args so this also works fine if invoked from a future
    # battery launcher that passes extra shared flags.
    args, _unknown = parser.parse_known_args()
    return args


ARGS = _parse_args()

#Values pre-filled into the settings screen (see contents/settings_screen.py)
DEFAULTS = {
    "suj": ARGS.suj,
    "n_trials": ARGS.n_trials,
    "lim_time": ARGS.lim_time,
    "interstimulus": ARGS.interstimulus,
}

#Fixed task parameters (not exposed in the settings screen)
PERC_6 = .15  # % das tentativas devem ser o número 6
PRACTICE_TRIALS = 8  # trials run by the "Familiarização" button

#Data root: audios/ and the results spreadsheets live next to main.py
BASE_DIR = Path(__file__).resolve().parent.parent
AUDIO_DIR = BASE_DIR / "audios"

#Configuration screen
screen = pygame.display.set_mode()
WIDTH, HEIGHT  = screen.get_size()

#Colors
BLACK = (0, 0, 0)
