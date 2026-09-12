import pygame

pygame.init()

COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
COLOR_TEXT = pygame.Color('white')
FONT = pygame.font.Font(None, 32)


class InputBox:
    """A clickable, editable text field. Adapted from the InputBox pattern
    already used in Dots/incongruent/contents/textInput.py, generalized
    with an optional numeric-only filter."""

    def __init__(self, x, y, w, h, text='', numeric=False, max_len=20):
        self.rect = pygame.Rect(x, y, w, h)
        self.numeric = numeric
        self.max_len = max_len
        self.text = text
        self.active = False
        self.box_color = COLOR_INACTIVE
        self.txt_surface = FONT.render(self.text, True, COLOR_TEXT)

    def set_active(self, active):
        self.active = active
        self.box_color = COLOR_ACTIVE if active else COLOR_INACTIVE

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.set_active(self.rect.collidepoint(event.pos))
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key in (pygame.K_RETURN, pygame.K_TAB):
                pass  # advancing/submitting is handled by the screen
            elif len(self.text) < self.max_len:
                ch = event.unicode
                if ch and (ch.isdigit() if self.numeric else ch.isprintable()):
                    self.text += ch
            self.txt_surface = FONT.render(self.text, True, COLOR_TEXT)

    def draw(self, screen):
        pygame.draw.rect(screen, (30, 30, 30), self.rect)
        screen.blit(self.txt_surface, (self.rect.x + 8,
                                        self.rect.y + (self.rect.h - self.txt_surface.get_height()) // 2))
        pygame.draw.rect(screen, self.box_color, self.rect, 2)


class Button:
    """A clickable rectangle with a label; `selected` draws it highlighted
    (used for the condition toggle)."""

    def __init__(self, x, y, w, h, label, selected=False, font=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.label = label
        self.selected = selected
        self.font = font or FONT

    def clicked(self, event):
        return (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
                and self.rect.collidepoint(event.pos))

    def draw(self, screen):
        bg = (70, 130, 180) if self.selected else (50, 50, 50)
        border = (255, 255, 255) if self.selected else (150, 150, 150)
        pygame.draw.rect(screen, bg, self.rect)
        pygame.draw.rect(screen, border, self.rect, 2)
        txt = self.font.render(self.label, True, (255, 255, 255))
        screen.blit(txt, (self.rect.centerx - txt.get_width() // 2,
                           self.rect.centery - txt.get_height() // 2))
