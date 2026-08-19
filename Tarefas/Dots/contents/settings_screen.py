import pygame

from .constants import WIDTH, HEIGHT, BLACK, N_CATEGORIES, CONDITIONS
from .input_box import InputBox, Button

TITLE_FONT = pygame.font.Font(None, 40)
LABEL_FONT = pygame.font.Font(None, 28)
ENGLISH_FONT = pygame.font.Font(None, 20)
CONDITION_FONT = pygame.font.Font(None, 24)
FOOTER_FONT = pygame.font.Font(None, 18)
ERROR_COLOR = (230, 90, 90)
ENGLISH_COLOR = (140, 140, 140)
FOOTER_COLOR = (110, 110, 110)
FOOTER_TEXT = "Desenvolvido por Tércio Apolinário-Souza — edf.tercio@gmail.com"

CONDITION_LABELS = {
    "congruent": "Con",
    "incongruent": "Inco",
    "mixed": "Mix",
}


class SettingsScreen:
    """Pre-task form: participant code, condition (congruent / incongruent
    / mixed), number of trials, presentation time and interstimulus.
    Blocks until the user clicks 'Começar' with valid values (returns a
    config dict), or closes the window / presses Esc (returns None)."""

    def __init__(self, win, defaults):
        self.win = win
        self.condition = defaults.get("condition")
        self.error = ""

        cx = WIDTH // 2
        box_w, box_h = 280, 44
        self.gap = 78
        self.top = HEIGHT // 2 - 230

        self.suj_box = InputBox(cx - box_w // 2, self.top, box_w, box_h,
                                 text=str(defaults.get("suj", "1")), max_len=20)

        cond_w, cond_h, cond_gap = 64, 32, 10
        row_w = len(CONDITIONS) * cond_w + (len(CONDITIONS) - 1) * cond_gap
        row_x = cx - row_w // 2
        self.condition_btns = {
            cond: Button(row_x + i * (cond_w + cond_gap), self.top + self.gap, cond_w, cond_h,
                         CONDITION_LABELS[cond], selected=self.condition == cond, font=CONDITION_FONT)
            for i, cond in enumerate(CONDITIONS)
        }

        self.n_trials_box = InputBox(cx - box_w // 2, self.top + self.gap * 2, box_w, box_h,
                                      text=str(defaults.get("n_trials", 20)), numeric=True, max_len=4)
        self.presentation_box = InputBox(cx - box_w // 2, self.top + self.gap * 3, box_w, box_h,
                                          text=str(defaults.get("presentation_time", 750)), numeric=True, max_len=5)
        self.interstimulus_box = InputBox(cx - box_w // 2, self.top + self.gap * 4, box_w, box_h,
                                           text=str(defaults.get("interstimulus", 500)), numeric=True, max_len=5)

        self.fields = [self.suj_box, self.n_trials_box, self.presentation_box, self.interstimulus_box]

        self.start_btn = Button(cx - box_w // 2, self.top + self.gap * 5 + 20, box_w, box_h, "Começar")

        # (label in Portuguese, English translation, y position)
        self.labels = [
            ("Código do sujeito", "Subject code", self.top),
            ("Condição", "Condition", self.top + self.gap),
            ("Número de tentativas", "Number of trials", self.top + self.gap * 2),
            ("Tempo de apresentação (ms)", "Presentation time", self.top + self.gap * 3),
            ("Interstímulo (ms)", "Interstimulus", self.top + self.gap * 4),
        ]

    def _validate(self):
        suj = self.suj_box.text.strip()
        if not suj:
            return None, "Informe o código do sujeito."
        if self.condition not in CONDITIONS:
            return None, "Selecione a condição: congruente, incongruente ou mista."
        try:
            n_trials = int(self.n_trials_box.text)
            presentation_time = int(self.presentation_box.text)
            interstimulus = int(self.interstimulus_box.text)
        except ValueError:
            return None, "Número de tentativas, tempo de apresentação e interstímulo devem ser números."
        if n_trials <= 0 or n_trials % N_CATEGORIES != 0:
            return None, f"Número de tentativas deve ser positivo e múltiplo de {N_CATEGORIES}."
        if presentation_time <= 0:
            return None, "Tempo de apresentação deve ser maior que zero."
        if interstimulus < 0:
            return None, "Interstímulo não pode ser negativo."
        return {
            "suj": suj,
            "condition": self.condition,
            "n_trials": n_trials,
            "presentation_time": presentation_time,
            "interstimulus": interstimulus,
        }, None

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

                for cond, btn in self.condition_btns.items():
                    if btn.clicked(event):
                        self.condition = cond

                if self.start_btn.clicked(event):
                    submit = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    submit = True

            if submit:
                config, error = self._validate()
                if config:
                    return config
                self.error = error

            self._draw()

    def _draw(self):
        self.win.fill(BLACK)

        title = TITLE_FONT.render("Dots — Configuração", True, (255, 255, 255))
        self.win.blit(title, (WIDTH // 2 - title.get_width() // 2, self.top - 70))

        for text, english, y in self.labels:
            lbl = LABEL_FONT.render(text, True, (200, 200, 200))
            x = WIDTH // 2 - 140
            self.win.blit(lbl, (x, y - 26))
            eng = ENGLISH_FONT.render(f"({english})", True, ENGLISH_COLOR)
            self.win.blit(eng, (x + lbl.get_width() + 8, y - 22))

        for box in self.fields:
            box.draw(self.win)

        for cond, btn in self.condition_btns.items():
            btn.selected = self.condition == cond
            btn.draw(self.win)

        self.start_btn.draw(self.win)

        if self.error:
            err = LABEL_FONT.render(self.error, True, ERROR_COLOR)
            self.win.blit(err, (WIDTH // 2 - err.get_width() // 2, self.top + self.gap * 5 + 75))

        footer = FOOTER_FONT.render(FOOTER_TEXT, True, FOOTER_COLOR)
        self.win.blit(footer, (WIDTH // 2 - footer.get_width() // 2, HEIGHT - footer.get_height() - 12))

        pygame.display.update()
