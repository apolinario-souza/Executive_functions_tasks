import subprocess
import sys

import pygame

from .constants import WIDTH, HEIGHT, BLACK, TASKS
from .input_box import Button
from .video import open_video

TITLE_FONT = pygame.font.Font(None, 44)
SUBTITLE_FONT = pygame.font.Font(None, 22)
BUTTON_FONT = pygame.font.Font(None, 32)
QUESTION_FONT = pygame.font.Font(None, 24)
FOOTER_FONT = pygame.font.Font(None, 18)
NOTE_COLOR = (230, 90, 90)
FOOTER_COLOR = (110, 110, 110)
FOOTER_TEXT = "Desenvolvido por Tércio Apolinário-Souza — edf.tercio@gmail.com"


class LauncherScreen:
    """Battery menu: one button per task, plus a small "?" button next to
    each one that has an instructions video (some tasks, like Flanker
    Test, show their own instead — see TASKS in contents/constants.py).
    Clicking a task button hides this window, runs that task's main.py as
    a subprocess and waits for it to close, then brings this menu back so
    another task can be picked."""

    def __init__(self):
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Bateria de Funções Executivas')

        btn_w, btn_h, q_w, small_gap, gap = 300, 66, 40, 8, 22
        row_w = btn_w + small_gap + q_w
        total_h = len(TASKS) * btn_h + (len(TASKS) - 1) * gap
        self.top = HEIGHT // 2 - total_h // 2
        row_x = WIDTH // 2 - row_w // 2

        self.rows = []
        for i, (label, main_path, video_path) in enumerate(TASKS):
            rect_y = self.top + i * (btn_h + gap)
            task_btn = Button(row_x, rect_y, btn_w, btn_h, label, font=BUTTON_FONT)
            question_btn = (Button(row_x + btn_w + small_gap, rect_y, q_w, btn_h, "?", font=QUESTION_FONT)
                             if video_path is not None else None)
            self.rows.append((task_btn, main_path, question_btn, video_path))

        self.note = ""

    def _launch(self, main_path):
        pygame.display.quit()
        try:
            result = subprocess.run([sys.executable, str(main_path)], cwd=str(main_path.parent))
            if result.returncode == 0:
                self.note = ""
            else:
                self.note = f"A última tarefa fechou com um erro (código {result.returncode})."
        except Exception as exc:
            self.note = f"Não foi possível abrir a tarefa: {exc}"

        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Bateria de Funções Executivas')

    def run(self):
        clock = pygame.time.Clock()
        pygame.mouse.set_visible(True)

        while True:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
                for task_btn, main_path, question_btn, video_path in self.rows:
                    if task_btn.clicked(event):
                        self._launch(main_path)
                    if question_btn is not None and question_btn.clicked(event):
                        open_video(video_path)

            self._draw()

    def _draw(self):
        self.win.fill(BLACK)

        title = TITLE_FONT.render("Bateria de Funções Executivas", True, (255, 255, 255))
        self.win.blit(title, (WIDTH // 2 - title.get_width() // 2, self.top - 100))

        subtitle = SUBTITLE_FONT.render("Escolha uma tarefa para abrir (choose a task to open)",
                                         True, (180, 180, 180))
        self.win.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, self.top - 60))

        for task_btn, _, question_btn, _ in self.rows:
            task_btn.draw(self.win)
            if question_btn is not None:
                question_btn.draw(self.win)

        if self.note:
            note = FOOTER_FONT.render(self.note, True, NOTE_COLOR)
            self.win.blit(note, (WIDTH // 2 - note.get_width() // 2, self.rows[-1][0].rect.bottom + 20))

        footer = FOOTER_FONT.render(FOOTER_TEXT, True, FOOTER_COLOR)
        self.win.blit(footer, (WIDTH // 2 - footer.get_width() // 2, HEIGHT - footer.get_height() - 12))

        pygame.display.update()
