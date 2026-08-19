import os
import subprocess
import sys


def open_video(path):
    """Opens a video file with the OS's default player, without blocking
    the launcher. Silently does nothing if the file is missing or can't be
    opened."""
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
