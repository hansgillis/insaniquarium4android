from __future__ import division
import pygame
from pygame.locals import *

class Toggle(object):
    def __init__(self):
        self.buttons = {}

    def load(self, name, pathfile, quantity=2, horizontal=True, alpha=True, SW=1, SH=1, state=True):
        if alpha == True:
            img = pygame.image.load(pathfile).convert_alpha()
        else:
            img = pygame.image.load(pathfile).convert()

        img = pygame.transform.scale(img, (int(img.get_width()*SW), int(img.get_height()*SH)))

        images = []
        if horizontal:
            width = int(img.get_width() / quantity)
            height = img.get_height()
            for i in range(quantity):
                images.append(img.subsurface((int(img.get_width() / quantity * i), 0, width, height)))

        else:
            width = img.get_width()
            height = int(img.get_height() / quantity)
            for i in range(quantity):
                images.append(img.subsurface((0, int(img.get_height() / quantity * i), width, height)))

        self.buttons.update({name: {'img': images, 'state': state,
                                    'width': images[0].get_width(),
                                    'height': images[0].get_height(),
                                    'block': False}})

    def render(self, name, position, screen, mouse):
        if (position[0] < mouse[0] < position[0] + self.buttons[name]['width'] and
            position[1] < mouse[1] < position[1] + self.buttons[name]['height']):
            screen.blit(self.buttons[name]['img'][0], position)

            if self.buttons[name]['state'] != True:
                screen.blit(self.buttons[name]['img'][1], position)

            self.buttons[name]['block'] = True
            
        else:
            screen.blit(self.buttons[name]['img'][0], position)

            if self.buttons[name]['state'] != True:
                screen.blit(self.buttons[name]['img'][1], position)

            if self.buttons[name]['block']:
                self.buttons[name]['block'] = False
                self.buttons[name]['state'] = not self.buttons[name]['state']
                return True

        return False

    def get_state(self, name):
        return self.buttons[name]['state']

    def set_state(self, name, state=False):
        self.buttons[name]['state'] = state


























        
