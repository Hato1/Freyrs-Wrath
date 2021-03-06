import os
import math
import time

import pygame as pg

# from pygame.compat import geterror
from pygame.locals import *

import helper
from helper import (
    load_sound,
    load_music,
    DATA_DIR,
    load_all_images,
    WIN_SIZE,
    LOADED_IMAGES,
)
from world import World
from entity import Entity

if not pg.font:
    print("Warning, fonts disabled")
if not pg.mixer:
    print("Warning, sound disabled")

MENU = 1
GAME = 2
END = 3
SELECT = 4
GAME_STATE = MENU

WHITE = (255, 255, 255)
GREY = (122, 122, 122)
GREEN = (20, 239, 20)
BLACK = (0, 0, 0)

GAME_NAME = "Freyr's Wrath"
XBOX360 = {"A": 0, "B": 1, "X": 2, "Y": 3, "LB": 4, "RB": 5}
P1DIRS = {
    pg.K_w: "UP",
    pg.K_s: "DOWN",
    pg.K_a: "LEFT",
    pg.K_d: "RIGHT",
    pg.K_f: "MORE",
    pg.K_g: "SPEED",
    pg.K_h: "HEAL",
}
P2DIRS = {
    pg.K_UP: "UP",
    pg.K_DOWN: "DOWN",
    pg.K_LEFT: "LEFT",
    pg.K_RIGHT: "RIGHT",
    pg.K_k: "MORE",
    pg.K_l: "SPEED",
    pg.K_SEMICOLON: "HEAL",
}
pg.init()
joysticks = [pg.joystick.Joystick(x) for x in range(pg.joystick.get_count())]

# TODO
# Store sounds and fonts in dictionary created by helper.py
# Draw PIT on title background
# Cut off empty end end of fishing.wav or make it a full bar if it breaks looping of title screen background in sync with music


class Game:
    def __init__(self, state=MENU):
        self.game_state = state
        self.background_surface = None  # init in setup_game
        self.screen = None  # init in setup_game
        self.button_sound = None
        self.victory_sound = None
        self.select_sound = None
        self.number_of_players = 2
        self.themes = ["VIKING", "PRIEST", "FARMER", "DEMON"]
        self.menu_theme = 0  # Set to viking for scrolling_menu_background
        self.players = []
        self.setup_game()

    def create_scrolling_menu_background(self):
        bg = helper.create_background(self.themes[self.menu_theme], helper.WIN_SIZE)
        return Entity(bg, (0, 0))

    def setup_game(self):
        self.screen = pg.display.set_mode(WIN_SIZE, pg.SCALED | pg.RESIZABLE)
        load_all_images()
        pg.display.set_icon(LOADED_IMAGES["sprite_viking_front"])
        pg.display.set_caption(GAME_NAME)
        self.scrolling_menu_background = self.create_scrolling_menu_background()
        self.initialize_menu_background()

        self.button_sound = load_sound("button_sound.wav")
        self.button_sound.set_volume(0.5)

        self.victory_sound = load_sound("victory.wav")
        self.victory_sound.set_volume(0.3)

        self.select_sound = load_sound("select_sound.wav")
        self.select_sound.set_volume(0.3)

        load_music("Fishing_Song.wav")
        # pg.mixer.music.load(load_music("Fishing_Song.wav"))
        pg.mixer.music.set_volume(0.2)
        pg.mixer.music.play(-1)

    def initialize_menu_background(self):
        # Create The Menu
        self.background_surface = pg.Surface(self.screen.get_size())
        self.background_surface = self.background_surface.convert()
        self.background_surface.fill(WHITE)
        self.scrolling_menu_background.draw(
            self.background_surface, self.background_surface.get_size()
        )
        self.write_menu_text()

    def write_menu_text(self):
        font_title = pg.font.Font(os.path.join(DATA_DIR, "Amatic-Bold.ttf"), 36 * 3)
        text_title = font_title.render(GAME_NAME, 1, (220, 20, 60))
        text_title = pg.transform.rotate(text_title, math.sin(time.time() / 1.5) * 10)
        text_title = pg.transform.scale(
            text_title,
            (
                text_title.get_width() + int(math.sin(time.time() / 1) * 20),
                text_title.get_height() + int(math.sin(time.time() / 1) * 20),
            ),
        )
        textpos_title = text_title.get_rect(
            centerx=self.background_surface.get_width() / 2,
            centery=self.background_surface.get_height() / 5,
        )

        self.background_surface.blit(text_title, textpos_title)

        font_team = pg.font.Font(os.path.join(DATA_DIR, "Amatic-Bold.ttf"), 12 * 3)
        text_team = font_team.render("Team Fishing Minigame Metaphor", 1, (220, 20, 60))
        textpos_team = text_team.get_rect(
            centerx=self.background_surface.get_width() / 2,
            centery=self.background_surface.get_height() / 1.8,
        )
        self.background_surface.blit(text_team, textpos_team)

        self.draw_number_players_selector()

        text_by = font_team.render("by", 1, (220, 20, 60))
        textpos_by = text_by.get_rect(
            centerx=self.background_surface.get_width() / 2,
            centery=self.background_surface.get_height() / 2.2,
        )
        self.background_surface.blit(text_by, textpos_by)

        font_space_to_begin = pg.font.Font(
            os.path.join(DATA_DIR, "AmaticSC-Regular.ttf"), 16 * 3
        )
        text_space_to_begin = font_space_to_begin.render(
            "Press Spacebar to Start", 1, (220, 20, 60)
        )
        textpos_space_to_begin = text_space_to_begin.get_rect(
            centerx=self.background_surface.get_width() / 2,
            centery=self.background_surface.get_height() / 1.2,
        )
        self.background_surface.blit(text_space_to_begin, textpos_space_to_begin)

    def draw_number_players_selector(self):
        font_number_of_players = pg.font.Font(
            os.path.join(DATA_DIR, "Amatic-Bold.ttf"), 20 * 3
        )

        number_players_string = "  Number of players:  "
        if self.number_of_players > 2:
            number_players_string += "< "
        else:
            number_players_string += "   "
        number_players_string += str(self.number_of_players)
        if self.number_of_players < 4:
            number_players_string += " >"
        else:
            number_players_string += "    "

        text_number_of_players = font_number_of_players.render(
            number_players_string, 1, (220, 20, 60)
        )
        textpos_number_of_players = text_number_of_players.get_rect(
            centerx=self.background_surface.get_width() / 2,
            centery=self.background_surface.get_height() / 1.4,
        )
        self.screen.blit(text_number_of_players, textpos_number_of_players)

    def draw_menu_background(self):
        self.initialize_menu_background()
        self.draw_number_players_selector()

    def draw_game_background(self):
        screen_height = self.screen.get_size()[1]
        screen_width = self.screen.get_size()[0]
        half_screen_width = (screen_width / 2) + 1
        half_screen_height = (screen_height / 2) + 1

        self.screen.fill(BLACK)

        if len(self.players) == 2:
            self.screen.blit(self.players[0].world, (0, 1))
            self.screen.blit(self.players[1].world, (half_screen_width, 1))
        elif len(self.players) == 3:
            self.screen.blit(self.players[0].world, (0, 0))
            self.screen.blit(self.players[1].world, (half_screen_width, 0))
            self.screen.blit(
                self.players[2].world, (screen_width / 4, half_screen_height)
            )
        elif len(self.players) == 4:
            self.screen.blit(self.players[0].world, (0, 0))
            self.screen.blit(self.players[1].world, (half_screen_width, 0))
            self.screen.blit(self.players[2].world, (0, half_screen_height))
            self.screen.blit(
                self.players[3].world, (half_screen_width, half_screen_height)
            )

    def draw_select_background(self):
        screen_height = self.screen.get_size()[1]
        screen_width = self.screen.get_size()[0]
        half_screen_width = (screen_width / 2) + 1
        half_screen_height = (screen_height / 2) + 1

        self.screen.fill(BLACK)

        if len(self.players) == 2:
            self.screen.blit(self.players[0].world, (0, 1))
            self.screen.blit(self.players[1].world, (half_screen_width, 1))
        elif len(self.players) == 3:
            self.screen.blit(self.players[0].world, (0, 0))
            self.screen.blit(self.players[1].world, (half_screen_width, 0))
            self.screen.blit(
                self.players[2].world, (screen_width / 4, half_screen_height)
            )
        elif len(self.players) == 4:
            self.screen.blit(self.players[0].world, (0, 0))
            self.screen.blit(self.players[1].world, (half_screen_width, 0))
            self.screen.blit(self.players[2].world, (0, half_screen_height))
            self.screen.blit(
                self.players[3].world, (half_screen_width, half_screen_height)
            )

    def draw_end_background(self):
        self.background_surface = pg.Surface(self.screen.get_size())
        self.background_surface = self.background_surface.convert()
        self.background_surface.fill(BLACK)

        winner = "Player "
        for i, player in enumerate(self.players):
            if player.get_player().is_alive():
                winner += str(i + 1)
                break

        self.write_end_text(winner=winner, sprite_name=player.get_theme())

    def write_end_text(self, winner, sprite_name):

        font_title = pg.font.Font(os.path.join(DATA_DIR, "Amatic-Bold.ttf"), 36 * 3)
        text_title = font_title.render(winner + " wins!", 1, (255, 20, 30))
        textpos_title = text_title.get_rect(
            centerx=self.background_surface.get_width() / 2,
            centery=self.background_surface.get_height() / 5,
        )
        self.background_surface.blit(text_title, textpos_title)

        font_team = pg.font.Font(os.path.join(DATA_DIR, "Amatic-Bold.ttf"), 12 * 3)
        text_team = font_team.render("Team Fishing Minigame Metaphor", 1, (220, 20, 60))
        textpos_team = text_team.get_rect(
            centerx=self.background_surface.get_width() / 2,
            centery=self.background_surface.get_height() / 1.8,
        )
        self.background_surface.blit(text_team, textpos_team)

        winner_sprite = helper.LOADED_IMAGES["sprite_" + sprite_name.lower() + "_front"]
        winner_sprite = pg.transform.scale(winner_sprite, (150, 150))
        winner_sprite_pos = winner_sprite.get_rect(
            centerx=self.background_surface.get_width() / 2,
            centery=self.background_surface.get_height() / 2.5,
        )

        self.background_surface.blit(winner_sprite, winner_sprite_pos)

    def main(self):
        """this function is called when the program starts.
        it initializes everything it needs, then runs in
        a loop until the function returns."""
        # Initialize Everything

        # Prepare Game Objects
        clock = pg.time.Clock()
        allsprites = pg.sprite.RenderPlain(())
        # Main Loop
        going = True
        while going:
            clock.tick(60)
            # Handle Input Events

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    going = False
                elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    going = False
                elif event.type == pg.KEYDOWN and event.key == pg.K_v:
                    pg.display.toggle_fullscreen()
                elif event.type == pg.VIDEORESIZE:
                    pg.display._resize_event(event)
                elif event.type == pg.KEYDOWN and event.key == pg.K_m:
                    if not pg.mixer.music.get_busy():
                        pg.mixer.music.unpause()
                    else:
                        pg.mixer.music.pause()

                self.process_event(event)

            if self.game_state == MENU:
                self.menu_loop()
            elif self.game_state == SELECT:
                self.select_loop()
            elif self.game_state == GAME:
                pass
                self.game_loop()
            elif self.game_state == END:
                self.end_loop()

            allsprites.update()

            # Draw Everything
            allsprites.draw(self.screen)
            pg.display.flip()

        pg.quit()

    def process_event(self, event):
        if self.game_state == MENU:
            self.process_menu_event(event)
        elif self.game_state == SELECT:
            self.process_select_event(event)
        elif self.game_state == GAME:
            self.process_game_event(event)
        elif self.game_state == END:
            self.process_end_event(event)

    def process_menu_event(self, event):
        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            self.initialize_game_worlds()
            for player in self.players:
                player.start()
            self.game_state = SELECT
            self.button_sound.play()
        elif event.type == pg.JOYBUTTONDOWN and event.button == 0:
            self.initialize_game_worlds()
            for player in self.players:
                player.start()
            self.game_state = SELECT
            self.button_sound.play()

        elif event.type == pg.KEYDOWN and (
            event.key == pg.K_a or event.key == pg.K_LEFT
        ):
            if self.number_of_players > 2:
                self.number_of_players -= 1
                self.select_sound.play()

        elif event.type == pg.KEYDOWN and event.key in [pg.K_d, pg.K_RIGHT]:
            if self.number_of_players < 4:
                self.number_of_players += 1
                self.select_sound.play()

        elif event.type == JOYBUTTONDOWN and event.button == 4:
            if self.number_of_players > 2:
                self.number_of_players -= 1
                self.select_sound.play()

        elif event.type == JOYBUTTONDOWN and event.button == 5:
            if self.number_of_players < 4:
                self.number_of_players += 1
                self.select_sound.play()

    def process_select_event(self, event):

        if (
            event.type == pg.KEYDOWN
            and event.key == pg.K_SPACE
            and self.game_state == SELECT
        ):
            self.game_state = GAME
            self.button_sound.play()
        elif (
            event.type == pg.JOYBUTTONDOWN
            and event.button == 0
            and self.game_state == SELECT
        ):
            self.game_state = GAME
            self.button_sound.play()

        if (
            event.type == pg.KEYDOWN
            and event.key == pg.K_a
            and not self.players[0].ready
        ):
            self.players[0].init_character(
                self.themes[(self.themes.index(self.players[0].get_theme()) - 1) % 4]
            )
            self.select_sound.play()
        elif (
            event.type == pg.KEYDOWN
            and event.key == pg.K_d
            and not self.players[0].ready
        ):
            self.players[0].init_character(
                self.themes[(self.themes.index(self.players[0].get_theme()) + 1) % 4]
            )
            self.select_sound.play()
        elif event.type == pg.KEYDOWN and event.key == pg.K_LEFT:
            self.players[1].init_character(
                self.themes[(self.themes.index(self.players[1].get_theme()) - 1) % 4]
            )
            self.select_sound.play()
        elif event.type == pg.KEYDOWN and event.key == pg.K_RIGHT:
            self.players[1].init_character(
                self.themes[(self.themes.index(self.players[1].get_theme()) + 1) % 4]
            )
            self.select_sound.play()

        if event.type == pg.KEYDOWN and event.key == pg.K_q:
            self.players[0].ready = not self.players[0].ready
            self.button_sound.play()

        for index, player in enumerate(self.players):
            try:
                if (
                    event.type == pg.JOYBUTTONDOWN
                    and joysticks[index].get_instance_id() == event.instance_id
                    and event.button == XBOX360["LB"]
                ):
                    player.init_character(
                        self.themes[(self.themes.index(player.get_theme()) - 1) % 4]
                    )
            except IndexError:
                pass
            try:
                if (
                    event.type == pg.JOYBUTTONDOWN
                    and joysticks[index].get_instance_id() == event.instance_id
                    and event.button == XBOX360["RB"]
                ):
                    player.init_character(
                        self.themes[(self.themes.index(player.get_theme()) + 1) % 4]
                    )
            except IndexError:
                pass

    def process_game_event(self, event):
        if event.type == pg.KEYDOWN and event.key in P1DIRS:
            self.players[0].set_dir(P1DIRS[event.key], 1)
        elif event.type == pg.KEYUP and event.key in P1DIRS:
            self.players[0].set_dir(P1DIRS[event.key], 0)

        # controller support for player 1
        for index, player in enumerate(self.players):
            try:
                if (
                    event.type == pg.JOYHATMOTION
                    and joysticks[index].get_instance_id() == event.instance_id
                ):
                    player.set_dir(0, event.value)
            except IndexError:
                pass
            try:
                if (
                    event.type == pg.JOYAXISMOTION
                    and joysticks[index].get_instance_id() == event.instance_id
                ):
                    if abs(event.value) > 0.3:
                        player.set_dir(event.axis, event.value)
                    else:
                        player.set_dir(event.axis, 0.0)
            except IndexError:
                pass

        if event.type == pg.KEYDOWN and event.key in P2DIRS:
            self.players[1].set_dir(P2DIRS[event.key], 1)
        elif event.type == pg.KEYUP and event.key in P2DIRS:
            self.players[1].set_dir(P2DIRS[event.key], 0)

        # shop open/close keys
        if event.type == pg.KEYDOWN and event.key == pg.K_q:
            self.players[0].shop.toggle_open()
        elif event.type == pg.KEYDOWN and event.key == pg.K_p:
            self.players[1].shop.toggle_open()

        # players shop controller
        for index, player in enumerate(self.players):
            try:
                if (
                    event.type == pg.JOYBUTTONDOWN
                    and joysticks[index].get_instance_id() == event.instance_id
                    and event.button == XBOX360["LB"]
                ):
                    player.shop.toggle_open()
            except IndexError:
                pass

        # players[0] using powers
        if event.type == pg.KEYDOWN and event.key == pg.K_f:
            if self.players[0].pay_for_power("more"):
                self.players[1].activate_power("more")
        elif event.type == pg.KEYDOWN and event.key == pg.K_g:
            if self.players[0].pay_for_power("speed"):
                self.players[1].activate_power("speed")
        elif event.type == pg.KEYDOWN and event.key == pg.K_h:
            if self.players[0].pay_for_power("heal"):
                self.players[0].activate_power("heal")

        # players[0] powers with controller
        for index, player in enumerate(self.players):
            enemy_player = (index % 2) + 1
            try:
                if (
                    event.type == pg.JOYBUTTONDOWN
                    and joysticks[index].get_instance_id() == event.instance_id
                    and event.button == XBOX360["A"]
                ):
                    if player.pay_for_power("more"):
                        self.players[enemy_player].activate_power("more")
                elif (
                    event.type == pg.JOYBUTTONDOWN
                    and joysticks[index].get_instance_id() == event.instance_id
                    and event.button == XBOX360["B"]
                ):
                    if player.pay_for_power("speed"):
                        self.players[enemy_player].activate_power("speed")
                elif (
                    event.type == pg.JOYBUTTONDOWN
                    and joysticks[index].get_instance_id() == event.instance_id
                    and event.button == XBOX360["X"]
                ):
                    if player.pay_for_power("heal"):
                        player.activate_power("heal")
            except IndexError:
                pass

        # players[1] using powers
        if event.type == pg.KEYDOWN and event.key == pg.K_k:
            if self.players[1].pay_for_power("more"):
                self.players[0].activate_power("more")
        elif event.type == pg.KEYDOWN and event.key == pg.K_l:
            if self.players[1].pay_for_power("speed"):
                self.players[0].activate_power("speed")
        elif event.type == pg.KEYDOWN and event.key == pg.K_SEMICOLON:
            if self.players[1].pay_for_power("heal"):
                self.players[1].activate_power("heal")

    def process_end_event(self, event):
        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            for player in self.players:
                player.reset()
            self.game_state = MENU
            self.initialize_menu_background()
            self.victory_sound.stop()
            pg.mixer.music.play(-1)
        if event.type == JOYBUTTONDOWN and event.button == XBOX360["A"]:
            for player in self.players:
                player.reset()
            self.game_state = MENU
            self.initialize_menu_background()
            self.victory_sound.stop()
            pg.mixer.music.play(-1)

    def menu_loop(self):
        self.scrolling_menu_background.slide([-1, -1])
        music_ms = pg.mixer.music.get_pos()
        music_s = music_ms / 1000
        # Fishing song is 120bpm. Divide by 2 for 60bpm or 1bps and 4 beats makes a bar.
        val = (music_s % 8) / 2
        if self.menu_theme != math.floor(val):
            self.menu_theme = math.floor(val)
            self.scrolling_menu_background.set_sprite_dict(
                helper.create_background(self.themes[self.menu_theme], helper.WIN_SIZE)
            )
        self.scrolling_menu_background.draw(
            self.background_surface, self.screen.get_size()
        )
        self.write_menu_text()
        self.screen.blit(self.background_surface, (0, 0))
        self.draw_number_players_selector()

    def select_loop(self):
        self.draw_select_background()
        for i in self.players:
            i.draw_world()
            i.draw_select()

    def game_loop(self):
        for i in self.players:
            i.move()
            i.update_world()
        self.draw_game_background()

        players_left = 0
        for player in self.players:
            players_left += player.get_player().is_alive()

        if players_left < 2:
            self.game_state = END
            self.draw_end_background()
            pg.mixer.music.stop()
            self.victory_sound.play()

    def end_loop(self):
        self.screen.blit(self.background_surface, (0, 0))

    def initialize_game_worlds(self):
        self.players = []
        world_size = ((512 * 3) // 2, (288 * 3))
        if self.number_of_players > 2:
            world_size = ((512 * 3) // 2, (288 * 3) // 2)
        for i in range(self.number_of_players):
            self.players.append(World(dims=world_size, theme=self.themes[i]))


# Game Over

# this calls the 'main' function when this script is executed
game = Game()
game.main()
