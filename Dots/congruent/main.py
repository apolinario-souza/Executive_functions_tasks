import pygame
from contents.constants import WIDTH, HEIGHT
from contents.draw import Draw

'''
“Remember, gray opposite; striped same side.”
'''

FPS = 200

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('Dots Task')

pygame.init()

with open(r"trials/legend.txt", "w") as f:
    f.write("1 = dots stripes left; 2 = dots stripes left; 3 = dots stripes right; 4 = dots stripes right \n 0 = key left; 1 = key right; -1 = no key" )


def main():
    run = True
    clock = pygame.time.Clock()
    draw = Draw(WIN)  
       

    while run:
        clock.tick(FPS)      
                                

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False  
       
        
        draw.update()                  

    
    
    pygame.quit()

main()
