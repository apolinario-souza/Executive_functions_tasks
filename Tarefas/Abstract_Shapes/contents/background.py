import pygame
from .constants import WIDTH, HEIGHT, BLACK, PERC_SWITCHES
import random

import numpy as np



pygame.init()

class Target_random:
    def __init__(self, n_shapes):
        self.n_shapes = n_shapes
        self.counts = {i: 0 for i in range(1, n_shapes + 1)}

        self.response = []

    def target_control (self, n_trial):
        per_shape = n_trial // self.n_shapes
        for k in range(n_trial):

            check = True
            while check:

                b = random.randint(1, self.n_shapes)
                if self.counts[b] < per_shape:
                    self.response.append(b)
                    self.counts[b] += 1
                    check = False



        return self.response
class switches:

    def switches_control (n_trial, perce, n_shapes):
        checar = True
        while checar:
            sequence = Target_random(n_shapes).target_control(n_trial)
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

_IMAGE_CACHE = {}  # (path, size) -> scaled image, see Background.img


class Background:
    def __init__(self, session):
        self.session = session
        self.finished = False
        self.current_time = []
        self.key = []
        self.trial = 0
        self.target = []
        self.cont = 0 #Timer counter
        self.sequence = switches.switches_control(session.n_trials, PERC_SWITCHES, session.n_shapes)

        np.savetxt(str(session.trials_dir / 'sequence.csv'), np.array(self.sequence))

        pygame.mouse.set_visible(False)

    def draw_rectangle_init (self, win):
        rect1 = pygame.Rect(0, 0, WIDTH, HEIGHT)
        rect2 = pygame.Rect(0, 0, WIDTH*.80, HEIGHT*0.4)
        rect2.center = rect1.center
        pygame.draw.rect(win, (0, 0, 0), rect1, 2)
        pygame.draw.rect(win, (255, 255, 255), rect2)


    def img (self, win, pos_x, pos_y, diameter,  img):
        # Loaded and scaled once, not on every frame, so frames stay short
        # and the recorded times stay precise
        key = (img, diameter)
        if key not in _IMAGE_CACHE:
            _IMAGE_CACHE[key] = pygame.transform.scale(pygame.image.load(img), (diameter, diameter))
        win.blit(_IMAGE_CACHE[key], (pos_x, pos_y))

    def stimulus_image_path (self, value):
        half = self.session.n_shapes // 2
        if value <= half:
            return str(self.session.img_dir / f"left{value}.png")
        return str(self.session.img_dir / f"right{value - half}.png")


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

            stim_path = self.stimulus_image_path(self.sequence[self.trial])
            self.img (win,  WIDTH*.45, (HEIGHT//2)-(WIDTH*.05), WIDTH*.10, stim_path)

        # Set all ans Save
        if self.cont >= interstimulus+presentation_time+1 and self.cont >= interstimulus+presentation_time+1+50:
            win.fill(BLACK)
            self.draw_rectangle_init(win)
            names = ['Time', 'Key_press', 'Stimulus']
            time = []
            for i in range (len(self.current_time)):
                self.target.append(self.sequence[self.trial])
                time.append(self.current_time[i] - self.current_time[0])  # real ms since the trial began

            trial_path = self.session.trials_dir / ('SUJ'+str(self.session.suj)+'_trial'+str(self.trial)+'.csv')
            np.savetxt(str(trial_path), np.column_stack([time,self.key, self.target] ), header = ','.join(names), delimiter=',')
            self.trial +=1
            if self.trial >= self.session.n_trials:
                self.finished = True
            #Set data
            self.current_time = []
            self.key = []
            self.target = []
