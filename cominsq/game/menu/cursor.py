import math

from .food import TutorialFood
from .fish import TutorialFish

class Cursor(object):
    def __init__(self, window, pos):
        self.window = window
        self.img_normal             = self.window.get_image("instructions/cursor")
        self.img_pressing           = self.window.get_image("instructions/cursor_press")

        self.strip_food             = self.load_strip("instructions/food", 10, seconds=1.0)

        self.strip_fish_turn_left   = self.load_strip("instructions/fish_turn", 10, seconds=0.001)
        self.strip_fish_turn_right  = self.load_strip("instructions/fish_turn", 10, seconds=0.001, backwards=True)

        self.strip_fish_swim_left   = self.load_strip("instructions/fish_swim", 10, seconds=1.0, flip=True)
        self.strip_fish_swim_right  = self.load_strip("instructions/fish_swim", 10, seconds=1.0)

        self.strip_fish_eat_left    = self.load_strip("instructions/fish_eat", 10, seconds=1.0, flip=True)
        self.strip_fish_eat_right   = self.load_strip("instructions/fish_eat", 10, seconds=1.0)

        self.x = pos[0]
        self.y = pos[1]
        self.moved = 0
        self.direction = 2.0
        self.animation = True
        self.is_attacking = False
        self.is_sleeping = False
        self.sleeping_time_left = 0
        self.img = self.img_normal
        self.bounds_feeding = [0, 100]
        self.bounds_attacking = [-32, 32]
        self.food = None
        self.fish = TutorialFish(self.window, self.strip_fish_turn_left,
                                 self.strip_fish_turn_right, self.strip_fish_eat_left,
                                 self.strip_fish_eat_right, self.strip_fish_swim_left,
                                 self.strip_fish_swim_right, self.x+20, self.y + 100)

    def load_strip(self, name, quantity, horizontal=True,
                   alpha=True, reverse=False, seconds=0.75,
                   backwards=False, flip=False):

        return self.window.load_strip(name,
                                      "img/" + name + ".png",
                                      quantity,
                                      horizontal,
                                      alpha,
                                      reverse=reverse,
                                      seconds=seconds,
                                      flip=flip,
                                      backwards=backwards)

    def is_waked(self):
        if 0 < self.sleeping_time_left:
            self.sleeping_time_left -= 1
            return False
        else:
            return True

    def is_idle(self):
        if 0 < self.sleeping_time_left:
            self.sleeping_time_left -= 1
            return False
        else:
            self.img = self.img_normal
            return True

    def can_attack(self):
        if 0 < self.sleeping_time_left:
            self.sleeping_time_left -= 1
            return False
        else:
            self.img = self.img_pressing
            return True

    def sleep(self, seconds=1.0):
        self.is_sleeping = True
        self.sleeping_time_left = self.window.FPS * seconds

    def instruction_feed_press(self):
        self.img = self.img_pressing
        self.sleep()
        self.animation = False

        self.food = TutorialFood(self.window, self.strip_food, self.x + self.moved,
                                 self.y , -self.bounds_feeding[1] / 2.0 + self.moved)

        self.fish.set_speed(self.food)
        if 0 < self.direction:
            self.fish.do_turn(False)
        else:
            self.fish.do_turn(True)

    def instruction_feed_release(self):
        self.img = self.img_normal

    def is_food_catched(self, food):
        if food.is_catched():
            self.animation = True
            self.direction *= -1
            self.food = None

    def instruction_attack_press(self):
        self.img = self.img_pressing
        self.sleep()
        self.animation = False

    def render(self, feeding=True):
        if self.animation:
            self.moved += self.direction

        if feeding:

            if self.fish and self.food:
                self.food.collision(self.fish)
                self.fish.collision(self.food)
                self.is_food_catched(self.food)

            if self.food:
                self.food.render()

            if self.fish:
                self.fish.render()

            if self.animation:
                if not self.bounds_feeding[0] < self.moved < self.bounds_feeding[1]:
                    self.instruction_feed_press()
                    self.moved += self.direction * (-1)
            else:
                self.instruction_feed_release()

            self.window.blit(self.img, (self.x + self.moved, self.y))

        else:
            if self.is_attacking:
                if self.is_idle():
                    self.sleep(0.25)
                    self.is_attacking = False
            else:
                if self.can_attack():
                    self.sleep(0.25)
                    self.is_attacking = True

            if not self.bounds_attacking[0] < self.moved < self.bounds_attacking[1]:
                self.direction *= -1

            if self.direction < 0:
                self.window.blit(self.img, (self.x + self.moved, self.y + 6.28 * math.cos(self.moved/2.5)))
            else:
                self.window.blit(self.img, (self.x + self.moved, self.y + 6.28 * math.sin(self.moved/2.5)))