#
# Wrapper for the pygame input module
#
# Copyright (C) 2009 Thadeus Burgess
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see /www.gnu.org/licenses/>

import pygame
from pygame.locals import *


class EventHandler(object):
    """
    Wrapper for the pygame input module
 
    To check a key use the pygame.locals. Such as K_a, K_d, K_ESC, etc.
    To check a mouse event use "MB1", "MB2", "MB3", etc.
    To check exit event use "QUIT"
 
    Support for up to 10 mouse buttons.
 
    Uses:
 
    Input[KEY] - Returns the pygame.event for KEY
    Input.isset(KEY) - True if there is an event for KEY
    Input.get(KEY) - Retrieve tuple of (pygame.event, status)
    Input.event(KEY) - Retrieve pygame event of key
    Input.stat(KEY) - Retrieve status value of key
    Input.down(KEY) - True if the key is a down event
    Input.motion(KEY) - True if the key is being held down
    Input.up(KEY) - True if the key is an up event
    """
    def __init__(self):
        self.mice = (MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION)
        self.butt = {1: "MB1", 2: "MB2", 3: "MB3"}
        self.events = {}
        self.mouse = (0,0)
        
        self.DOWN = 1
        self.MOTION = 2
        self.UP = 3

    def get_events(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                self.events.update({event.key: [event, self.DOWN]})
            elif event.type == KEYUP:
                self.events.update({event.key: [event, self.UP]})
            elif event.type == MOUSEBUTTONDOWN:
                self.events.update({self.butt[event.button]: [event,self.DOWN]})
            elif event.type == MOUSEBUTTONUP:
                self.events.update({self.butt[event.button]: [event,self.UP]})
            elif event.type == MOUSEMOTION:
                self.events.update({MOUSEMOTION: [event, self.MOTION]})
            elif event.type == pygame.QUIT:
                self.events.update({"QUIT": [event, True]})

        if pygame.mouse.get_pos(): self.mouse = pygame.mouse.get_pos()
        else: self.mouse = (0,0)

    def update(self):
        flag = []
        for event in self.events:
            if self.events[event][0].type == KEYDOWN:
                self.events[event][1] = self.MOTION
            elif self.events[event][0].type == KEYUP:
                flag.append(event)
            elif event == MOUSEMOTION:
                flag.append(event)
            elif event in self.butt.values():
                if event[:2] == "MB":
                    if self.down(event):
                        self.events[event][1] = self.MOTION
                    if self.up(event):
                        flag.append(event)

        for i in flag:
            del self.events[i]

    def get(self, name):
        try:event = self.events[name]
        except KeyError:event = None
        return event
    
    def stat(self, name):
        event = self.get(name)
        if event != None:status = event[1]
        else:status = None
        return status

    def isset(self, name):
        try:self.events[name];event = True
        except KeyError:event = False

        return event

    def down(self, name):
        stat = self.stat(name)
        if stat == self.DOWN:return True
        else:return False

    def motion(self, name):
        stat = self.stat(name)
        if stat == self.MOTION:return True
        else:return False

    def up(self, name):
        stat = self.stat(name)
        if stat == self.UP:return True
        else:return False
