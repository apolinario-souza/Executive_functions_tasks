import sys
import tkinter as tk
from tkinter import filedialog, messagebox

from .constants import TITLE, ICON_FILE, BG
from .session import Session
from .advanced_view import AdvancedView
from .guided_view import GuidedView


class LauncherScreen:
    """The battery menu window. Opens in the guided mode (step by step,
    for people with little computer experience); the advanced mode
    (everything on one screen, each task with its own settings) is one
    click away. Both share the same Session, so switching keeps the
    participant code and the results of the session."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title(TITLE)
        self.root.configure(bg=BG)
        self.root.minsize(1000, 680)
        sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.geometry(f"{min(1280, sw)}x{min(760, sh - 60)}+0+0")
        try:  # open maximized
            if sys.platform.startswith("win"):
                self.root.state("zoomed")
            else:
                self.root.attributes("-zoomed", True)
        except tk.TclError:
            pass
        if sys.platform.startswith("win"):  # .ico only works on Windows
            try:
                self.root.iconbitmap(default=str(ICON_FILE))
            except tk.TclError:
                pass

        self.session = Session(self.root)
        self.view = None
        self.show_guided()
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.root.bind("<Escape>", lambda e: self.close())

    def _show(self, view_class):
        if self.view is not None:
            self.view.destroy()
        self.view = view_class(self)
        self.view.frame.pack(fill="both", expand=True)

    def show_guided(self):
        self._show(GuidedView)

    def show_advanced(self):
        self._show(AdvancedView)

    def save_results(self):
        """Asks where to save, then writes every task done in this session
        into one workbook. Returns the path, or None if cancelled or failed."""
        path = filedialog.asksaveasfilename(
            parent=self.root, title="Salvar resultados da sessão", defaultextension=".xlsx",
            filetypes=[("Planilha do Excel", "*.xlsx")], initialfile=self.session.default_results_name())
        if not path:
            return None
        try:
            self.session.save_results(path)
        except Exception as exc:
            messagebox.showerror("Salvar resultados", f"Não foi possível salvar a planilha:\n{exc}")
            return None
        self.view.saved(path)
        return path

    def close(self):
        if not self.session.saved:
            answer = messagebox.askyesnocancel(
                "Sair", "Os resultados desta sessão ainda não foram salvos.\n\n"
                        "Quer salvar agora?")
            if answer is None or (answer and not self.save_results()):
                return
        elif not messagebox.askyesno("Sair", "Fechar o programa?"):
            return
        self.view.destroy()
        self.root.destroy()

    def run(self):
        self.root.mainloop()
