import random

import numpy as np
import pygame

from .constants import WIDTH, HEIGHT, WHITE, PERC_SWITCHES, N_CATEGORIES
from .session import stimulus_suffix, stimulus_parts, correct_key

pygame.init()


class Target_random:
    """Draws a balanced random sequence: each of the `n_categories`
    stimulus values appears exactly `n_trial // n_categories` times."""

    def __init__(self, n_categories):
        self.n_categories = n_categories
        self.counts = [0] * n_categories
        self.response = []

    def target_control(self, n_trial):
        per_category = n_trial // self.n_categories
        for _ in range(n_trial):
            check = True
            while check:
                b = random.randint(1, self.n_categories)
                if self.counts[b - 1] < per_category:
                    self.response.append(b)
                    self.counts[b - 1] += 1
                    check = False
        return self.response


class switches:

    def switches_control(n_trial, perce, n_categories):
        checar = True
        while checar:
            sequence = Target_random(n_categories).target_control(n_trial)
            var = []
            for k in range(len(sequence) - 1):
                var.append(abs(sequence[k] - sequence[k + 1]))

            cont = 0

            for i in var:
                if i == 0:
                    cont += 1

            if cont == (n_trial * (1 - perce)):
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
        self.cont = 0  # Timer counter
        self.n_categories = N_CATEGORIES[session.condition]
        self.sequence = switches.switches_control(session.n_trials, PERC_SWITCHES, self.n_categories)

        np.savetxt(str(session.trials_dir / 'sequence.csv'), np.array(self.sequence))

        pygame.mouse.set_visible(False)

    def img(self, win, pos_x, pos_y, diameter_w, diameter_h, img_path):
        image = pygame.image.load(img_path)
        image = pygame.transform.scale(image, (diameter_h, diameter_w))
        win.blit(image, (pos_x, pos_y))

    def stimulus_image_path(self, value):
        color, suffix = stimulus_suffix(self.session.condition, value)
        return str(self.session.img_dir / f"{color}{suffix}.jpg")

    def feedback_image_path(self, value):
        """Which happy/sad image to show, based on every key pressed so
        far this trial (matches the original: the correct key wins even
        if the wrong one was also pressed at some point; nothing is shown
        until either key has been pressed)."""
        color, suffix = stimulus_suffix(self.session.condition, value)
        _, local = stimulus_parts(self.session.condition, value)
        correct = correct_key(local)
        pressed = set(self.key)
        if correct in pressed:
            mood = "Feliz"
        elif (1 - correct) in pressed:
            mood = "Triste"
        else:
            return None
        return str(self.session.img_dir / f"{color}{mood}{suffix}.jpg")

    def draw(self, win):

        if self.trial >= self.session.n_trials:
            self.finished = True
            return

        # def cont timer
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
        feedback_time = self.session.feedback_time
        stim = self.sequence[self.trial]

        # Screen 1: Holding
        if self.cont >= 0 and self.cont < interstimulus:
            win.fill(WHITE)

        # Screen 2: Stimulus
        if self.cont >= interstimulus and self.cont < interstimulus + presentation_time:
            win.fill(WHITE)
            stim_path = self.stimulus_image_path(stim)
            self.img(win, WIDTH * .05, HEIGHT * .23, WIDTH * .25, HEIGHT * 1.50, stim_path)

        # Screen 3: Feedback (happy/sad face); skipped entirely if feedback_time is 0
        feedback_start = interstimulus + presentation_time
        if feedback_time > 0 and self.cont >= feedback_start and self.cont < feedback_start + feedback_time:
            win.fill(WHITE)
            fb_path = self.feedback_image_path(stim)
            if fb_path is not None:
                self.img(win, WIDTH * .05, HEIGHT * .23, WIDTH * .25, HEIGHT * 1.50, fb_path)

        # Set all ans Save
        save_at = interstimulus + presentation_time + feedback_time
        if self.cont >= save_at + 1 and self.cont >= save_at + 1 + 50:
            win.fill(WHITE)
            names = ['Time', 'Key_press', 'Stimulus']
            time = []
            for i in range(len(self.current_time)):
                self.target.append(stim)
                time.append(5 * i)

            trial_path = self.session.trials_dir / (f"SUJ{self.session.suj}_trial{self.trial}.csv")
            np.savetxt(str(trial_path), np.column_stack([time, self.key, self.target]), header=','.join(names), delimiter=',')
            self.trial += 1
            if self.trial >= self.session.n_trials:
                self.finished = True
            # Set data
            self.current_time = []
            self.key = []
            self.target = []
