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
    ("Abstract Shapes", BASE_DIR / "Abstract_Shapes" / "main.py", INSTRUCTIONS_DIR / "Abstract_2.webm"),
    ("Arrows", BASE_DIR / "Arrows" / "main.py", INSTRUCTIONS_DIR / "Arrows.webm"),
    ("Dots", BASE_DIR / "Dots" / "main.py", INSTRUCTIONS_DIR / "Dots.webm"),
    ("Pictures", BASE_DIR / "Pictures" / "main.py", INSTRUCTIONS_DIR / "Pictures.webm"),
]

#Configuration screen
screen = pygame.display.set_mode()
WIDTH, HEIGHT  = screen.get_size()

#Colors
BLACK = (0, 0, 0)
