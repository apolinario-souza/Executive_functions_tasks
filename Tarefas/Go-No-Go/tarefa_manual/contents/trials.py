import time

import pygame

from .constants import WIDTH, HEIGHT, BLACK, AUDIO_DIR

NUMBER_FONT = pygame.font.Font(None, int(HEIGHT * .20))
FEEDBACK_FONT = pygame.font.Font(None, int(HEIGHT * .10))

COLUMNS = ["Tentativa", "Número Apresentado", "Pressionou?", "Resultado", "Tempo de Reação"]


def _blit_center(win, surface):
    win.blit(surface, (WIDTH // 2 - surface.get_width() // 2, HEIGHT // 2 - surface.get_height() // 2))


def run_trials(win, session):
    """Plays the session's numbers one by one (image + sound), waits up to
    lim_time ms for Space, then shows the feedback for interstimulus ms.
    Returns one row per trial (see COLUMNS), or None if the window was
    closed or Esc pressed before the end."""
    pygame.mixer.init()
    sounds = {str(i): pygame.mixer.Sound(str(AUDIO_DIR / f"{i}.wav")) for i in range(1, 10)}
    pygame.mouse.set_visible(False)

    data = []
    for trial, num in enumerate(session.sequence, start=1):
        # Drop keys pressed during the previous feedback, so they don't
        # count as an instant answer to this number
        pygame.event.clear(pygame.KEYDOWN)
        win.fill(BLACK)
        _blit_center(win, NUMBER_FONT.render(num, True, (255, 255, 255)))
        pygame.display.flip()

        sounds[num].play()
        start_time = time.time()
        pressed = False
        reaction_time = None

        while time.time() - start_time < session.lim_time / 1000:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return None
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not pressed:
                    pressed = True
                    reaction_time = time.time() - start_time

        if num == "6" and pressed:
            result_text = f"Acertou! Tempo: {reaction_time:.3f}s"
            result_type = "Acerto"
        elif num != "6" and pressed:
            result_text = "Erro!"
            result_type = "Erro"
        elif num == "6" and not pressed:
            result_text = "Erro!"
            result_type = "Erro!"
        else:
            result_text = ""
            result_type = "Nenhuma resposta"

        data.append([trial, num, "Sim" if pressed else "Não", result_type, reaction_time if reaction_time else ""])

        win.fill(BLACK)
        _blit_center(win, FEEDBACK_FONT.render(result_text, True, (255, 255, 255)))
        pygame.display.flip()
        time.sleep(session.interstimulus / 1000)

    win.fill(BLACK)
    _blit_center(win, FEEDBACK_FONT.render("Encerrado", True, (255, 255, 255)))
    pygame.display.flip()
    time.sleep(1)
    return data
