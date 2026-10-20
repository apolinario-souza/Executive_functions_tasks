import sys

import pygame

from contents.constants import WIDTH, HEIGHT, DEFAULTS, ARGS
from contents.settings_screen import SettingsScreen
from contents.session import Session
from contents.instructions_screen import show_instructions
from contents.draw import Draw
from contents.results import summarize_subject, save_summary_dialog, save_summary_file

FPS = 200

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('Simon effect')

pygame.init()


def main():
    defaults = DEFAULTS

    while True:
        settings = SettingsScreen(WIN, defaults)
        if ARGS.guided:
            config, error = settings.preset(practice=ARGS.practice)
            if config is None:
                sys.exit(error)
        else:
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
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    run = False

            draw.update()

            if draw.background.finished:
                run = False

        if not draw.background.finished:
            break

        if config.get("practice"):
            if ARGS.guided:
                break  # the battery shows what comes next
            # Practice round done: back to the settings screen (with the
            # same values already filled in) so the experimenter can start
            # the real task next.
            defaults = config
            continue

        # All trials done: score this subject and let the experimenter
        # choose where to save the processed summary.
        summary = summarize_subject(session)
        if ARGS.result_file:
            save_summary_file(summary, ARGS.result_file)
        else:
            save_summary_dialog(summary, default_name=f"Pictures_SUJ{session.suj}.csv")
        break

    pygame.quit()
    sys.exit(0)

main()
