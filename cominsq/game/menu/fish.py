from math import sqrt

class TutorialFish(object):
    def __init__(self, window, ftl, ftr, fel, fer, fsl, fsr, x, y):
        self.x = x
        self.y = y
        self.moved = 0
        self.speed = 5.0
        self.window = window
        self.speed = 0
        self.ftl = ftl
        self.ftr = ftr
        self.fel = fel
        self.fer = fer
        self.fsl = fsl
        self.fsr = fsr
        self.strip = self.fsl
        self.turn = False
        self.eating = False

    def get_speed(self, food):
        return self.speed

    def set_speed(self, food):
        self.speed = food.get_fish_speed()

    def do_turn(self, right=True):
        if right:
            self.strip = self.ftr
        else:
            self.strip = self.ftl
        self.turn = True

    def collision(self, food, radius=10):
        if sqrt((self.x + self.moved - food.x) ** 2) < radius:
            if self.speed < 0:
                self.strip = self.fel
                self.turn = False
                self.speed = 0
            else:
                self.strip = self.fer
                self.turn = False
                self.speed = 0
            self.eating = True

    def render(self):
        self.moved += self.speed
        if self.turn:
            if self.strip.EOS():

                if self.speed < 0:
                    self.strip = self.fsl
                else:
                    self.strip = self.fsr

                self.turn = False

        if self.eating and self.strip.EOS():
            self.eating = False
            if 10 < self.moved:
                self.strip = self.fsr
            else:
                self.strip = self.fsl

        self.window.render_strip(self.strip, (self.x + self.moved, self.y))
