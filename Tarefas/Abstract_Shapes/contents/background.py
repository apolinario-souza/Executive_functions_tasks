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
