import pygame

from .constants import WIDTH, HEIGHT, BLACK

TITLE_FONT = pygame.font.Font(None, int(HEIGHT * .10))
TEXT_FONT = pygame.font.Font(None, int(HEIGHT * .065))

# (text, color)
LINES = [
    ("Você vai ver números na tela e ouvir o som de cada um.", (255, 255, 255)),
    ("REGRA:", (0, 255, 0)),
    ("Aperte a BARRA DE ESPAÇO só quando for o número 6.", (255, 255, 255)),
    ("Nos outros números, não aperte nada.", (255, 255, 255)),
    ("Responda o mais rápido possível!", (255, 255, 255)),
]


def show_instructions(win):
    """Shows the rule (press Space only for the number 6) and waits for
    the participant to press Space. Returns False if the window is closed
    or Esc is pressed instead (so the caller can quit cleanly)."""

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
        title = TITLE_FONT.render("Go/No-Go", True, (255, 255, 255))
        win.blit(title, (WIDTH // 2 - title.get_width() // 2, int(HEIGHT * .10)))
        for i, (text, color) in enumerate(LINES):
            line = TEXT_FONT.render(text, True, color)
            win.blit(line, (WIDTH // 2 - line.get_width() // 2, int(HEIGHT * (.28 + i * .10))))
        start = TEXT_FONT.render("Aperte ESPAÇO para começar", True, (0, 255, 255))
        win.blit(start, (WIDTH // 2 - start.get_width() // 2, int(HEIGHT * .85)))
        pygame.display.update()
