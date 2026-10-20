import tkinter as tk

from .constants import TASKS, TITLE, FOOTER_TEXT, BG, PANEL, MUTED, FOOTER, ERROR, GREY
from .session import open_path
from .widgets import label, button, entry, load_icon

COLUMNS = 2


class AdvancedView:
    """Everything on one screen, for the experimenter: each task opens its
    own settings screen (number of trials, times...) pre-filled with the
    participant code typed here, and saves its own CSV with "Save as", as
    when the task is opened by its Executable.bat."""

    def __init__(self, app):
        self.app = app
        self.session = app.session
        self.frame = tk.Frame(app.root, bg=BG)

        header = tk.Frame(self.frame, bg=BG)
        header.pack(fill="x", padx=30, pady=(14, 0))
        label(header, f"{TITLE} — modo avançado", 15, MUTED, bold=True).pack(side="left")
        button(header, "Modo guiado", self.app.show_guided, color=GREY, size=10).pack(side="right")

        label(self.frame, FOOTER_TEXT, 9, FOOTER).pack(side="bottom", pady=6)

        body = tk.Frame(self.frame, bg=BG)
        body.pack(fill="both", expand=True, padx=40, pady=10)

        row = tk.Frame(body, bg=BG)
        row.pack(fill="x", pady=(6, 4))
        label(row, "Código do participante:", 13, bold=True).pack(side="left")
        entry(row, self.session.subject, 10, size=14).pack(side="left", padx=10, ipady=3)
        label(body, "Cada tarefa abre a sua tela de configuração (já com este código), e no fim pede onde "
                    "salvar o próprio arquivo CSV. Os botões \"?\" abrem o vídeo de instruções.",
              11, MUTED, anchor="w", justify="left", wraplength=1100).pack(fill="x", pady=(0, 10))

        self.note = label(body, "", 12, ERROR, anchor="w")
        self.note.pack(fill="x")

        grid = tk.Frame(body, bg=BG)
        grid.pack(fill="x")
        for i, task in enumerate(TASKS):
            grid.columnconfigure(i % COLUMNS, weight=1, uniform="col")
            self._row(grid, task).grid(row=i // COLUMNS, column=i % COLUMNS, sticky="ew", padx=6, pady=4)

    def _row(self, parent, task):
        row = tk.Frame(parent, bg=PANEL, padx=10, pady=6)
        image = load_icon(task.icon, 40)
        if image is not None:
            tk.Label(row, image=image, bg=PANEL).pack(side="left", padx=(0, 10))
        name = f"{task.name} — {task.variant}" if task.variant else task.name
        label(row, name, 13, bold=True, anchor="w").pack(side="left", fill="x", expand=True)
        if task.video is not None:
            button(row, "?", lambda: open_path(task.video), color=GREY, size=12, width=2).pack(side="right")
        button(row, "Abrir", lambda: self._open(task), size=12).pack(side="right", padx=(0, 8))
        return row

    def _open(self, task):
        def done(status, detail):
            if self.frame.winfo_exists():
                self.note.config(text=f"A última tarefa fechou com um erro: {detail}" if status == "error" else "")
        self.session.launch(task, done, guided=False)

    def show_problem(self, technical):
        self.note.config(text=technical)

    def saved(self, path):
        pass

    def destroy(self):
        self.frame.destroy()
