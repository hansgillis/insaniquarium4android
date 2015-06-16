import random

class Bubble(object):
    def __init__(self, window, img):
        self.window = window
        self.img = img
        self.randomize()

    def randomize(self):
        self.x = random.randint(32, self.window.width-32)
        self.y = random.randint(self.window.height+32, self.window.height+321)

    def render(self):
        self.y -= 8.25
        self.x += random.randint(-1, 1)
        if self.y < 92:
            self.randomize()
        else:
            self.window.blit(self.img, (self.x, self.y))