import sys

import pygame

from contents.constants import WIDTH, HEIGHT, DEFAULTS
from contents.settings_screen import SettingsScreen
from contents.session import Session
from contents.instructions_screen import show_instructions
from contents.draw import Draw
from contents.results import summarize_subject, save_summary_dialog

'''
“for this one press the left button”; “for this one press right”
'''

FPS = 200

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('Abstract Shapes Task')

pygame.init()


def main():
    settings = SettingsScreen(WIN, DEFAULTS)
    config = settings.run()
    if config is None:
        pygame.quit()
        sys.exit(0)

    session = Session(config)

    if not show_instructions(WIN, session):
        pygame.quit()
        sys.exit(0)

    draw = Draw(WIN, session)

    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        draw.update()

        if draw.background.finished:
            run = False

    completed = draw.background.finished
    pygame.quit()

    if completed:
        # All trials done: score this subject and let the experimenter
        # choose where to save the processed summary.
        variant_name = "two" if session.n_shapes == 2 else "six"
        summary = summarize_subject(session)
        save_summary_dialog(summary, default_name=f"Abstract_{variant_name}_SUJ{session.suj}.csv")

    sys.exit(0)

main()
