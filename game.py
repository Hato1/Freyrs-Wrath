import os

import pygame as pg
from pygame.compat import geterror
from pygame.locals import *

from helper import load_sound, DATA_DIR, load_all_images
from world import World

if not pg.font:
    print("Warning, fonts disabled")
if not pg.mixer:
    print("Warning, sound disabled")

WIN_SIZE = (512, 288)
MENU = 1
GAME = 2
END = 3
GAME_STATE = MENU
WHITE = (255, 255, 255)
GREY = (122, 122, 122)
GREEN = (20, 239, 20)
BLACK = (0, 0, 0)
GAME_NAME = "Name of the Game"
PLAYER_1_NAME = "VIKING"
PLAYER_2_NAME = "MONK"
PLAYER_1_SPRITE = "sprite_priest"
PLAYER_2_SPRITE = "sprite_viking"
P1DIRS = {pg.K_w: 'UP', pg.K_s: 'DOWN', pg.K_a: 'LEFT', pg.K_d: 'RIGHT'}
P2DIRS = {pg.K_UP: 'UP', pg.K_DOWN: 'DOWN', pg.K_LEFT: 'LEFT', pg.K_RIGHT: 'RIGHT'}


class Game:

    def __init__(self, state=MENU):
        self.game_state = state
        self.background_surface = None  # init in setup_game
        self.screen = None  # init in setup_game
        self.soundtrack = None
        self.setup_game()

        half_screen_width = self.screen.get_size()[0] / 2
        screen_height = self.screen.get_size()[1]
        self.p1 = World(dims=(half_screen_width-1, screen_height), player_sprite=PLAYER_1_SPRITE)
        self.p2 = World(dims=(half_screen_width-1, screen_height), player_sprite=PLAYER_2_SPRITE)

    def setup_game(self):
        pg.init()
        self.screen = pg.display.set_mode(WIN_SIZE, pg.SCALED | pg.RESIZABLE)
        pg.display.set_caption(GAME_NAME)
        load_all_images()
        self.draw_menu_background()
        self.soundtrack = load_sound("Fishing song.mp3")
        self.soundtrack.play(-1)

    def draw_menu_background(self):
        # Create The Menu
        self.background_surface = pg.Surface(self.screen.get_size())
        self.background_surface = self.background_surface.convert()
        self.background_surface.fill(WHITE)
        self.write_menu_text()

    def write_menu_text(self):
        font_title = pg.font.Font(os.path.join(DATA_DIR, 'Amatic-Bold.ttf'), 36 * 3)
        text_title = font_title.render(GAME_NAME, 1, (220, 20, 60))
        textpos_title = text_title.get_rect(centerx=self.background_surface.get_width() / 2,
                                            centery=self.background_surface.get_height() / 5)
        self.background_surface.blit(text_title, textpos_title)

        font_team = pg.font.Font(os.path.join(DATA_DIR, 'Amatic-Bold.ttf'), 12 * 3)
        text_team = font_team.render("Team Fishing Minigame Metaphor", 1, (220, 20, 60))
        textpos_team = text_team.get_rect(centerx=self.background_surface.get_width() / 2,
                                          centery=self.background_surface.get_height() / 1.8)
        self.background_surface.blit(text_team, textpos_team)

        text_by = font_team.render("by", 1, (220, 20, 60))
        textpos_by = text_by.get_rect(centerx=self.background_surface.get_width() / 2,
                                      centery=self.background_surface.get_height() / 2.2)
        self.background_surface.blit(text_by, textpos_by)

        font_space_to_begin = pg.font.Font(os.path.join(DATA_DIR, 'AmaticSC-Regular.ttf'), 16 * 3)
        text_space_to_begin = font_space_to_begin.render("Press Spacebar to Start", 1, (220, 20, 60))
        textpos_space_to_begin = text_space_to_begin.get_rect(centerx=self.background_surface.get_width() / 2,
                                                              centery=self.background_surface.get_height() / 1.2)
        self.background_surface.blit(text_space_to_begin, textpos_space_to_begin)

    def draw_game_background(self):
        half_screen_width = self.screen.get_size()[0] / 2
        screen_height = self.screen.get_size()[1]
        self.screen.blit(self.p1.world, (0, 0))
        self.screen.blit(self.p2.world, (half_screen_width + 1, 0))
        divider = pg.Surface((2, screen_height))
        divider = divider.convert()
        divider.fill(BLACK)
        self.screen.blit(divider, (half_screen_width-1, 0))
        pg.display.flip()

    def draw_end_background(self):
        self.background_surface = pg.Surface(self.screen.get_size())
        self.background_surface = self.background_surface.convert()
        self.background_surface.fill(GREY)
        self.write_end_text()

    def write_end_text(self):

        loser = ""
        if not self.p1.check_alive():
            loser = PLAYER_1_NAME
        elif not self.p2.check_alive():
            loser = PLAYER_2_NAME

        font_title = pg.font.Font(os.path.join(DATA_DIR, 'Amatic-Bold.ttf'), 36 * 3)
        text_title = font_title.render(loser, 1, (255, 20, 30))
        textpos_title = text_title.get_rect(centerx=self.background_surface.get_width() / 2,
                                            centery=self.background_surface.get_height() / 5)
        self.background_surface.blit(text_title, textpos_title)

        font_team = pg.font.Font(os.path.join(DATA_DIR, 'Amatic-Bold.ttf'), 12 * 3)
        text_team = font_team.render("Team Fishing Minigame Metaphor", 1, (220, 20, 60))
        textpos_team = text_team.get_rect(centerx=self.background_surface.get_width() / 2,
                                          centery=self.background_surface.get_height() / 1.8)
        self.background_surface.blit(text_team, textpos_team)

    def main(self):
        """this function is called when the program starts.
           it initializes everything it needs, then runs in
           a loop until the function returns."""
        # Initialize Everything

        # Display The Background
        self.screen.blit(self.background_surface, (0, 0))
        pg.display.flip()  # Flipping display is recommended practice to be sure display updates???

        # Prepare Game Objects
        clock = pg.time.Clock()
        allsprites = pg.sprite.RenderPlain(())

        self.draw_menu_background()

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
                    self.soundtrack.stop()

                self.process_event(event)

            if self.game_state == MENU:
                self.menu_loop()
            elif self.game_state == GAME:
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
        elif self.game_state == GAME:
            self.process_game_event(event)
        elif self.game_state == END:
            self.process_end_event(event)

    def process_menu_event(self, event):
        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE and self.game_state == MENU:
            self.game_state = GAME
            button_sound = load_sound("button_sound.mp3")
            button_sound.play()

    def process_game_event(self, event):
        if event.type == pg.KEYDOWN and event.key in P1DIRS:
            self.p1.set_dir(P1DIRS[event.key], 1)
        elif event.type == pg.KEYUP and event.key in P1DIRS:
            self.p1.set_dir(P1DIRS[event.key], 0)

        if event.type == pg.KEYDOWN and event.key in P2DIRS:
            self.p2.set_dir(P2DIRS[event.key], 1)
        elif event.type == pg.KEYUP and event.key in P2DIRS:
            self.p2.set_dir(P2DIRS[event.key], 0)

        if event.type == pg.KEYDOWN and event.key == pg.K_q:
            self.p1.shop.toggle_open()
        elif event.type == pg.KEYDOWN and event.key == pg.K_p:
            self.p2.shop.toggle_open()

        if event.type == pg.KEYDOWN and event.key == pg.K_f:
            if self.p1.pay_for_power("more"):
                self.p2.activate_power("more")
        elif event.type == pg.KEYDOWN and event.key == pg.K_g:
            if self.p1.pay_for_power("speed"):
                self.p2.activate_power("speed")
        elif event.type == pg.KEYDOWN and event.key == pg.K_h:
            if self.p1.pay_for_power("health"):
                self.p1.activate_power("health")

    def process_end_event(self, event):
        pass

    def menu_loop(self):
        self.screen.blit(self.background_surface, (0, 0))

    def game_loop(self):
        self.p1.move()
        self.p2.move()
        self.p1.update_world()
        self.p2.update_world()
        self.draw_game_background()

        if (not self.p1.check_alive()) or (not self.p2.check_alive()):
            self.game_state = END
            self.draw_end_background()

    def end_loop(self):
        self.screen.blit(self.background_surface, (0, 0))


# Game Over

# this calls the 'main' function when this script is executed
game = Game()
game.main()
