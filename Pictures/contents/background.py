import pygame
from .constants import WIDTH, HEIGHT, N_TRIALS, BLACK, PERC_SWITCHES, PRESENTATION_TIME, INTERSTIMULUS 
import random

import numpy as np



pygame.init()

class Target_random:
    def __init__(self):
        self.cont1 = 0
        self.cont2 =0
        self.cont3 = 0
        self.cont4 = 0
        
        self.response = []
        
    def target_control (self, n_trial):        
        for k in range(n_trial):   
            
            check = True
            while check:
                
                b = random.randint(1,  4)           
                if b == 1 and self.cont1 < n_trial//4:
                    self.response.append(1)
                    self.cont1 +=1
                    check = False
                if b == 2 and self.cont2 < n_trial//4:
                    self.response.append(2)
                    self.cont2 +=1
                    check = False
                if b == 3 and self.cont3 < n_trial//4:
                    self.response.append(3)
                    self.cont3 +=1
                    check = False
                if b == 4 and self.cont4 < n_trial//4:
                    self.response.append(4)
                    self.cont4 +=1
                    check = False
                
                    
        return self.response

class switches:

    def switches_control (n_trial, perce):
        checar = True
        while checar:   
            sequence = Target_random().target_control(n_trial)
            var = []
            for k in range(len(sequence)-1):
                var.append(abs(sequence[k]-sequence[k+1]))

            cont = 0
    
            for i in var:
                if i == 0:
                    cont+=1;
            if cont == (n_trial*(1-perce)):
                checar = False
            
            return sequence

class Background:
    def __init__(self):
        self.clicked = False
        self.current_time = []
        self.key = []
        self.trial = 0
        self.target = []
        self.cont = 0 #Timer counter        
        self.sequence = switches.switches_control(N_TRIALS, PERC_SWITCHES) 
        
        np.savetxt('trials/sequence.csv', np.array(self.sequence))         
    
    def draw_rectangle_init (self, win):
        rect1 = pygame.Rect(0, 0, WIDTH, HEIGHT)
        rect2 = pygame.Rect(0, 0, WIDTH*.80, HEIGHT*0.4)
        rect2.center = rect1.center
        size_cross = int(WIDTH*.035)
        width = int(WIDTH*.0037)
        L1_starX = (WIDTH*.5)-size_cross ; L1_startY = HEIGHT*0.5; L1_endX =(WIDTH*.5)+size_cross; L1_endY=L1_startY; 
        L2_starX = (WIDTH*.5); L2_startY = (HEIGHT*0.5)-size_cross; L2_endX =L2_starX; L2_endY=(HEIGHT*0.5)+size_cross;
        pygame.draw.rect(win, (0, 0, 0), rect1, 2)
        pygame.draw.rect(win, (255, 255, 255), rect2)
        pygame.draw.line(win, (0, 0, 0), (L1_starX,L1_startY), (L1_endX,L1_endY),width )
        pygame.draw.line(win, (0, 0, 0), (L2_starX,L2_startY), (L2_endX,L2_endY),width )
        #pygame.draw.rect(win, (255,255,255), pygame.Rect(30, 30, 60, 60), diameter, fill)
    
    def img (self, win, pos_x, pos_y, diameter,  img):
        image = pygame.image.load(img)   
        image = pygame.transform.scale(image, (diameter, diameter)) 
        win.blit(image, (pos_x, pos_y)) 
    
    
    def text_write (self, win, text, width, height):
        base_font = pygame.font.Font(None, 32)
        text_surface = base_font.render(text, True, (255,255,255))
        win.blit(text_surface, (width, height))     
        
    def draw_button (self, win):
        win.fill(BLACK)
        self.img (win,  WIDTH*.30, 0, WIDTH*.50, "img/inicio.png")        
        if pygame.key.get_pressed()[pygame.K_SPACE] == True:
            self.clicked = True        
        
           
      
            
    def draw(self, win):    
        

        if self.clicked == True and self.trial < N_TRIALS:
            #Hide mouse 
            pygame.mouse.set_visible(False)
        
            #def cont timer
            self.current_time.append(pygame.time.get_ticks())            
            self.cont = self.current_time[-1] - self.current_time[0]
            
            if pygame.key.get_pressed()[pygame.K_RIGHT] == True:
                self.key.append(1)
            elif pygame.key.get_pressed()[pygame.K_LEFT] == True:
                self.key.append(0)
            else:
                self.key.append(-1)
                               
            
            # Screen 1: Holding 
            if self.cont >= 0 and self.cont < INTERSTIMULUS:
                win.fill(BLACK)
                self.draw_rectangle_init(win)                             
            
            # Screen 2: Stimulus 
            if self.cont >= INTERSTIMULUS and self.cont < INTERSTIMULUS+PRESENTATION_TIME:
                win.fill(BLACK)
                self.draw_rectangle_init(win)
                
                                            
               
                if self.sequence[self.trial] == 1:
                    self.img (win,  WIDTH*.10, (HEIGHT//2)-(WIDTH*.05), WIDTH*.10, "img/frog.png") #frog left
                if self.sequence[self.trial] == 2:
                    self.img (win,  WIDTH*.10, (HEIGHT//2)-(WIDTH*.05), WIDTH*.10, "img/butterfly.png") #butterfly left
                if self.sequence[self.trial] == 3:
                    self.img (win,  WIDTH*.80, (HEIGHT//2)-(WIDTH*.05), WIDTH*.10, "img/frog.png")#frog right
                if self.sequence[self.trial] == 4:
                    self.img (win,  WIDTH*.80, (HEIGHT//2)-(WIDTH*.05), WIDTH*.10, "img/butterfly.png")#butterfly right                           
                
            # Set all ans Save
            if self.cont >= INTERSTIMULUS+PRESENTATION_TIME+1 and self.cont >= INTERSTIMULUS+PRESENTATION_TIME+1+50:
                win.fill(BLACK)
                self.draw_rectangle_init(win)
                names = ['Time', 'Key_press', 'Stimulus']
                time = []
                for i in range (len(self.current_time)):
                    self.target.append(self.sequence[self.trial])
                    time.append(5*i)
                   
                np.savetxt('trials/trial_'+ str(self.trial)+'.csv', np.column_stack([time,self.key, self.target] ), header = ','.join(names), delimiter=',')
                self.trial +=1                         
                #Set data
                self.current_time = []
                self.key = []
                self.target = []         
                             
        
        else:
            
            pygame.mouse.set_visible(True)
            
            
            self.draw_button (win)
           
            
            
            
            
            
                
              
        
 
