import pygame
pygame.init()
#Configuration trials
SUJ = 2
N_TRIALS = 48
PERC_SWITCHES = .5
PRESENTATION_TIME = 2500
INTERSTIMULUS = 500
FEEDBACK = 1500 #MUDAR PARA 0

#Configuration screen
screen = pygame.display.set_mode()
WIDTH, HEIGHT  = screen.get_size()

#Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

