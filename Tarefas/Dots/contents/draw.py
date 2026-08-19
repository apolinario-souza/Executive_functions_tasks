import pygame
from contents.background import Background


class Draw:
    def __init__(self, win, session):
        self.background = Background(session)
        self.win = win



    def update(self):

        self.background.draw(self.win)
        pygame.display.update()
