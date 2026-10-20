import pygame

from .constants import WIDTH, HEIGHT, BLACK


def show_instructions(win, session):
    """Shows img/inicio.png (frog/butterfly-to-key mapping + 'Barra de
    espaço para iniciar!') and waits for the participant to press Space.
    Returns False if the window is closed instead (so the caller can quit
    cleanly)."""

    image = pygame.image.load(str(session.img_dir / "inicio.png"))
    image = pygame.transform.scale(image, (int(WIDTH * .50), int(WIDTH * .50)))

    pygame.mouse.set_visible(True)

    clock = pygame.time.Clock()
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return True

        win.fill(BLACK)
        win.blit(image, (WIDTH * .30, 0))
        pygame.display.update()
