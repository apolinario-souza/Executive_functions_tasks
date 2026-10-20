import sys

import pygame

from contents.constants import WIDTH, HEIGHT, DEFAULTS, ARGS
from contents.settings_screen import SettingsScreen
from contents.session import Session
from contents.instructions_screen import show_instructions
from contents.trials import run_trials
from contents.results import save_trials, summarize_subject, save_summary_dialog, save_summary_file

'''
Tarefa auditiva: números de 1 a 9 aparecem na tela e são tocados em áudio.
O participante aperta a barra de espaço somente para o número 6 (go) e
não aperta nada para os demais (no-go).
'''

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('Go/No-Go')

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

        if not show_instructions(WIN):
            break

        data = run_trials(WIN, session)
        if data is None:
            break

        if config.get("practice"):
            if ARGS.guided:
                break  # the battery shows what comes next
            # Practice round done: back to the settings screen (with the
            # same values already filled in) so the experimenter can start
            # the real task next.
            defaults = config
            continue

        # All trials done: keep the trial-by-trial spreadsheet, score this
        # subject and let the experimenter choose where to save the summary.
        save_trials(session, data)
        summary = summarize_subject(session, data)
        if ARGS.result_file:
            save_summary_file(summary, ARGS.result_file)
        else:
            save_summary_dialog(summary, default_name=f"GoNoGo_SUJ{session.suj}.csv")
        break

    pygame.quit()
    sys.exit(0)

main()
