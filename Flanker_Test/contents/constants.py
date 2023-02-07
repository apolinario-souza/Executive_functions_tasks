import pygame
pygame.init()
#Configuration trials
N_TRIALS = 24
PERC_SWITCHES = .5
PRESENTATION_TIME = 750
INTERSTIMULUS = 500
FEEDBACK = 500

#Configuration screen
screen = pygame.display.set_mode()
WIDTH, HEIGHT  = screen.get_size()

#Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

