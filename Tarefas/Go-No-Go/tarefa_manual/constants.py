import pygame
pygame.init()
#Configuration trials
SUJ = 1
N_TRIALS = 20
PERC_6 = .15  # % das tentativas devem ser o número 6
LIM_TIME = 750 #Tempo limite para resposta
INTERSTIMULUS = 500 #intervalor entre os estimulos

#Configuration screen
screen = pygame.display.set_mode()
WIDTH, HEIGHT  = screen.get_size()

#Colors
BLACK = (0, 0, 0)

