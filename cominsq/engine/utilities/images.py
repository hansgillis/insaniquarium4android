import pygame
from pygame.locals import *

class Image(object):
    def __init__(self):
        self.images = {}

    def load(self, name, pathfile, alpha=True):
        if alpha == True:
            img = pygame.image.load(pathfile).convert_alpha()
        else:
            img = pygame.image.load(pathfile).convert()

        self.images.update({name:{"img":img, "original":img}})

    def resize(self, name, size):
        img = self.images[name]['img']
        self.images[name]['img'] = pygame.transform.scale(img, size)

    def scale(self, name, SW=1, SH=1):
        img = self.images[name]['img']
        self.images[name]['img'] = pygame.transform.scale(img,
                                        (int(img.get_width()*SW),
                                         int(img.get_height()*SH)))

    def flip(self, name, horizontal=False, vertical=False):
        img = self.images[name]['img']
        self.images[name]['img'] = pygame.transform.flip(img,
                                                         horizontal,
                                                         vertical)
        
    def reset(self, name):
        img = self.images[name]['original']
        self.images[name]['img'] = img

    def copy(self, src, dst):
        img = self.images[src]['img']
        self.images.update({dst:{"img":img, "original":img}})

    def get_image(self, name):
        return self.images[name]['img']
        
