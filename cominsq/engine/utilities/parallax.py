class Parallax(object):
    def __init__(self, screen, img, SW, SH):
        self.x      = 0
        self.y      = 0
        self.SW     = SW
        self.SH     = SH
        self.img    = img
        self.screen = screen

    def up(self, value=5):
        value *= self.SH
        self.screen.blit(self.img,(self.x,self.y))
        self.screen.blit(self.img,(self.x,self.y+self.screen.get_height()))
        if self.y - value <= -self.screen.get_height():
            self.y += self.screen.get_height()
        self.y -= value

    def down(self, value=5):
        value *= self.SH
        self.screen.blit(self.img,(self.x,self.y))
        self.screen.blit(self.img,(self.x,self.y-self.screen.get_height()))
        if self.y + value >= self.screen.get_height():
            self.y -= self.screen.get_height()
        self.y += value

    def left(self, value=5):
        value *= self.SW
        self.screen.blit(self.img,(self.x,self.y))
        self.screen.blit(self.img,(self.x+self.screen.get_width(),self.y))
        if self.x - value <= -self.screen.get_width():
            self.x += self.screen.get_width()
        self.x -= value

    def right(self, value=5):
        value *= self.SW
        self.screen.blit(self.img,(self.x,self.y))
        self.screen.blit(self.img,(self.x-self.screen.get_width(),self.y))
        if self.x + value >= self.screen.get_width():
            self.x -= self.screen.get_width()
        self.x += value

    def reset(self):
        self.x = 0
        self.y = 0
