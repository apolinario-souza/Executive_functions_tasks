import argparse
from pathlib import Path

import pygame

pygame.init()


def _parse_args():
    parser = argparse.ArgumentParser(description="Abstract Shapes Task")
    # None of these override the settings screen — they only pre-fill it,
    # so a shortcut like Executable.bat can suggest a variant/participant
    # while still letting the experimenter confirm or change everything.
    parser.add_argument("--variant", type=int, choices=(2, 6), default=None)
    parser.add_argument("--suj", default="1")
    parser.add_argument("--n-trials", type=int, default=48)
    parser.add_argument("--presentation-time", type=int, default=750)
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
    "variant": ARGS.variant,
    "n_trials": ARGS.n_trials,
    "presentation_time": ARGS.presentation_time,
    "interstimulus": ARGS.interstimulus,
}

#Fixed task parameter (not exposed in the settings screen)
PERC_SWITCHES = .5
# Minimum trials run by the "Familiarização" button. The settings screen
# rounds this up to a multiple of the chosen variant (2 or 6 shapes) so
# every shape appears at least once — target_control() in background.py
# loops forever otherwise.
PRACTICE_TRIALS = 4

#Data root: each variant's img/ and trials/ live one level below here
BASE_DIR = Path(__file__).resolve().parent.parent

#Configuration screen
screen = pygame.display.set_mode()
WIDTH, HEIGHT  = screen.get_size()

#Colors
BLACK = (0, 0, 0)
