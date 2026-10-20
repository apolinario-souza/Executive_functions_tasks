import base64
import io
import tkinter as tk

from .constants import FG, ACCENT

FONT = "Helvetica"


def label(parent, text, size=11, color=FG, bold=False, **kw):
    font = (FONT, size, "bold" if bold else "normal")
    return tk.Label(parent, text=text, bg=parent["bg"], fg=color, font=font, **kw)


def button(parent, text, command, color=ACCENT, width=None, size=11, padx=12, pady=5):
    return tk.Button(parent, text=text, command=command, bg=color, fg=FG, activebackground=color,
                     activeforeground=FG, disabledforeground="#777777", relief="flat", bd=0, cursor="hand2",
                     padx=padx, pady=pady, font=(FONT, size, "bold"), width=width, highlightthickness=0)


def entry(parent, var, width, size=12):
    return tk.Entry(parent, textvariable=var, width=width, bg="#222222", fg=FG, insertbackground=FG,
                    relief="flat", font=(FONT, size), justify="center",
                    highlightthickness=1, highlightbackground="#444444", highlightcolor=ACCENT)


_icon_cache = {}


def load_icon(icon, size=72):
    """A task's picture(s) on a white size x size tile, as a Tk image.
    `icon` is a list of image paths (wide pictures are stacked, the others
    put side by side) or "text:<chars>". Drawn with pygame, which the tasks
    already need. None if it fails. Cached, since Tk drops images nothing
    references."""
    key = (str(icon), size)
    if key in _icon_cache:
        return _icon_cache[key]
    try:
        import pygame
        pygame.font.init()
        tile = pygame.Surface((size, size))
        tile.fill((255, 255, 255))
        inner = int(size * .86)
        if isinstance(icon, str) and icon.startswith("text:"):
            text = pygame.font.Font(None, int(size * 1.1)).render(icon[5:], True, (0, 0, 0))
            tile.blit(text, ((size - text.get_width()) // 2, (size - text.get_height()) // 2))
        else:
            images = [pygame.image.load(str(p)) for p in icon]
            stacked = images[0].get_width() > images[0].get_height()
            cell = inner // len(images)
            for i, img in enumerate(images):
                w, h = img.get_size()
                box_w, box_h = (inner, cell) if stacked else (cell, inner)
                scale = min(box_w / w, box_h / h)
                img = pygame.transform.smoothscale(img, (max(1, int(w * scale)), max(1, int(h * scale))))
                x0 = (size - inner) // 2 + (0 if stacked else i * cell)
                y0 = (size - inner) // 2 + (i * cell if stacked else 0)
                tile.blit(img, (x0 + (box_w - img.get_width()) // 2, y0 + (box_h - img.get_height()) // 2))
        png = io.BytesIO()
        pygame.image.save(tile, png, "icon.png")
        _icon_cache[key] = tk.PhotoImage(data=base64.b64encode(png.getvalue()))
    except Exception:
        _icon_cache[key] = None
    return _icon_cache[key]
