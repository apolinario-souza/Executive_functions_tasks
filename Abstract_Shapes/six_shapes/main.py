import pygame
from contents.constants import WIDTH, HEIGHT
from contents.draw import Draw

'''
“for this one press the left button”; “for this one press right”
'''

FPS = 200

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('Abstract Shapes Task')

pygame.init()

with open(r"trials/legend.txt", "w") as f:
    f.write("1 = shape left 1; 2 = shape left 2; 3 = shape left 3; 4 = shape right1; 5 = shape right2; 6 = shape right3 \n 0 = key left; 1 = key right; -1 = no key" )


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
