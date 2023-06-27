import pygame
from contents.constants import WIDTH, HEIGHT
from contents.draw import Draw

'''
““I want you to push the button the arrow is pointing toward. If the arrow is on the side of the box pointing down like this
[E demonstrated] to this button, press this button. If the arrow is on the other side. If the arrow is on the other 
side pointing down like this [E demonstrated] to this button, press this button. If the
arrow is on this side, pointing down across the screen like this [E demonstrated] to this button, press this button. 
If the arrow is on the other side, pointing down across the screen like this [E demonstrated] to this button, press this button.””
'''

FPS = 200

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('Arrows Task')

pygame.init()

with open(r"trials/legend.txt", "w") as f:
    f.write("1 = arrow left; 2 = 45 right in left side; 3 = arrow right; 4 = 45 left in right side \n 0 = key left; 1 = key right; -1 = no key" )


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