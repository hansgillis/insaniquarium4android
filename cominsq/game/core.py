import os
import json

from .menu.bubble import Bubble
from .menu.cursor import Cursor

class Factory(object):
    def __init__(self, window):
        self.window = window

        if not os.path.exists("options.json"):
            with open('options.json', 'w') as outfile:
                self.data = {"music": True}
                json.dump({"music": True}, outfile)
                self.music = True
        else:
            with open('options.json') as data_file:
                self.data = json.load(data_file)
                self.music = self.data["music"]

        with open('players.json') as data_file:
            self.players = json.load(data_file)

        self.current_player_id = self.players["player"] - 1
        self.current_player = self.players["players"][self.current_player_id]
        self.load_home()

    def load_player(self, id):
        self.players["player"] = id
        self.current_player_id = id - 1
        self.current_player = self.players["players"][id - 1]

        with open('players.json', 'w') as outfile:
            json.dump(self.players, outfile, indent=4, sort_keys=True)

    def load_loading(self):
        self._img_title_screen = self.window.get_image("loading/title_screen")
        self._img_stone = self.window.get_image("loading/stone")
        self._img_loading = self.window.get_image("loading/loading")
        self._strip_stinky = self.load_strip("loading/stinky", 10)
        self._button_press_play = self.window.load_button("loading/play")
        self._sound_button_click = self.window.load_sound("button_click")
        self._var_x = 0
        self.window.MENU = "LOADING"
        if self.music: self.window.load_music("title_screen")
        else: self.window.load_music("empty")

    def load_instructions(self):
        self._img_background = self.window.get_image("instructions/background")
        self._strip_sylv = self.load_strip("instructions/sylv", 10, seconds=2.0)
        self._object_cursor_attacking = Cursor(self.window, (300, 128))
        self._object_cursor_feeding = Cursor(self.window, (40, 100))
        self._button_continue = self.window.load_button("instructions/continue")
        self._button_menu = self.window.load_button("instructions/menu")
        self.window.transition(0.25, "INSTRUCTIONS")

    def load_home(self, music=True, instant=False):
        self._img_background = self.window.get_image("home/background")
        self._img_welcome_back = self.window.get_image("home/welcome_back")
        self._strip_merryeyes = self.load_strip("home/merryeyes", 40, seconds=5.0)
        self._button_time_trial = self.window.load_button("home/time_trial")
        self._button_start_adventure = self.window.load_button("home/start_adventure")
        self._button_challenge = self.window.load_button("home/challenge")
        self._button_hof = self.window.load_button("home/hall_of_fame")
        self._button_options = self.window.load_button("home/options")
        self._button_quit = self.window.load_button("home/quit")
        self._button_help = self.window.load_button("home/help")
        self._button_player = self.window.load_button("home/choose_player")

        self._font_dejavu_20 = self.window.get_font("dejavu", 20)

        self._text_welcome_back = self.window.get_text_border("WELCOME BACK,",
                                                              self._font_dejavu_20, (67, 72, 147))

        self._text_player = self.window.get_text_border(self.players["players"][self.current_player_id]["name"],
                                                        self._font_dejavu_20, (67, 72, 147))

        self._sound_button_click = self.window.load_sound("button_click")
        if self.music and music: self.window.load_music("main_menu_and_shop")
        if not instant:
            self.window.transition(0.5, "HOME")
        else:
            self.window.MENU = "HOME"

    def load_hall_of_fame(self):
        self._img_background = self.window.get_image("hof/background")
        self._img_template = self.window.get_image("hof/template")
        self._button_menu = self.window.load_button("hof/menu")
        self._button_adventure = self.window.load_button("hof/adventure")
        self._button_time_trial = self.window.load_button("hof/time_trial")
        self._button_challenge = self.window.load_button("hof/challenge")
        self._button_personal = self.window.load_button("hof/personal")
        self._strip_waves = self.load_strip("hof/waves", 12, False, reverse=True, seconds=1.25)
        self._sound_button_click = self.window.load_sound("button_click")

        self._img_bubbles = [self.window.get_image("hof/bubble_small"),
                             self.window.get_image("hof/bubble_medium"),
                             self.window.get_image("hof/bubble_large")]

        self._var_bubbles = [Bubble(self.window, self._img_bubbles[bubble // 5]) for bubble in range(15)]

        self._font_nirmala_bold_16 = self.window.get_font("nirmala_bold", 16)
        self._font_nirmala_bold_26 = self.window.get_font("nirmala_bold", 26)

        self._var_page = "adventure"
        self._text_adventure = self.window.get_text_border("Adventure"  , self._font_nirmala_bold_26, (255, 255, 255))
        self._text_time_trial = self.window.get_text_border("Time Trial", self._font_nirmala_bold_26, (255, 255, 255))
        self._text_challenge = self.window.get_text_border("Challenge"  , self._font_nirmala_bold_26, (255, 255, 255))
        self._text_personal = self.window.get_text_border("Personal"    , self._font_nirmala_bold_26, (255, 255, 255))
        self._text_tank1 = self.window.get_text_border("TANK 1"         , self._font_nirmala_bold_26, (255, 255, 99))
        self._text_tank2 = self.window.get_text_border("TANK 2"         , self._font_nirmala_bold_26, (255, 255, 99))
        self._text_tank3 = self.window.get_text_border("TANK 3"         , self._font_nirmala_bold_26, (255, 255, 99))
        self._text_tank4 = self.window.get_text_border("TANK 4"         , self._font_nirmala_bold_26, (255, 255, 99))

        self._var_adventure_tank1_name = [
            self.window.get_text_border(self.players["scores"]["adventure"]["tank1"][i]["name"],
                                        self._font_nirmala_bold_16, (198, 207, 239)) for i in range(5)]

        self._var_adventure_tank1_time = [
            self.window.get_text_border(self.players["scores"]["adventure"]["tank1"][i]["time"],
                                        self._font_nirmala_bold_16, (198, 207, 239)) for i in range(5)]

        self._var_adventure_tank2_name = [
            self.window.get_text_border(self.players["scores"]["adventure"]["tank2"][i]["name"],
                                        self._font_nirmala_bold_16, (198, 207, 239)) for i in range(5)]

        self._var_adventure_tank2_time = [
            self.window.get_text_border(self.players["scores"]["adventure"]["tank2"][i]["time"],
                                        self._font_nirmala_bold_16, (198, 207, 239)) for i in range(5)]

        self._var_adventure_tank3_name = [
            self.window.get_text_border(self.players["scores"]["adventure"]["tank3"][i]["name"],
                                        self._font_nirmala_bold_16, (198, 207, 239)) for i in range(5)]

        self._var_adventure_tank3_time = [
            self.window.get_text_border(self.players["scores"]["adventure"]["tank3"][i]["time"],
                                        self._font_nirmala_bold_16, (198, 207, 239)) for i in range(5)]

        self._var_adventure_tank4_name = [
            self.window.get_text_border(self.players["scores"]["adventure"]["tank4"][i]["name"],
                                        self._font_nirmala_bold_16, (198, 207, 239)) for i in range(5)]

        self._var_adventure_tank4_time = [
            self.window.get_text_border(self.players["scores"]["adventure"]["tank4"][i]["time"],
                                        self._font_nirmala_bold_16, (198, 207, 239)) for i in range(5)]

        self._var_time_trial_tank1_name = [
            self.window.get_text_border(self.players["scores"]["time_trial"]["tank1"][i]["name"],
                                        self._font_nirmala_bold_16, (198, 207, 239)) for i in range(5)]

        self._var_time_trial_tank1_score = [
            self.window.get_text_border(str(self.players["scores"]["time_trial"]["tank1"][i]["score"]),
                                        self._font_nirmala_bold_16, (198, 207, 239)) for i in range(5)]

        self._var_time_trial_tank2_name = [
            self.window.get_text_border(self.players["scores"]["time_trial"]["tank2"][i]["name"],
                                        self._font_nirmala_bold_16, (198, 207, 239)) for i in range(5)]

        self._var_time_trial_tank2_score = [
            self.window.get_text_border(str(self.players["scores"]["time_trial"]["tank2"][i]["score"]),
                                        self._font_nirmala_bold_16, (198, 207, 239)) for i in range(5)]

        self._var_time_trial_tank3_name = [
            self.window.get_text_border(self.players["scores"]["time_trial"]["tank3"][i]["name"],
                                        self._font_nirmala_bold_16, (198, 207, 239)) for i in range(5)]

        self._var_time_trial_tank3_score = [
            self.window.get_text_border(str(self.players["scores"]["time_trial"]["tank3"][i]["score"]),
                                        self._font_nirmala_bold_16, (198, 207, 239)) for i in range(5)]

        self._var_time_trial_tank4_name = [
            self.window.get_text_border(self.players["scores"]["time_trial"]["tank4"][i]["name"],
                                        self._font_nirmala_bold_16, (198, 207, 239)) for i in range(5)]

        self._var_time_trial_tank4_score = [
            self.window.get_text_border(str(self.players["scores"]["time_trial"]["tank4"][i]["score"]),
                                        self._font_nirmala_bold_16, (198, 207, 239)) for i in range(5)]

        self._var_challenge_tank1_name = [
            self.window.get_text_border(self.players["scores"]["challenge"]["tank1"][i]["name"],
                                        self._font_nirmala_bold_16, (198, 207, 239)) for i in range(5)]

        self._var_challenge_tank1_time = [
            self.window.get_text_border(self.players["scores"]["challenge"]["tank1"][i]["time"],
                                        self._font_nirmala_bold_16, (198, 207, 239)) for i in range(5)]

        self._var_challenge_tank2_name = [
            self.window.get_text_border(self.players["scores"]["challenge"]["tank2"][i]["name"],
                                        self._font_nirmala_bold_16, (198, 207, 239)) for i in range(5)]

        self._var_challenge_tank2_time = [
            self.window.get_text_border(self.players["scores"]["challenge"]["tank2"][i]["time"],
                                        self._font_nirmala_bold_16, (198, 207, 239)) for i in range(5)]

        self._var_challenge_tank3_name = [
            self.window.get_text_border(self.players["scores"]["challenge"]["tank3"][i]["name"],
                                        self._font_nirmala_bold_16, (198, 207, 239)) for i in range(5)]

        self._var_challenge_tank3_time = [
            self.window.get_text_border(self.players["scores"]["challenge"]["tank3"][i]["time"],
                                        self._font_nirmala_bold_16, (198, 207, 239)) for i in range(5)]

        self._var_challenge_tank4_name = [
            self.window.get_text_border(self.players["scores"]["challenge"]["tank4"][i]["name"],
                                        self._font_nirmala_bold_16, (198, 207, 239)) for i in range(5)]

        self._var_challenge_tank4_time = [
            self.window.get_text_border(self.players["scores"]["challenge"]["tank4"][i]["time"],
                                        self._font_nirmala_bold_16, (198, 207, 239)) for i in range(5)]


        self.window.play_sound(self._sound_button_click)
        self.window.transition(0.5, "HOF")

    def load_help(self):
        self._img_background = self.window.get_image("help/background")
        self._img_page1 = self.window.get_image("help/page1")
        self._img_page2 = self.window.get_image("help/page2")
        self._img_page3 = self.window.get_image("help/page3")
        self._img_page4 = self.window.get_image("help/page4")
        self._img_page5 = self.window.get_image("help/page5")
        self._img_page6 = self.window.get_image("help/page6")
        self._img_page7 = self.window.get_image("help/page7")
        self._img_page8 = self.window.get_image("help/page8")
        self._button_menu = self.window.load_button("help/menu")
        self._button_next = self.window.load_button("help/next")
        self._button_previous = self.window.load_button("help/previous")
        self._strip_waves = self.load_strip("help/waves", 12, False, reverse=True, seconds=1.25)
        self._sound_button_click = self.window.load_sound("button_click")
        self._var_page = 1

        self._img_bubbles = [self.window.get_image("help/bubble_small"),
                             self.window.get_image("help/bubble_medium"),
                             self.window.get_image("help/bubble_large")]

        self._var_bubbles = [Bubble(self.window, self._img_bubbles[bubble // 5]) for bubble in range(15)]


        self._strip_page_11 = self.load_strip("help/page_11", 10)
        self._strip_page_12 = self.load_strip("help/page_12", 10)
        self._strip_page_13 = self.load_strip("help/page_13", 10)
        self._strip_page_14 = self.load_strip("help/page_14", 3, seconds=5)

        self.window.play_sound(self._sound_button_click)
        self.window.transition(0.5, "HELP")

    def load_options(self):
        self._img_background = self.window.screen.copy()
        self._img_options = self.window.get_image("options/options")
        self._sound_button_click = self.window.load_sound("button_click")
        self._toggle_music = self.window.load_toggle("options/music", state=self.music)
        self._button_ok = self.window.load_button("options/ok")
        self.window.play_sound(self._sound_button_click)
        self.window.MENU = "OPTIONS"

    def load_save_slot(self):
        self._img_background = self.window.screen.copy()
        self._img_hud = self.window.get_image("save_slot/hud")
        self._button_ok = self.window.load_button("save_slot/ok")

        self._var_player_states = [True for _ in range(8)]
        self._var_player_states[self.current_player_id] = False

        self._toggle_p1 = self.window.load_toggle("save_slot/p1", state=self._var_player_states[0])
        self._toggle_p2 = self.window.load_toggle("save_slot/p2", state=self._var_player_states[1])
        self._toggle_p3 = self.window.load_toggle("save_slot/p3", state=self._var_player_states[2])
        self._toggle_p4 = self.window.load_toggle("save_slot/p4", state=self._var_player_states[3])
        self._toggle_p5 = self.window.load_toggle("save_slot/p5", state=self._var_player_states[4])
        self._toggle_p6 = self.window.load_toggle("save_slot/p6", state=self._var_player_states[5])
        self._toggle_p7 = self.window.load_toggle("save_slot/p7", state=self._var_player_states[6])
        self._toggle_p8 = self.window.load_toggle("save_slot/p8", state=self._var_player_states[7])
        self._sound_button_click = self.window.load_sound("button_click")
        self.window.play_sound(self._sound_button_click)
        self.window.MENU = "SAVE_SLOT"

    def load_strip(self, name, quantity, horizontal=True,
                   alpha=True, reverse=False, seconds=0.75,
                   backwards=False, flip = False):

        return self.window.load_strip(name,
                                      "img/" + name + ".png",
                                      quantity,
                                      horizontal,
                                      alpha,
                                      reverse=reverse,
                                      seconds=seconds,
                                      flip=flip,
                                      backwards=backwards)

    def render_loading(self):
        self.window.blit(self._img_title_screen, (0, 0))
        self.window.blit(self._img_loading, (180, 418), (min(self._var_x + 7, 250), 31))
        self.window.render_strip(self._strip_stinky, (127 + self._var_x, 388))
        self.window.blit(self._img_stone, (384, 386))
        if self._var_x < 348: self._var_x += 6
        if 332 < self._var_x:
            if self.window.render_button(self._button_press_play, (180, 418)):
                self.window.play_sound(self._sound_button_click)
                self.load_home()

    def render_instructions(self):
        self.window.blit(self._img_background, (0, 0))
        self.window.render_strip(self._strip_sylv, (240, 100))
        self._object_cursor_attacking.render(feeding=False)
        self._object_cursor_feeding.render(feeding=True)

        if self.window.render_button(self._button_menu, (524, 4)):
            self.window.play_sound(self._sound_button_click)
            self.load_home()

        if self.window.render_button(self._button_continue, (203, 406)):
            self.window.play_sound(self._sound_button_click)


    def render_home(self):
        self.window.blit(self._img_background, (0, 0))
        self.window.blit(self._img_welcome_back, (0, 0))
        self.window.render_strip(self._strip_merryeyes, (139, 196))
        self._text_welcome_back.render_border((170, 34))
        self._text_player.render_border((170, 62))

        if self.window.render_button(self._button_player, (60, 32)):
            self.load_save_slot()

        if self.window.render_button(self._button_start_adventure, (300, 40)):
            self.window.play_sound(self._sound_button_click)
            if self.players["players"][self.current_player_id]["first_time"]:
                self.load_instructions()

        if self.window.render_button(self._button_time_trial, (300, 130)):
            self.window.play_sound(self._sound_button_click)

        if self.window.render_button(self._button_challenge, (300, 200)):
            self.window.play_sound(self._sound_button_click)

        if self.window.render_button(self._button_hof, (401, 380)):
            self.load_hall_of_fame()

        if self.window.render_button(self._button_options, (326, 412)):
            self.load_options()

        if self.window.render_button(self._button_help, (420, 412)):
            self.load_help()

        if self.window.render_button(self._button_quit, (515, 412)):
            self.window.quit()

    def render_hall_of_fame(self):
        self.window.blit(self._img_background, (0, 0))
        self.window.render_strip(self._strip_waves, (0, 82))
        for bubble in self._var_bubbles: bubble.render()
        self.window.blit(self._img_template, (0, 0))

        if self._var_page != "personal":
            self._text_tank1.render_border((160, 120), 3)
            self._text_tank2.render_border((480, 120), 3)
            self._text_tank3.render_border((160, 270), 3)
            self._text_tank4.render_border((480, 270), 3)

        if self._var_page == "adventure":
            self._text_adventure.render_border((320, 45), 3)

            for i, text in enumerate(self._var_adventure_tank1_name):
                text.render_border((60, 156 + i * 20), 2, False)

            for i, text in enumerate(self._var_adventure_tank1_time):
                text.render_border((240, 156 + i * 20), 2)

            for i, text in enumerate(self._var_adventure_tank2_name):
                text.render_border((380, 156 + i * 20), 2, False)

            for i, text in enumerate(self._var_adventure_tank2_time):
                text.render_border((560, 156 + i * 20), 2)

            for i, text in enumerate(self._var_adventure_tank3_name):
                text.render_border((60, 306 + i * 20), 2, False)

            for i, text in enumerate(self._var_adventure_tank3_time):
                text.render_border((240, 306 + i * 20), 2)

            for i, text in enumerate(self._var_adventure_tank4_name):
                text.render_border((380, 306 + i * 20), 2, False)

            for i, text in enumerate(self._var_adventure_tank4_time):
                text.render_border((560, 306 + i * 20), 2)

        if self._var_page == "time_trial":
            self._text_time_trial.render_border((320, 45), 3)

            for i, text in enumerate(self._var_time_trial_tank1_name):
                text.render_border((60, 156 + i * 20), 2, False)

            for i, text in enumerate(self._var_time_trial_tank1_score):
                text.render_border((240, 156 + i * 20), 2)

            for i, text in enumerate(self._var_time_trial_tank2_name):
                text.render_border((380, 156 + i * 20), 2, False)

            for i, text in enumerate(self._var_time_trial_tank2_score):
                text.render_border((560, 156 + i * 20), 2)

            for i, text in enumerate(self._var_time_trial_tank3_name):
                text.render_border((60, 306 + i * 20), 2, False)

            for i, text in enumerate(self._var_time_trial_tank3_score):
                text.render_border((240, 306 + i * 20), 2)

            for i, text in enumerate(self._var_time_trial_tank4_name):
                text.render_border((380, 306 + i * 20), 2, False)

            for i, text in enumerate(self._var_time_trial_tank4_score):
                text.render_border((560, 306 + i * 20), 2)

        if self._var_page == "challenge":
            self._text_challenge.render_border((320, 45), 3)

            for i, text in enumerate(self._var_challenge_tank1_name):
                text.render_border((60, 156 + i * 20), 2, False)

            for i, text in enumerate(self._var_challenge_tank1_time):
                text.render_border((240, 156 + i * 20), 2)

            for i, text in enumerate(self._var_challenge_tank2_name):
                text.render_border((380, 156 + i * 20), 2, False)

            for i, text in enumerate(self._var_challenge_tank2_time):
                text.render_border((560, 156 + i * 20), 2)

            for i, text in enumerate(self._var_challenge_tank3_name):
                text.render_border((60, 306 + i * 20), 2, False)

            for i, text in enumerate(self._var_challenge_tank3_time):
                text.render_border((240, 306 + i * 20), 2)

            for i, text in enumerate(self._var_challenge_tank4_name):
                text.render_border((380, 306 + i * 20), 2, False)

            for i, text in enumerate(self._var_challenge_tank4_time):
                text.render_border((560, 306 + i * 20), 2)

        if self.window.render_button(self._button_adventure, (21, 442)):
            self.window.play_sound(self._sound_button_click)
            self._var_page = "adventure"

        if self.window.render_button(self._button_time_trial, (181, 442)):
            self.window.play_sound(self._sound_button_click)
            self._var_page = "time_trial"

        if self.window.render_button(self._button_challenge, (341, 442)):
            self.window.play_sound(self._sound_button_click)
            self._var_page = "challenge"

        if self.window.render_button(self._button_personal, (501, 442)):
            self.window.play_sound(self._sound_button_click)
            self._var_page = "personal"

        if self.window.render_button(self._button_menu, (525, 4)):
            self.window.play_sound(self._sound_button_click)
            self.load_home(False)

    def render_help(self):
        self.window.blit(self._img_background, (0, 0))
        self.window.render_strip(self._strip_waves, (0, 82))
        for bubble in self._var_bubbles: bubble.render()

        if self._var_page == 1:
            self.window.blit(self._img_page1, (0, 0))
            self.window.render_strip(self._strip_page_11, (40, 170))
            self.window.render_strip(self._strip_page_12, (40, 230))
            self.window.render_strip(self._strip_page_13, (40, 295))
            self.window.render_strip(self._strip_page_14, (40, 360))

        elif self._var_page == 2:
            self.window.blit(self._img_page2, (0, 0))

        elif self._var_page == 3:
            self.window.blit(self._img_page3, (0, 0))

        elif self._var_page == 4:
            self.window.blit(self._img_page4, (0, 0))

        elif self._var_page == 5:
            self.window.blit(self._img_page5, (0, 0))

        elif self._var_page == 6:
            self.window.blit(self._img_page6, (0, 0))

        elif self._var_page == 7:
            self.window.blit(self._img_page7, (0, 0))

        elif self._var_page == 8:
            self.window.blit(self._img_page8, (0, 0))

        if self.window.render_button(self._button_next, (331, 431)):
            self._var_page += 1
            if 8 < self._var_page:
                self._var_page = 1
            self.window.play_sound(self._sound_button_click)

        if self.window.render_button(self._button_previous, (191, 431)):
            self._var_page -= 1
            if self._var_page < 1:
                self._var_page = 8
            self.window.play_sound(self._sound_button_click)

        if self.window.render_button(self._button_menu, (526, 5)):
            self.load_home(False)
            self.window.play_sound(self._sound_button_click)

    def render_options(self):
        self.window.blit(self._img_background, (0, 0))
        self.window.blit(self._img_options, (0, 0))

        if self.window.render_toggle(self._toggle_music, (180, 140)):
            self.window.play_sound(self._sound_button_click)
            if self.window.get_toggle_state(self._toggle_music):
                with open('options.json', 'w') as data_file:
                    self.data["music"] = True
                    json.dump(self.data, data_file)
                    self.music = True
                    self.window.load_music("main_menu_and_shop")
            else:
                with open('options.json', 'w') as data_file:
                    self.data["music"] = False
                    json.dump(self.data, data_file)
                    self.music = False
                    self.window.load_music("empty")


        if self.window.render_button(self._button_ok, (180, 340)):
            self.window.play_sound(self._sound_button_click)
            self.load_home(False, True)

    def get_save_slot_states(self):
        return (
            self.window.get_toggle_state(self._toggle_p1) or
            self.window.get_toggle_state(self._toggle_p2) or
            self.window.get_toggle_state(self._toggle_p3) or
            self.window.get_toggle_state(self._toggle_p4) or
            self.window.get_toggle_state(self._toggle_p5) or
            self.window.get_toggle_state(self._toggle_p6) or
            self.window.get_toggle_state(self._toggle_p7) or
            self.window.get_toggle_state(self._toggle_p8)
        )

    def set_save_slot_states_except(self, id):
        if id != 1 : self.window.set_toggle_state(self._toggle_p1, True)
        if id != 2 : self.window.set_toggle_state(self._toggle_p2, True)
        if id != 3 : self.window.set_toggle_state(self._toggle_p3, True)
        if id != 4 : self.window.set_toggle_state(self._toggle_p4, True)
        if id != 5 : self.window.set_toggle_state(self._toggle_p5, True)
        if id != 6 : self.window.set_toggle_state(self._toggle_p6, True)
        if id != 7 : self.window.set_toggle_state(self._toggle_p7, True)
        if id != 8 : self.window.set_toggle_state(self._toggle_p8, True)

    def render_save_slot(self):
        self.window.blit(self._img_background, (0, 0))
        self.window.blit(self._img_hud, (0, 0))

        if self.window.render_toggle(self._toggle_p1, (80, 100)):
            self.window.play_sound(self._sound_button_click)
            self.window.set_toggle_state(self._toggle_p1, False)
            self.set_save_slot_states_except(1)
            self.load_player(1)

        if self.window.render_toggle(self._toggle_p2, (210, 100)):
            self.window.play_sound(self._sound_button_click)
            self.window.set_toggle_state(self._toggle_p2, False)
            self.set_save_slot_states_except(2)
            self.load_player(2)

        if self.window.render_toggle(self._toggle_p3, (340, 100)):
            self.window.play_sound(self._sound_button_click)
            self.window.set_toggle_state(self._toggle_p3, False)
            self.set_save_slot_states_except(3)
            self.load_player(3)

        if self.window.render_toggle(self._toggle_p4, (470, 100)):
            self.window.play_sound(self._sound_button_click)
            self.window.set_toggle_state(self._toggle_p4, False)
            self.set_save_slot_states_except(4)
            self.load_player(4)

        if self.window.render_toggle(self._toggle_p5, (80, 230)):
            self.window.play_sound(self._sound_button_click)
            self.window.set_toggle_state(self._toggle_p5, False)
            self.set_save_slot_states_except(5)
            self.load_player(5)

        if self.window.render_toggle(self._toggle_p6, (210, 230)):
            self.window.play_sound(self._sound_button_click)
            self.window.set_toggle_state(self._toggle_p6, False)
            self.set_save_slot_states_except(6)
            self.load_player(6)

        if self.window.render_toggle(self._toggle_p7, (340, 230)):
            self.window.play_sound(self._sound_button_click)
            self.window.set_toggle_state(self._toggle_p7, False)
            self.set_save_slot_states_except(7)
            self.load_player(7)

        if self.window.render_toggle(self._toggle_p8, (470, 230)):
            self.window.play_sound(self._sound_button_click)
            self.window.set_toggle_state(self._toggle_p8, False)
            self.set_save_slot_states_except(8)
            self.load_player(8)

        if self.window.render_button(self._button_ok, (180, 375)):
            self.window.play_sound(self._sound_button_click)
            self.load_home(False, True)















