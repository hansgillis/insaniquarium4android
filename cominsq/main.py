import pygame
from pygame.locals import *
from engine.core import Engine
from game.core import *
from sys import exit

def main():
    window = Engine(font="assets/font/font.ttf", FPS=16)
    window.loading("img")
    game = Factory(window)
    
    while True:
        window.play_music()
        window.clear()
        window.stop()

        if window.MENU == "LOADING":
            game.render_loading()

        elif window.MENU == "HOME":
            game.render_home()

        elif window.MENU == "HELP":
            game.render_help()

        elif window.MENU == "OPTIONS":
            game.render_options()

        elif window.MENU == "SAVE_SLOT":
            game.render_save_slot()

        elif window.MENU == "HOF":
            game.render_hall_of_fame()

        elif window.MENU == "INSTRUCTIONS":
            game.render_instructions()

        window.update()

    pygame.quit()
    exit()

if __name__ == '__main__':
    main()
