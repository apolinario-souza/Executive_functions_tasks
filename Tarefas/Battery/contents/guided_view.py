import tkinter as tk
from pathlib import Path
from tkinter import messagebox

from .constants import TASKS, VARIANT_TEXT, VARIANT_ORDER, TITLE, FOOTER_TEXT, RESULT_NAMES, BG, PANEL, FG, MUTED, FOOTER, ACCENT, OK, WARN, ERROR, GREY
from .session import open_path
from .widgets import label, button, entry, load_icon

STEPS = ["Participante", "Escolher a tarefa", "Fazer a tarefa"]
COLUMNS = 3


def task_title(task):
    return f"{task.name} — {task.variant}" if task.variant else task.name


class GuidedView:
    """Step-by-step menu for people with little computer experience: one
    thing per screen, big text and buttons, Back/Continue at the bottom.
    Participant → task (cards, marked "FEITA" once done) → condition (only
    Dots, Abstract Shapes and Flanker) → how the task works, video,
    practice and start; after each task, go to the next one or end the
    session and save the spreadsheet."""

    def __init__(self, app):
        self.app = app
        self.session = app.session
        self.root = app.root
        self.frame = tk.Frame(self.root, bg=BG)
        self.task = None

        header = tk.Frame(self.frame, bg=BG)
        header.pack(fill="x", padx=30, pady=(14, 0))
        label(header, TITLE, 15, MUTED, bold=True).pack(side="left")
        button(header, "Modo avançado", self.app.show_advanced, color=GREY, size=10).pack(side="right")
        self.progress = tk.Frame(self.frame, bg=BG)
        self.progress.pack(fill="x", padx=30, pady=(8, 0))

        label(self.frame, FOOTER_TEXT, 9, FOOTER).pack(side="bottom", pady=6)
        self.nav = tk.Frame(self.frame, bg=BG)
        self.nav.pack(side="bottom", fill="x", padx=30, pady=(0, 10))
        self.back_btn = button(self.nav, "◀  Voltar", None, color=GREY, size=17, padx=26, pady=10)
        self.next_btn = button(self.nav, "Continuar  ▶", None, size=17, padx=26, pady=10)

        self.body = tk.Frame(self.frame, bg=BG)
        self.body.pack(fill="both", expand=True, padx=50, pady=(10, 10))

        if self.session.subject.get().strip():
            self._step_tasks()
        else:
            self._step_participant()

    def destroy(self):
        self.frame.destroy()

    # ---------- building blocks ----------

    def _clear(self, step=None):
        for child in self.body.winfo_children():
            child.destroy()
        for child in self.progress.winfo_children():
            child.destroy()
        for i, name in enumerate(STEPS):
            done, current = step is not None and i < step, i == step
            color = FG if current else (OK if done else "#555555")
            label(self.progress, f"{i + 1}  {name}", 13, color, bold=current).pack(side="left", padx=(0, 6))
            if i < len(STEPS) - 1:
                label(self.progress, "›", 13, "#555555").pack(side="left", padx=(0, 6))
        self._nav()

    def _nav(self, back=None, forward=None, forward_text="Continuar  ▶", forward_color=ACCENT):
        self.back_btn.pack_forget()
        self.next_btn.pack_forget()
        if back:
            self.back_btn.config(command=back)
            self.back_btn.pack(side="left")
        if forward:
            self.next_btn.config(command=forward, text=forward_text, bg=forward_color,
                                 activebackground=forward_color, state="normal")
            self.next_btn.pack(side="right")

    def _title(self, text, subtitle=None):
        label(self.body, text, 28, bold=True, anchor="w").pack(fill="x")
        if subtitle:
            label(self.body, subtitle, 16, MUTED, anchor="w", justify="left", wraplength=1150).pack(
                fill="x", pady=(6, 0))

    def _task_title(self, text):
        row = tk.Frame(self.body, bg=BG)
        row.pack(fill="x", pady=(0, 14))
        image = load_icon(self.task.icon, 64)
        if image is not None:
            tk.Label(row, image=image, bg=BG).pack(side="left", padx=(0, 16))
        label(row, text, 28, bold=True).pack(side="left")

    def _steps_list(self, parent, lines):
        for i, line in enumerate(lines, start=1):
            row = tk.Frame(parent, bg=parent["bg"])
            row.pack(fill="x", pady=5)
            label(row, f"{i}.", 16, ACCENT, bold=True).pack(side="left", anchor="n")
            label(row, line, 16, anchor="w", justify="left", wraplength=1000).pack(side="left", padx=(8, 0))

    def _big_button(self, parent, text, command, color=ACCENT, size=18):
        return button(parent, text, command, color=color, size=size, padx=30, pady=14)

    # ---------- 1. participant ----------

    def _step_participant(self):
        self._clear(0)
        self._title("Quem vai fazer as tarefas?", "Digite o código do participante e clique em Continuar.")
        box = tk.Frame(self.body, bg=BG)
        box.pack(anchor="w", pady=40)
        field = entry(box, self.session.subject, 8, size=34)
        field.pack(side="left", ipady=8)
        field.focus_set()
        field.icursor("end")
        error = label(self.body, "", 15, ERROR, anchor="w")
        error.pack(fill="x")

        def forward():
            if not self.session.subject.get().strip():
                error.config(text="Digite o código do participante antes de continuar.")
                field.focus_set()
                return
            self._step_tasks()

        field.bind("<Return>", lambda e: forward())
        if self.session.results:
            # The tasks already done belong to this participant
            field.config(state="readonly", readonlybackground="#222222")
            label(self.body, "Para trocar de participante, termine esta sessão e comece uma nova.",
                  14, WARN, anchor="w", justify="left", wraplength=1100).pack(fill="x", pady=(10, 0))
        self._nav(forward=forward)

    # ---------- 2. task ----------

    def _groups(self):
        """The tasks as the menu shows them: one entry per task name, with
        its conditions (e.g. Dots: Congruente, Incongruente, Mista)."""
        groups = {}
        for task in TASKS:
            groups.setdefault(task.name, []).append(task)
        return list(groups.values())

    def _step_tasks(self):
        self._clear(1)
        n = len(self.session.results)
        done = f"  Já feitas: {n} de {len(TASKS)}, contando cada condição." if n else ""
        self._title(f"Participante {self.session.subject.get().strip()}: escolha a tarefa",
                    "Clique na tarefa que o participante vai fazer agora." + done)
        grid = tk.Frame(self.body, bg=BG)
        grid.pack(fill="x", pady=(14, 0))
        for i, group in enumerate(self._groups()):
            n_done = sum(task.key in self.session.results for task in group)
            if len(group) == 1:
                status = "FEITA" if n_done else ""
                subtitle, open_it = "", lambda g=group: self._choose(g[0])
            else:
                status = f"{n_done} de {len(group)} feitas" if n_done else ""
                subtitle = f"{len(group)} condições"
                open_it = lambda g=group: self._step_variants(g)
            # the picture of the condition that shows the most (e.g. Dots-Mista: both circles)
            icon = max(group, key=lambda task: len(task.icon) if isinstance(task.icon, list) else 1).icon
            grid.columnconfigure(i % COLUMNS, weight=1, uniform="card")
            self._card(grid, icon, group[0].name, subtitle, status, n_done == len(group), open_it).grid(
                row=i // COLUMNS, column=i % COLUMNS, sticky="nsew", padx=8, pady=8)
        self._nav(back=self._step_participant, forward=self._screen_end,
                  forward_text="Terminar a sessão", forward_color=GREY)

    def _step_variants(self, group):
        """Extra page for tasks with more than one condition."""
        self._clear(1)
        row = tk.Frame(self.body, bg=BG)
        row.pack(fill="x", pady=(0, 6))
        image = load_icon(group[-1].icon, 64)
        if image is not None:
            tk.Label(row, image=image, bg=BG).pack(side="left", padx=(0, 16))
        label(row, f"{group[0].name}: escolha a condição", 28, bold=True).pack(side="left")
        order = VARIANT_ORDER.get(group[0].name)
        label(self.body, "Clique na condição que o participante vai fazer agora." + (f"\n{order}" if order else ""),
              16, MUTED, anchor="w", justify="left", wraplength=1150).pack(fill="x", pady=(0, 10))
        grid = tk.Frame(self.body, bg=BG)
        grid.pack(fill="x", pady=(10, 0))
        for i, task in enumerate(group):
            done = task.key in self.session.results
            grid.columnconfigure(i, weight=1, uniform="variant")
            self._card(grid, task.icon, task.variant, VARIANT_TEXT.get(task.key, ""), "FEITA" if done else "",
                       done, lambda t=task: self._choose(t), size=72, wrap=280).grid(
                row=0, column=i, sticky="nsew", padx=8, pady=8)
        self._nav(back=self._step_tasks)

    def _card(self, parent, icon, title, subtitle, status, done, command, size=64, wrap=220):
        color = OK if done else PANEL
        card = tk.Frame(parent, bg=PANEL, cursor="hand2", highlightthickness=3,
                        highlightbackground=color, padx=12, pady=10)
        parts = [card]
        image = load_icon(icon, size)
        if image is not None:
            picture = tk.Label(card, image=image, bg=PANEL, cursor="hand2")
            picture.pack(side="left", padx=(0, 12), anchor="n")
            parts.append(picture)
        text = tk.Frame(card, bg=PANEL, cursor="hand2")
        text.pack(side="left", fill="x", expand=True)
        parts.append(text)
        for line in (label(text, title, 17, bold=True, anchor="w", cursor="hand2"),
                     label(text, subtitle or " ", 13, MUTED, anchor="w", justify="left", wraplength=wrap,
                           cursor="hand2"),
                     label(text, status or " ", 13, OK, bold=True, anchor="w", cursor="hand2")):
            line.pack(fill="x")
            parts.append(line)

        def hover(on):
            card.config(highlightbackground=ACCENT if on else color)

        for part in parts:
            part.bind("<Button-1>", lambda e: command())
            part.bind("<Enter>", lambda e: hover(True))
            part.bind("<Leave>", lambda e: hover(False))
        return card

    def _choose(self, task):
        self.task = task
        self._step_run()

    def _back_from_task(self):
        """From a task's page back to where it was picked: its conditions
        page, or the task list."""
        group = next(g for g in self._groups() if self.task in g)
        if len(group) > 1:
            self._step_variants(group)
        else:
            self._step_tasks()

    # ---------- 3. how it works, practice, start ----------

    def _step_run(self, note=None, note_color=OK):
        self._clear(2)
        task = self.task
        self._task_title(task_title(task))

        box = tk.Frame(self.body, bg=PANEL, padx=18, pady=10)
        box.pack(fill="x", pady=(0, 14))
        label(box, "Como é a tarefa", 15, ACCENT, bold=True, anchor="w").pack(fill="x")
        label(box, task.rule, 15, anchor="w", justify="left", wraplength=1100).pack(fill="x")

        steps = []
        if task.video is not None:
            steps.append("Assista ao vídeo de instruções junto com o participante.")
        steps += ["Faça o treino: são poucas tentativas, só para praticar (não contam no resultado).",
                  "Quando o participante tiver entendido, clique em \"COMEÇAR A TAREFA\".",
                  "Na tela preta com a explicação, aperte a BARRA DE ESPAÇO para começar."]
        self._steps_list(self.body, steps)

        actions = tk.Frame(self.body, bg=BG)
        actions.pack(anchor="w", pady=(18, 0))
        if task.video is not None:
            self._big_button(actions, "▶  Ver o vídeo", lambda: open_path(task.video), color=GREY,
                             size=15).pack(side="left", padx=(0, 14))
        self._big_button(actions, "Treinar", self._practice, color=GREY, size=15).pack(side="left", padx=(0, 14))
        if note:
            label(actions, note, 15, note_color, bold=True).pack(side="left", padx=(10, 0))

        label(self.body, "Para parar a tarefa no meio, aperte a tecla ESC.", 15, WARN, anchor="w").pack(
            fill="x", pady=(18, 0))
        self._nav(back=self._back_from_task, forward=self._start, forward_text="▶  COMEÇAR A TAREFA",
                  forward_color=OK)

    def _practice(self):
        def done(status, detail):
            if status == "error":
                self._show_problem_screen(detail)
            elif status == "practice":
                self._step_run("Treino feito. Pode treinar de novo ou começar.")
            else:
                self._step_run("O treino foi interrompido.", WARN)
        self.session.launch(self.task, done, practice=True)

    def _start(self):
        task, s = self.task, self.session
        if task.key in s.results and not messagebox.askyesno(
                task_title(task), "Esta tarefa já foi feita nesta sessão.\n\n"
                                  "Se fizer de novo, o resultado anterior será trocado pelo novo.\nContinuar?"):
            return
        if s.would_overwrite(task) and not messagebox.askyesno(
                task_title(task), f"O participante {s.subject.get().strip()} já fez esta tarefa em uma sessão "
                                  "anterior.\n\nSe continuar, os dados anteriores serão trocados pelos novos.\n"
                                  "Continuar?"):
            return

        def done(status, detail):
            if status == "error":
                self._show_problem_screen(detail)
            elif status == "stopped":
                self._step_run("A tarefa foi interrompida antes do fim. Nada foi guardado.", WARN)
            else:
                self._screen_result(detail)
        s.launch(task, done)

    # ---------- after a task ----------

    def _next_task(self):
        """The first task after the current one (in menu order) not done yet."""
        start = TASKS.index(self.task) + 1
        for task in TASKS[start:] + TASKS[:start]:
            if task.key not in self.session.results:
                return task
        return None

    def _screen_result(self, summary):
        self._clear()
        self._task_title("Tarefa terminada!")
        shown = [(name, summary[key]) for key, name in RESULT_NAMES.items() if key in summary]
        if shown:
            row = tk.Frame(self.body, bg=BG)
            row.pack(anchor="w", pady=10)
            for name, value in shown:
                box = tk.Frame(row, bg=PANEL, padx=30, pady=14)
                box.pack(side="left", padx=(0, 14))
                label(box, name, 14, MUTED).pack()
                if isinstance(value, float):
                    value = "—" if value != value else f"{value:g}"  # NaN: nothing to compute it from
                label(box, f"{value}", 30, bold=True).pack()
        label(self.body, "O resultado foi guardado. No fim da sessão você salva tudo de uma vez.",
              15, MUTED, anchor="w").pack(fill="x", pady=(10, 0))

        choices = tk.Frame(self.body, bg=BG)
        choices.pack(anchor="w", pady=30)
        following = self._next_task()
        if following is not None:
            self._big_button(choices, f"Próxima tarefa: {task_title(following)}",
                             lambda: self._choose(following), color=OK).pack(side="left", padx=(0, 14))
        self._big_button(choices, "Escolher outra tarefa", self._step_tasks).pack(side="left", padx=(0, 14))
        self._big_button(choices, "Terminar a sessão", self._screen_end, color=GREY).pack(side="left")

    def _show_problem_screen(self, detail):
        self._clear()
        self._title("Algo deu errado", "A tarefa fechou por um problema. Tente de novo. "
                                       "Se continuar, chame o responsável técnico.")
        label(self.body, f"(Detalhe: {detail})", 12, MUTED, anchor="w", justify="left", wraplength=1100).pack(
            fill="x", pady=(10, 0))
        self._big_button(self.body, "Voltar", self._step_run if self.task else self._step_tasks).pack(
            anchor="w", pady=30)

    # ---------- end of session ----------

    def _screen_end(self):
        self._clear()
        n = len(self.session.results)
        if n == 0:
            self._title("Fim da sessão", "Nenhuma tarefa foi feita nesta sessão, então não há resultados para salvar.")
            choices = tk.Frame(self.body, bg=BG)
            choices.pack(anchor="w", pady=30)
            self._big_button(choices, "Voltar às tarefas", self._step_tasks).pack(side="left", padx=(0, 14))
            self._big_button(choices, "Fechar o programa", self.app.close, color=GREY).pack(side="left")
            return

        self._title("Fim da sessão: salvar os resultados",
                    f"Nesta sessão foram feitas {n} {'tarefa' if n == 1 else 'tarefas'}. "
                    "Agora vamos guardar todos os resultados em uma planilha.")
        box = tk.Frame(self.body, bg=BG)
        box.pack(fill="x", pady=(20, 0))
        self._steps_list(box, [
            "Clique no botão \"Salvar resultados\" aqui embaixo.",
            "Vai abrir uma janela do computador. Escolha a pasta onde guardar (por exemplo, Documentos).",
            "O nome do arquivo já vem preenchido. Clique no botão \"Salvar\" da janela.",
        ])
        self._big_button(self.body, "Salvar resultados", self._save, color=OK, size=20).pack(anchor="w", pady=26)
        self._nav(back=self._step_tasks)

    def _save(self):
        path = self.app.save_results()
        if path:
            self._screen_saved(path)

    def saved(self, path):
        pass  # the guided flow shows its own screen (_screen_saved)

    def _screen_saved(self, path):
        self._clear()
        self._title("Resultados salvos!")
        label(self.body, "A planilha foi guardada em:", 16, MUTED, anchor="w").pack(fill="x", pady=(16, 0))
        label(self.body, path, 16, bold=True, anchor="w", wraplength=1150, justify="left").pack(fill="x")
        choices = tk.Frame(self.body, bg=BG)
        choices.pack(anchor="w", pady=30)
        self._big_button(choices, "Abrir a pasta", lambda: open_path(Path(path).parent), color=GREY).pack(
            side="left", padx=(0, 14))
        self._big_button(choices, "Começar nova sessão", self._new_session).pack(side="left", padx=(0, 14))
        self._big_button(choices, "Fechar o programa", self.app.close, color=GREY).pack(side="left")

    def _new_session(self):
        self.session.reset()
        self.task = None
        self._step_participant()
