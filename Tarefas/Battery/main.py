import tkinter as tk
from tkinter import messagebox


def main():
    try:
        import pygame, pandas, openpyxl  # noqa: F401 — needed by the tasks and the results spreadsheet
    except ImportError as exc:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Bateria de Funções Executivas",
                             "O programa não foi instalado corretamente neste computador.\n\n"
                             "Abra a pasta Instalar_Win e dê dois cliques em instalacao.bat.\n\n"
                             f"(Detalhe: {exc})")
        return

    from contents.launcher_screen import LauncherScreen
    LauncherScreen().run()

main()
