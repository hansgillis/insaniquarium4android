from math import sqrt

class TutorialFood(object):
    def __init__(self, window, strip, x, y, offset_x=50.0, offset_y=100, direction=1):
        self.x = x
        self.y = y
        self.moved = 0
        self.speed = 5.0
        self.strip = strip
        self.window = window
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.fish_speed = self.offset_x / (self.offset_y / self.speed) * direction
        self.catched = False

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def is_catched(self):
        return self.catched

    def collision(self, fish, radius=10):
        if sqrt((self.x - fish.moved - fish.x) ** 2) < radius:
            self.catched = True

    def get_fish_speed(self):
        self.fish_speed *= 1.314
        return self.fish_speed

    def render(self):
        self.moved += self.speed
        if not self.is_catched():
            if self.x < 50:
                self.window.render_strip(self.strip, (self.x+16, self.y + self.moved))
            else:
                self.window.render_strip(self.strip, (self.x, self.y + self.moved))

        
