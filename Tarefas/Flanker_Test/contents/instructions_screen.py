import pygame

from .constants import WIDTH, HEIGHT, BLACK, INSTRUCTION_VIDEOS
from .input_box import Button
from .video import open_video

HINT_FONT = pygame.font.Font(None, 24)
VIDEO_BUTTON_FONT = pygame.font.Font(None, 24)
HINT_COLOR = (200, 200, 200)

# Always offered, in this order, regardless of the condition chosen —
# "geral" covers the task as a whole, "rosa"/"azul" the color-specific
# parts (relevant even outside "mixed", since the experimenter may want to
# preview them either way).
VIDEO_LABELS = {
    "geral": "▶ Instrução geral",
    "rosa": "▶ Instrução rosa",
    "azul": "▶ Instrução azul",
}


def show_instructions(win, session):
    """Shows the condition's instruction image (img/inicio.png) plus one
    button per instruction video (geral, rosa, azul) so the experimenter
    can play any of them before starting, and waits for the participant to
    press Space. Returns False if the window is closed instead (so the
    caller can quit cleanly)."""

    image = pygame.image.load(str(session.img_dir / "inicio.png"))
    image = pygame.transform.scale(image, (int(WIDTH * .50), int(WIDTH * .50)))

    btn_w, btn_h, gap = int(WIDTH * .18), 44, 16
    video_btns = [
        (Button(40, 40 + i * (btn_h + gap), btn_w, btn_h,
                VIDEO_LABELS[key], font=VIDEO_BUTTON_FONT), path)
        for i, (key, path) in enumerate(INSTRUCTION_VIDEOS.items())
    ]

    pygame.mouse.set_visible(True)

    clock = pygame.time.Clock()
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return True
            for btn, video_path in video_btns:
                if btn.clicked(event):
                    open_video(video_path)

        win.fill(BLACK)
        win.blit(image, (WIDTH * .30, 0))

        for btn, _ in video_btns:
            btn.draw(win)

        hint = HINT_FONT.render("Pressione ESPAÇO para começar", True, HINT_COLOR)
        win.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT - hint.get_height() - 20))

        pygame.display.update()
