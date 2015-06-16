#!/usr/bin/python
#===============================================================================
# Pygame || Locals || Exit
#===============================================================================
import pygame
import math
import os
from pygame.locals import *
from sys import exit

try:
    import android
except ImportError:
    android = None

#===============================================================================
# Helper Classes
#===============================================================================
from .utilities.parallax import *
from .utilities.images import *
from .utilities.strips import *
from .utilities.events import *
from .utilities.audio import *
from .gui.button import *
from .gui.toggle import *

class Engine(object):
    def __init__(self, size=(640, 480), font=None,
                 font_size= 22, color='white', FPS=32, 
				 stretch=False, stretch_size=(1024, 640)):
        pygame.init()
        pygame.display.init()
        self.debug = False
        try:
            info = pygame.display.Info()
            diag = math.hypot(info.current_w,
                              info.current_h) / android.get_dpi()

            width, height = (info.current_w, info.current_h)
            self.SW = width  / float(size[0])
            self.SH = height / float(size[1])
            self.screen = pygame.display.set_mode((width, height))

        except AttributeError:
            if not stretch:
                self.screen = pygame.display.set_mode(size)
                self.SH = 1
                self.SW = 1
            else:
                width, height = (1024, 640)
                self.SW = width  / float(size[0])
                self.SH = height / float(size[1])
                self.screen = pygame.display.set_mode((width, height))
            self.debug = True

        if android:
            android.init()
            android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)

        font_size = int((font_size*self.SW + self.SH*font_size)/2)
        if font != None and os.path.exists(font):
            font = pygame.font.Font(font, font_size)
        else:
            font = pygame.font.Font(None, font_size)

        try:
            color = pygame.color.Color(color)
        except ValueError:
            pass

        self.x      = 0
        self.y      = 0
        self.font   = font
        self.color  = color
        self.black  = pygame.color.Color('black')
        self.width  = self.screen.get_width()
        self.height = self.screen.get_height()
        self.alpha  = 255
        self.speed  = 2
        self.fin    = True
        self.fout   = False
        self.old    = pygame.Surface(self.screen.get_size())
        self.cover  = pygame.Surface(self.screen.get_size())
        self.mouse  = (0,0)
        self.touch  = False
        self.clock  = pygame.time.Clock()
        self.FPS    = FPS
        self.image  = Image()
        self.slice  = Slice()
        self.audio  = Audio()
        self.button = Button()
        self.toggle = Toggle()
        self.events = EventHandler()
        self.cover.fill((0,0,0))
        self.shade  = pygame.Surface(self.screen.get_size())
        self.shade.fill((0,0,0))
        self.shade.set_alpha(50)
        
        if android:
            if android.check_pause():
                android.wait_for_resume()

    def fill(self):
        self.screen.fill(self.color)

    def clear(self):
        self.screen.fill(self.black)
        self.events.get_events()

    def transition(self, speed, name):
        self.speed  = speed
        self.fout   = True
        self.fin    = False
        self.MENU = name

    def blit(self, img, position=(0,0), size=None):
        if not size:
            self.screen.blit(img, (position[0] * self.SW, position[1] * self.SH))
        else:
            sub = img.subsurface(0, 0, size[0]*self.SW, size[1]*self.SH)
            self.screen.blit(sub, (position[0] * self.SW, position[1] * self.SH))

    def render_strip(self, strip, position=(0,0)):
        strip.render((position[0] * self.SW, position[1] * self.SH))
        
    def render_button(self, name, position=(0,0)):
        return self.button.render(name,
                                  (position[0] * self.SW,
                                   position[1] * self.SH),
                                  self.screen, self.mouse)

    def render_toggle(self, name, position=(0,0)):
        return self.toggle.render(name,
                                  (position[0] * self.SW,
                                   position[1] * self.SH),
                                  self.screen, self.mouse)

    def get_toggle_state(self, name):
        return self.toggle.get_state(name)

    def set_toggle_state(self, name, state=False):
        return self.toggle.set_state(name, state)


    def parallax(self, img):
        return Parallax(self.screen, img, self.SW, self.SH)

    def fading(self):
        if self.fout:
            return True
        else:
            return False
        
    def update(self):
        if self.fout and self.alpha <= 0:
            self.old = self.screen.copy()
        if self.fout:
            self.blit(self.old,(0,0))
            self.alpha += self.FPS/self.speed
            self.cover.set_alpha(self.alpha)
            self.screen.blit(self.cover,(0,0))
            if self.alpha >= 255:
                self.fout = False
                self.fin  = True

        if self.fin:
            self.alpha -= self.FPS/self.speed
            self.cover.set_alpha(self.alpha)
            self.screen.blit(self.cover,(0,0))
        if self.fin and self.alpha <= 0:
            self.alpha = 0
            self.fin = False
            
        if android:
            if android.check_pause():
                android.wait_for_resume()

        if self.debug:
            if pygame.mouse.get_pressed()[0]:
                self.mouse = pygame.mouse.get_pos()
            else:
                self.mouse = (0, 0)
        else:
            self.mouse = pygame.mouse.get_pos()

        self.events.update()
        pygame.display.flip()
        self.clock.tick(self.FPS)

    def touching(self):
        return self.mouse != (0,0)

    def back(self):
        if self.events.down(K_ESCAPE):
            return True
        else:
            return False

    def stop(self):
        if self.events.down(K_ESCAPE):
            pygame.quit()
            exit()

    def quit(self):
        pygame.quit()
        exit()

    def load_sound(self, pathfile):
        return self.audio.sound("sound/" + pathfile + ".ogg")

    def play_sound(self, sound):
        self.audio.play(sound)

    def load_music(self, pathfile):
        self.audio.music("music/" + pathfile + ".ogg")
        return None
        
    def play_music(self, music=None):
        self.audio.loop()
        
    def load_image(self, pathfile, name="placeholder", alpha=True):
        self.image.load(name, pathfile, alpha)
        self.image.scale(name, self.SW, self.SH)
        return self.image.get_image(name)

    def get_image(self, name):
        return self.image.get_image(name)

    def load_strip(self, name, pathfile, quantity,
                   horizontal=True, alpha=True, seconds=0.75,
                   reverse=False, backwards=False, flip=False):

        self.slice.load(name, pathfile,
                         quantity, horizontal,
                         alpha, self.SW, self.SH)

        return Strip(self.screen, self.slice.get_strip(name),
                     seconds, reverse, backwards, flip, self.FPS)

    def load_button(self, name, folder="img/", ext=".png"):
        self.button.load(name, folder + name + ext, SW=self.SW, SH=self.SH)
        return name
        
    def load_toggle(self, name, folder="img/", ext=".png", state=True):
        self.toggle.load(name, folder + name + ext, SW=self.SW, SH=self.SH, state=state)
        return name

    def get_text(self, font, text, color="black"):
        try:
            color = pygame.color.Color(color)
        except ValueError:
            pass
        return font.render(text, 0, color)

    def get_text_border(self, text="HELLO WORLD!", font=None, color="black"):
        return Text(self, text, font, color)


    def get_font(self, name, size, ext=".ttf", folder="font/"):
        font_size = int((size * self.SW + size * self.SH) / 2.0)

        if name != None and os.path.exists(folder + name + ext):
            font = pygame.font.Font(folder + name + ext, font_size)
        else:
            font = pygame.font.Font(None, font_size)

        return font

    def loading(self, folder="img"):
        for root, directories, files in os.walk(folder):
            for filename in files:
                if filename.endswith('.png'):
                    self.load_image(os.path.join(root, filename),
                                    os.path.join(root, filename).split('.')[0].replace('\\', '/').replace(folder+'/', ''))
        return True


class Text(object):
    def __init__(self, window, text, font, color="black"):
        self.window = window
        self.color = color
        self.text = text
        self.font = font
        self.fg = self.window.get_text(self.font, self.text, self.color)
        self.bg = self.window.get_text(self.font, self.text, "black")
        self.size = self.fg.get_size()
        self.half_width = self.size[0] / 2.0 / self.window.SW

    def render(self, pos=(0, 0), center=True):
        if center:
            self.window.blit(self.fg, ((pos[0] - self.half_width), (pos[1])))
        else:
            self.window.blit(self.fg, ((pos[0]), (pos[1])))


    def render_border(self, pos=(0, 0), offset=1, center=True):
        if center:
            self.window.blit(self.bg, ((pos[0]-offset - self.half_width),
                                       (pos[1]-0)))
            self.window.blit(self.bg, ((pos[0]+offset - self.half_width),
                                       (pos[1]-0)))
            self.window.blit(self.bg, ((pos[0]-0 - self.half_width),
                                       (pos[1]-offset)))
            self.window.blit(self.bg, ((pos[0]-0 - self.half_width),
                                       (pos[1]+offset)))
            self.window.blit(self.fg, ((pos[0] - self.half_width),
                                       (pos[1])))
        else:
            self.window.blit(self.bg, ((pos[0]-offset),
                                       (pos[1]-0)))
            self.window.blit(self.bg, ((pos[0]+offset),
                                       (pos[1]-0)))
            self.window.blit(self.bg, ((pos[0]-0),
                                       (pos[1]-offset)))
            self.window.blit(self.bg, ((pos[0]-0),
                                       (pos[1]+offset)))
            self.window.blit(self.fg, ((pos[0]),
                                       (pos[1])))







