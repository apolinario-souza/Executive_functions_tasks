import os
import subprocess
import sys


def open_video(path):
    """Opens a video file with the OS's default player, without blocking
    the task. Silently does nothing if the file is missing or can't be
    opened. Copied from Battery/contents/video.py (kept local so this task
    stays runnable on its own, without importing across sibling tasks)."""
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
