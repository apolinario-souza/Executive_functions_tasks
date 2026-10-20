import json
import os
import subprocess
import sys
import tempfile
import threading
import tkinter as tk
from datetime import datetime

from .constants import RAW_FILES, RESULT_NAMES


class Session:
    """State shared by the guided and the advanced mode: the participant
    code and, for the guided mode, the summary of every task done since the
    menu opened (saved together in one spreadsheet at the end)."""

    def __init__(self, root):
        self.root = root
        self.subject = tk.StringVar(value="")
        self.results = {}  # task key -> (task, time it ended, summary dict)
        self.saved = True

    def reset(self):
        self.subject.set("")
        self.results = {}
        self.saved = True

    def would_overwrite(self, task):
        """True if this participant already has raw data of this task from
        an earlier session (a new run replaces it)."""
        if task.key in self.results:
            return False
        return os.path.exists(str(RAW_FILES[task.key]).format(suj=self.subject.get().strip()))

    def launch(self, task, on_done, guided=True, practice=False):
        """Hides the menu and runs the task's main.py. In the guided mode
        the task skips its settings screen and hands back its summary;
        on_done(status, summary_or_detail) runs on the Tk thread with
        status "saved", "practice", "stopped" or "error". In the advanced
        mode the task works on its own (settings screen and "Save as"), and
        the status is "closed" or "error"."""
        subject = self.subject.get().strip() or "1"
        cmd = [sys.executable, str(task.main), "--suj", subject] + task.args
        result_file = None
        if guided:
            fd, result_file = tempfile.mkstemp(suffix=".json", prefix="bateria_")
            os.close(fd)
            os.remove(result_file)
            cmd += ["--guided", "--result-file", result_file]
            if practice:
                cmd.append("--practice")

        outcome = {}

        def run():
            try:
                proc = subprocess.run(cmd, cwd=str(task.main.parent), stdout=subprocess.DEVNULL,
                                      stderr=subprocess.PIPE, text=True, errors="replace")
                outcome["code"], outcome["stderr"] = proc.returncode, proc.stderr
            except Exception as exc:
                outcome["code"], outcome["stderr"] = -1, str(exc)

        thread = threading.Thread(target=run, daemon=True)
        self.root.withdraw()
        thread.start()

        def wait():
            if thread.is_alive():
                self.root.after(200, wait)
                return
            self.root.deiconify()
            self.root.lift()
            self.root.focus_force()
            if outcome["code"] != 0:
                lines = [line for line in outcome["stderr"].splitlines() if line.strip()]
                on_done("error", lines[-1] if lines else f"código {outcome['code']}")
            elif not guided:
                on_done("closed", None)
            elif practice:
                on_done("practice", None)
            elif result_file and os.path.exists(result_file):
                with open(result_file, encoding="utf-8") as f:
                    summary = json.load(f)
                os.remove(result_file)
                self.results[task.key] = (task, datetime.now(), summary)
                self.saved = False
                on_done("saved", summary)
            else:
                on_done("stopped", None)

        self.root.after(200, wait)

    def default_results_name(self):
        return f"Bateria_SUJ{self.subject.get().strip()}_{datetime.now():%Y-%m-%d}.xlsx"

    def save_results(self, path):
        """One workbook: a 'Sessão' sheet with one friendly row per task,
        then one sheet per task with its full summary."""
        import pandas as pd

        rows = []
        for task, ended, summary in self.results.values():
            row = {"Participante": self.subject.get().strip(), "Tarefa": task.name,
                   "Condição": task.variant or "", "Horário": f"{ended:%d/%m/%Y %H:%M}"}
            row.update({name: summary[key] for key, name in RESULT_NAMES.items() if key in summary})
            rows.append(row)

        with pd.ExcelWriter(path, engine="openpyxl") as writer:
            pd.DataFrame(rows).to_excel(writer, sheet_name="Sessão", index=False)
            for task, ended, summary in self.results.values():
                pd.DataFrame([summary]).to_excel(writer, sheet_name=task.key, index=False)
        self.saved = True


def open_path(path):
    """Opens a file (e.g. a video) or folder with the computer's default
    program, without blocking the menu. Does nothing if it can't."""
    path = str(path)
    if not os.path.exists(path):
        return
    try:
        if hasattr(os, "startfile"):
            os.startfile(path)  # Windows
        elif sys.platform == "darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])
    except Exception:
        pass
