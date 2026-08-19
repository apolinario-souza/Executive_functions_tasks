import sys

import pygame

from contents.constants import WIDTH, HEIGHT, DEFAULTS
from contents.settings_screen import SettingsScreen
from contents.session import Session
from contents.instructions_screen import show_instructions
from contents.draw import Draw
from contents.results import summarize_subject, save_summary_dialog

'''
""I want you to push the button the arrow is pointing toward. If the arrow is on the side of the box pointing down like this
[E demonstrated] to this button, press this button. If the arrow is on the other side. If the arrow is on the other
side pointing down like this [E demonstrated] to this button, press this button. If the
arrow is on this side, pointing down across the screen like this [E demonstrated] to this button, press this button.
If the arrow is on the other side, pointing down across the screen like this [E demonstrated] to this button, press this button.""
'''

FPS = 200

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('Arrows Task')

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
        summary = summarize_subject(session)
        save_summary_dialog(summary, default_name=f"Arrows_SUJ{session.suj}.csv")

    sys.exit(0)

main()
