import pygame
from .constants import WIDTH, HEIGHT, N_TRIALS, BLACK, PERC_SWITCHES, PRESENTATION_TIME, INTERSTIMULUS, WHITE, FEEDBACK, SUJ   
import random

import numpy as np



pygame.init()

class Target_random:
    def __init__(self):
        self.cont1 = 0
        self.cont2 =0
        self.cont3 = 0
        self.cont4 = 0
        self.cont5 = 0
        self.cont6 = 0
        self.cont7 = 0
        self.cont8 = 0
        
        self.response = []
        
    def target_control (self, n_trial):        
        for k in range(n_trial):   
            
            check = True
            while check:
                
                b = random.randint(1,  8)           
                if b == 1 and self.cont1 < n_trial//8:
                    self.response.append(1)
                    self.cont1 +=1
                    check = False
                if b == 2 and self.cont2 < n_trial//8:
                    self.response.append(2)
                    self.cont2 +=1
                    check = False
                if b == 3 and self.cont3 < n_trial//8:
                    self.response.append(3)
                    self.cont3 +=1
                    check = False
                if b == 4 and self.cont4 < n_trial//8:
                    self.response.append(4)
                    self.cont4 +=1
                    check = False
                if b == 5 and self.cont5 < n_trial//8:
                    self.response.append(5)
                    self.cont5 +=1
                    check = False
                if b == 6 and self.cont6 < n_trial//8:
                    self.response.append(6)
                    self.cont6 +=1
                    check = False
                if b == 7 and self.cont7 < n_trial//8:
                    self.response.append(7)
                    self.cont7 +=1
                    check = False
                if b == 8 and self.cont8 < n_trial//8:
                    self.response.append(8)
                    self.cont8 +=1
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
    
    
    	
    def img (self, win, pos_x, pos_y, diameter_w,diameter_h, img):
        image = pygame.image.load(img)   
        image = pygame.transform.scale(image, (diameter_h, diameter_w)) 
        win.blit(image, (pos_x, pos_y)) 
    
    
    def text_write (self, win, text, width, height):
        base_font = pygame.font.Font(None, 32)
        text_surface = base_font.render(text, True, (255,255,255))
        win.blit(text_surface, (width, height))     
        
    def draw_button (self, win):
        win.fill(BLACK)
        self.img (win,  WIDTH*.30, 0, WIDTH*.50,WIDTH*.50, "img/inicio.png")        
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
                win.fill(WHITE)
                                            
            
            # Screen 2: Stimulus 
            if self.cont >= INTERSTIMULUS and self.cont < INTERSTIMULUS+PRESENTATION_TIME:
                win.fill(WHITE)
                
                
                                            
               
                if self.sequence[self.trial] == 1:
                    self.img (win,  WIDTH*.25,HEIGHT*.32, WIDTH*.2,HEIGHT*.80, "img/rosaE.jpg") # todos esquerda
                if self.sequence[self.trial] == 2:
                    self.img (win,  WIDTH*.25, HEIGHT*.32, WIDTH*.2,HEIGHT*.80, "img/rosaED.jpg") # laterais esquerda
                if self.sequence[self.trial] == 3:
                    self.img (win,  WIDTH*.25, HEIGHT*.32, WIDTH*.2,HEIGHT*.80, "img/rosaD.jpg")# todos para direita
                if self.sequence[self.trial] == 4:
                    self.img (win,  WIDTH*.25, HEIGHT*.32, WIDTH*.2,HEIGHT*.80, "img/rosaDE.jpg")# laterais para direita
                
                if self.sequence[self.trial] == 5:
                    self.img (win,  WIDTH*.25,HEIGHT*.32, WIDTH*.2,HEIGHT*.80, "img/azulE.jpg") # all left
                if self.sequence[self.trial] == 6:
                    self.img (win,  WIDTH*.25, HEIGHT*.32, WIDTH*.2,HEIGHT*.80, "img/azulDE.jpg") # center left
                if self.sequence[self.trial] == 7:
                    self.img (win,  WIDTH*.25, HEIGHT*.32, WIDTH*.2,HEIGHT*.80, "img/azulD.jpg")# all right
                if self.sequence[self.trial] == 8:
                    self.img (win,  WIDTH*.25, HEIGHT*.32, WIDTH*.2,HEIGHT*.80, "img/azulED.jpg")# center right                           
                
            	
            		
            
            
            # Feedback           
            if self.cont >= INTERSTIMULUS+PRESENTATION_TIME and self.cont < INTERSTIMULUS+PRESENTATION_TIME+FEEDBACK:
                win.fill(WHITE)
                if self.sequence[self.trial] == 1 and (np.array(self.key) == 0).any():
                	self.img (win,  WIDTH*.25,HEIGHT*.30, WIDTH*.2,HEIGHT*.80, "img/rosaFelizE.jpg")
                if self.sequence[self.trial] == 2 and (np.array(self.key) == 0).any():
                	self.img (win,  WIDTH*.25,HEIGHT*.32, WIDTH*.2,HEIGHT*.80, "img/rosaFelizED.jpg")
                if self.sequence[self.trial] == 3 and (np.array(self.key) == 1).any():
                	self.img (win,  WIDTH*.25,HEIGHT*.32, WIDTH*.2,HEIGHT*.80, "img/rosaFelizD.jpg")
                if self.sequence[self.trial] == 4 and (np.array(self.key) == 1).any():
                	self.img (win,  WIDTH*.25,HEIGHT*.34, WIDTH*.2,HEIGHT*.80, "img/rosaFelizDE.jpg")
                
                if self.sequence[self.trial] == 5 and (np.array(self.key) == 0).any():
                	self.img (win,  WIDTH*.25,HEIGHT*.30, WIDTH*.2,HEIGHT*.80, "img/azulFelizE.jpg")
                if self.sequence[self.trial] == 6 and (np.array(self.key) == 0).any():
                	self.img (win,  WIDTH*.25,HEIGHT*.32, WIDTH*.2,HEIGHT*.80, "img/azulFelizDE.jpg")
                if self.sequence[self.trial] == 7 and (np.array(self.key) == 1).any():
                	self.img (win,  WIDTH*.25,HEIGHT*.32, WIDTH*.2,HEIGHT*.80, "img/azulFelizD.jpg")
                if self.sequence[self.trial] == 8 and (np.array(self.key) == 1).any():
                	self.img (win,  WIDTH*.25,HEIGHT*.34, WIDTH*.2,HEIGHT*.80, "img/azulFelizED.jpg")               
                	
            # Set all ans Save
            if self.cont >= INTERSTIMULUS+PRESENTATION_TIME+FEEDBACK  and self.cont < INTERSTIMULUS+PRESENTATION_TIME+FEEDBACK+50:
                
                names = ['Time', 'Key_press', 'Stimulus']
                time = []
                for i in range (len(self.current_time)):
                    self.target.append(self.sequence[self.trial])
                    time.append(5*i)
                   
                np.savetxt('trials/Suj_'+str(SUJ)+'_trial_'+ str(self.trial)+'.csv', np.column_stack([time,self.key, self.target] ), header = ','.join(names), delimiter=',')
                self.trial +=1                         
                #Set data
                self.current_time = []
                self.key = []
                self.target = []         
                             
        
        else:
            
            pygame.mouse.set_visible(True)
            
            
            self.draw_button (win)
           
            
            
            
            
            
                
              
        
 
