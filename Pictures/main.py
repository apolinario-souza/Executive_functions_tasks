import pygame
from contents.constants import WIDTH, HEIGHT
from contents.draw import Draw

'''
“If you see a butterfly, press the button on the left, whether the butterfly appears on the left or right; if you see a frog, press the
button on to the right, whether the frog appears on the left of right.”
'''

FPS = 200

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('Simon effect')

pygame.init()

with open(r"trials/legend.txt", "w") as f:
    f.write("1 = frog left; 2 = butterfly left; 3 = frog right; 4 = butterfly right \n 0 = key left; 1 = key right; -1 = no key" )


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

