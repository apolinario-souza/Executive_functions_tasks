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
    defaults = DEFAULTS

    while True:
        settings = SettingsScreen(WIN, defaults)
        config = settings.run()
        if config is None:
            break

        session = Session(config)

        if not show_instructions(WIN, session):
            break

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

        if not draw.background.finished:
            break

        if config.get("practice"):
            # Practice round done: back to the settings screen (with the
            # same values already filled in) so the experimenter can start
            # the real task next.
            defaults = config
            continue

        # All trials done: score this subject and let the experimenter
        # choose where to save the processed summary.
        summary = summarize_subject(session)
        save_summary_dialog(summary, default_name=f"Arrows_SUJ{session.suj}.csv")
        break

    pygame.quit()
    sys.exit(0)

main()
