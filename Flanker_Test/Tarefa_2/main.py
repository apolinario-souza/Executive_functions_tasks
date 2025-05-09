import pygame
from contents.constants import WIDTH, HEIGHT
from contents.draw import Draw



FPS = 200

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('Simon effect')

pygame.init()

with open(r"trials/legend.txt", "w") as f:
    f.write("1 = todos para esq.; 2 = laterais esquerda; 3 = todos para direita; 4 = laterais para esquerda \n 0 = key left; 1 = key right; -1 = no key" )


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

