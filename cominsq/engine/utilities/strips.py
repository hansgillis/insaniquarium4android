from __future__ import division
import pygame
from pygame.locals import *
import copy

class Slice(object):
    def __init__(self):
        self.strips = {}

    def load(self, name, pathfile, quantity, horizontal=True, alpha=True, SW=1, SH=1):
        if alpha == True:
            img = pygame.image.load(pathfile).convert_alpha()
        else:
            img = pygame.image.load(pathfile).convert()

        img = pygame.transform.scale(img, (int(img.get_width()*SW), int(img.get_height()*SH)))

        strip = []
        if horizontal:
            width = int(img.get_width() / quantity)
            height = img.get_height()
            for i in range(quantity):
                strip.append(img.subsurface((int(img.get_width() / quantity * i), 0, width, height)))

        else:
            width = img.get_width()
            height = int(img.get_height() / quantity)
            for i in range(quantity):
                strip.append(img.subsurface((0, int(img.get_height() / quantity * i), width, height)))

        self.strips.update({name: strip})
        return strip

    def get_strip(self, name):
        return self.strips[name]

#===============================================================================
# Strip Object
#===============================================================================
class Strip(object):
    def __init__(self, screen, strips, seconds=1, reverse=False, backwards=False, flip=False, FPS=32):
        self.current    = 0
        self.frame      = 0
        self.strips     = strips
        self.frames     = len(strips)

        self.FPS        = FPS / self.frames * seconds
        self.screen     = screen
        self.reloop     = False
        self.width      = self.strips[self.frame].get_width()
        self.height     = self.strips[self.frame].get_height()

        if flip:
            for i, img in enumerate(self.strips):
                self.strips[i] = pygame.transform.flip(img, True, False)

        if backwards: self.strips = self.strips[::-1]
        self.reverse    = reverse
        self.up         = True

    def EOS(self):
        if self.reloop:
            self.reloop = False
            return True
        else:
            return False

    def render(self, position=(0,0)):
        self.screen.blit(self.strips[self.frame],position)
        if not self.reverse:
            self.current += 1
            if (self.frame + 1) * self.FPS < self.current:
                self.frame += 1
                if self.frame > self.frames-1:
                    self.frame = 0
                    self.current = 0
                    self.reloop = True
            else:
                self.reloop = False
        else:
            if self.up:
                self.current += 1
                if (self.frame + 1) * self.FPS < self.current:
                    self.frame += 1
                    if self.frame > self.frames-1:
                        self.frame = self.frames-1
                        self.up = not self.up
            else:
                self.current -= 1
                if (self.frame-1) * self.FPS > self.current:
                    self.frame -= 1
                    if  self.frame - 1 < 0:
                        self.frame = 0
                        self.current = 0
                        self.up = not self.up


             

