from pathlib import Path

import pygame

pygame.init()

# Tarefas/ (this launcher's parent folder) — each task lives in its own
# sibling folder there, with its own main.py handling settings/instructions/
# trials/results on its own.
BASE_DIR = Path(__file__).resolve().parent.parent.parent
INSTRUCTIONS_DIR = BASE_DIR.parent / "instrucao"

# (label shown on the button, path to that task's main.py, path to its
# instructions video). Abstract Shapes has two variants with separate
# videos; the "?" button here opens the two-shapes one.
TASKS = [
    ("Arrows", BASE_DIR / "Arrows" / "main.py", INSTRUCTIONS_DIR / "Arrows.mp4"),
    ("Dots", BASE_DIR / "Dots" / "main.py", INSTRUCTIONS_DIR / "Dots.mp4"),
    ("Abstract Shapes", BASE_DIR / "Abstract_Shapes" / "main.py", INSTRUCTIONS_DIR / "Abstract_2.mp4"),
    ("Pictures", BASE_DIR / "Pictures" / "main.py", INSTRUCTIONS_DIR / "Pictures.mp4"),
    ("Flanker Test", BASE_DIR / "Flanker_Test" / "main.py", INSTRUCTIONS_DIR / "gerais_flaker.mp4"),
]

#Configuration screen
screen = pygame.display.set_mode()
WIDTH, HEIGHT  = screen.get_size()

#Colors
BLACK = (0, 0, 0)
