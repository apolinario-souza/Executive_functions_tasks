import pygame
from .constants import WIDTH, HEIGHT, BLACK, PERC_SWITCHES
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
    def __init__(self, session):
        self.session = session
        self.finished = False
        self.current_time = []
        self.key = []
        self.trial = 0
        self.target = []
        self.cont = 0 #Timer counter
        self.sequence = switches.switches_control(session.n_trials, PERC_SWITCHES)

        np.savetxt(str(session.trials_dir / 'sequence.csv'), np.array(self.sequence))

        pygame.mouse.set_visible(False)

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

    def img (self, win, pos_x, pos_y, diameter,  img):
        image = pygame.image.load(img)
        image = pygame.transform.scale(image, (diameter, diameter))
        win.blit(image, (pos_x, pos_y))

    def stimulus_image_path(self, value):
        name = {1: "down.png", 2: "downRight.png", 3: "down.png", 4: "downLeft.png"}[value]
        return str(self.session.img_dir / name)

    def draw(self, win):

        if self.trial >= self.session.n_trials:
            self.finished = True
            return

        #def cont timer
        self.current_time.append(pygame.time.get_ticks())
        self.cont = self.current_time[-1] - self.current_time[0]

        if pygame.key.get_pressed()[pygame.K_RIGHT] == True:
            self.key.append(1)
        elif pygame.key.get_pressed()[pygame.K_LEFT] == True:
            self.key.append(0)
        else:
            self.key.append(-1)

        interstimulus = self.session.interstimulus
        presentation_time = self.session.presentation_time

        # Screen 1: Holding
        if self.cont >= 0 and self.cont < interstimulus:
            win.fill(BLACK)
            self.draw_rectangle_init(win)

        # Screen 2: Stimulus
        if self.cont >= interstimulus and self.cont < interstimulus+presentation_time:
            win.fill(BLACK)
            self.draw_rectangle_init(win)

            stim = self.sequence[self.trial]
            stim_path = self.stimulus_image_path(stim)
            pos_x = WIDTH*.13 if stim in (1, 2) else WIDTH*.77
            self.img (win, pos_x, (HEIGHT//2)-(WIDTH*.05), WIDTH*.10, stim_path)

        # Set all ans Save
        if self.cont >= interstimulus+presentation_time+1 and self.cont >= interstimulus+presentation_time+1+50:
            win.fill(BLACK)
            self.draw_rectangle_init(win)
            names = ['Time', 'Key_press', 'Stimulus']
            time = []
            for i in range (len(self.current_time)):
                self.target.append(self.sequence[self.trial])
                time.append(5*i)

            trial_path = self.session.trials_dir / ('SUJ'+str(self.session.suj)+'_trial'+str(self.trial)+'.csv')
            np.savetxt(str(trial_path), np.column_stack([time,self.key, self.target] ), header = ','.join(names), delimiter=',')
            self.trial +=1
            if self.trial >= self.session.n_trials:
                self.finished = True
            #Set data
            self.current_time = []
            self.key = []
            self.target = []
