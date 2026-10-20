import pygame

from .constants import WIDTH, HEIGHT, BLACK, PRACTICE_TRIALS
from .input_box import InputBox, Button

TITLE_FONT = pygame.font.Font(None, 40)
LABEL_FONT = pygame.font.Font(None, 28)
ENGLISH_FONT = pygame.font.Font(None, 20)
BUTTON_FONT = pygame.font.Font(None, 26)
FOOTER_FONT = pygame.font.Font(None, 18)
ERROR_COLOR = (230, 90, 90)
ENGLISH_COLOR = (140, 140, 140)
FOOTER_COLOR = (110, 110, 110)
FOOTER_TEXT = "Desenvolvido por Tércio Apolinário-Souza — edf.tercio@gmail.com"


class SettingsScreen:
    """Pre-task form: participant code, variant (2 or 6 shapes), number of
    trials, presentation time and interstimulus. Blocks until the user
    clicks 'Começar' with valid values (returns a config dict), or closes
    the window / presses Esc (returns None)."""

    def __init__(self, win, defaults):
        self.win = win
        self.variant = defaults.get("variant")
        self.error = ""

        cx = WIDTH // 2
        box_w, box_h = 280, 44
        self.gap = 78
        self.top = HEIGHT // 2 - 230

        self.suj_box = InputBox(cx - box_w // 2, self.top, box_w, box_h,
                                 text=str(defaults.get("suj", "1")), max_len=20)

        self.variant_2_btn = Button(cx - box_w // 2, self.top + self.gap, box_w // 2 - 5, box_h,
                                     "2 formas", selected=self.variant == 2)
        self.variant_6_btn = Button(cx + 5, self.top + self.gap, box_w // 2 - 5, box_h,
                                     "6 formas", selected=self.variant == 6)

        self.n_trials_box = InputBox(cx - box_w // 2, self.top + self.gap * 2, box_w, box_h,
                                      text=str(defaults.get("n_trials", 48)), numeric=True, max_len=4)
        self.presentation_box = InputBox(cx - box_w // 2, self.top + self.gap * 3, box_w, box_h,
                                          text=str(defaults.get("presentation_time", 750)), numeric=True, max_len=5)
        self.interstimulus_box = InputBox(cx - box_w // 2, self.top + self.gap * 4, box_w, box_h,
                                           text=str(defaults.get("interstimulus", 500)), numeric=True, max_len=5)

        self.fields = [self.suj_box, self.n_trials_box, self.presentation_box, self.interstimulus_box]

        btn_row_y = self.top + self.gap * 5 + 20
        half_btn_w = (box_w - 10) // 2
        self.start_btn = Button(cx - box_w // 2, btn_row_y, half_btn_w, box_h,
                                 "Começar", font=BUTTON_FONT)
        self.practice_btn = Button(cx - box_w // 2 + half_btn_w + 10, btn_row_y, half_btn_w, box_h,
                                    "Familiarização", font=BUTTON_FONT)

        # (label in Portuguese, English translation, y position)
        self.labels = [
            ("Código do sujeito", "Subject code", self.top),
            ("Tarefa: número de formas", "Task: number of shapes", self.top + self.gap),
            ("Número de tentativas", "Number of trials", self.top + self.gap * 2),
            ("Tempo de apresentação (ms)", "Presentation time", self.top + self.gap * 3),
            ("Interstímulo (ms)", "Interstimulus", self.top + self.gap * 4),
        ]

    def _base_fields(self):
        """Fields shared by 'Começar' and 'Familiarização': subject code,
        variant, presentation time and interstimulus. Returns
        (values, error)."""
        suj = self.suj_box.text.strip()
        if not suj:
            return None, "Informe o código do sujeito."
        if self.variant not in (2, 6):
            return None, "Selecione a tarefa: 2 ou 6 formas."
        try:
            presentation_time = int(self.presentation_box.text)
            interstimulus = int(self.interstimulus_box.text)
        except ValueError:
            return None, "Tempo de apresentação e interstímulo devem ser números."
        if presentation_time <= 0:
            return None, "Tempo de apresentação deve ser maior que zero."
        if interstimulus < 0:
            return None, "Interstímulo não pode ser negativo."
        return {
            "suj": suj,
            "variant": self.variant,
            "presentation_time": presentation_time,
            "interstimulus": interstimulus,
        }, None

    def _validate(self):
        base, error = self._base_fields()
        if error:
            return None, error
        try:
            n_trials = int(self.n_trials_box.text)
        except ValueError:
            return None, "Número de tentativas deve ser um número."
        if n_trials <= 0 or n_trials % self.variant != 0:
            return None, f"Número de tentativas deve ser positivo e múltiplo de {self.variant}."
        return {**base, "n_trials": n_trials}, None

    def _validate_practice(self):
        """Same required fields as 'Começar', but always runs a short
        practice block instead of the typed number of trials: the
        smallest multiple of the chosen variant that is at least
        PRACTICE_TRIALS, so every shape appears at least once (the
        shape-balancing loop in background.py never ends otherwise)."""
        base, error = self._base_fields()
        if error:
            return None, error
        reps = -(-PRACTICE_TRIALS // self.variant)  # ceil division
        n_trials = self.variant * reps
        return {**base, "n_trials": n_trials, "practice": True}, None

    def preset(self, practice=False):
        """What 'Começar' (or 'Familiarização') would return with the
        pre-filled values, without showing the screen — used by the
        battery's guided mode. Returns (config, error)."""
        return self._validate_practice() if practice else self._validate()

    def run(self):
        clock = pygame.time.Clock()
        pygame.mouse.set_visible(True)

        while True:
            clock.tick(60)
            submit = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return None

                for box in self.fields:
                    box.handle_event(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for box in self.fields:
                        if box.rect.collidepoint(event.pos):
                            for other in self.fields:
                                if other is not box:
                                    other.set_active(False)

                if self.variant_2_btn.clicked(event):
                    self.variant = 2
                if self.variant_6_btn.clicked(event):
                    self.variant = 6

                if self.start_btn.clicked(event):
                    submit = self._validate
                if self.practice_btn.clicked(event):
                    submit = self._validate_practice
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    submit = self._validate

            if submit:
                config, error = submit()
                if config:
                    return config
                self.error = error

            self._draw()

    def _draw(self):
        self.win.fill(BLACK)

        title = TITLE_FONT.render("Abstract Shapes — Configuração", True, (255, 255, 255))
        self.win.blit(title, (WIDTH // 2 - title.get_width() // 2, self.top - 70))

        for text, english, y in self.labels:
            lbl = LABEL_FONT.render(text, True, (200, 200, 200))
            x = WIDTH // 2 - 140
            self.win.blit(lbl, (x, y - 26))
            eng = ENGLISH_FONT.render(f"({english})", True, ENGLISH_COLOR)
            self.win.blit(eng, (x + lbl.get_width() + 8, y - 22))

        for box in self.fields:
            box.draw(self.win)

        self.variant_2_btn.selected = self.variant == 2
        self.variant_6_btn.selected = self.variant == 6
        self.variant_2_btn.draw(self.win)
        self.variant_6_btn.draw(self.win)

        self.start_btn.draw(self.win)
        self.practice_btn.draw(self.win)

        if self.error:
            err = LABEL_FONT.render(self.error, True, ERROR_COLOR)
            self.win.blit(err, (WIDTH // 2 - err.get_width() // 2, self.top + self.gap * 5 + 75))

        footer = FOOTER_FONT.render(FOOTER_TEXT, True, FOOTER_COLOR)
        self.win.blit(footer, (WIDTH // 2 - footer.get_width() // 2, HEIGHT - footer.get_height() - 12))

        pygame.display.update()
