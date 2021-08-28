import os

import pygame as pg
from pygame.compat import geterror
from pygame.locals import *

import helper
from helper import load_sound, DATA_DIR, load_all_images, WIN_SIZE
from world import World

if not pg.font:
    print("Warning, fonts disabled")
if not pg.mixer:
    print("Warning, sound disabled")

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
P1DIRSC = {0: 'UP'}
P1DIRS = {pg.K_w: 'UP', pg.K_s: 'DOWN', pg.K_a: 'LEFT', pg.K_d: 'RIGHT'}
P2DIRS = {pg.K_UP: 'UP', pg.K_DOWN: 'DOWN', pg.K_LEFT: 'LEFT', pg.K_RIGHT: 'RIGHT'}
pg.init()
js = pg.joystick.Joystick(0)
js.init()

class Game:

    def __init__(self, state=MENU):
        self.game_state = state
        self.background_surface = None  # init in setup_game
        self.screen = None  # init in setup_game
        self.soundtrack = None
        self.setup_game()

        half_screen_width = self.screen.get_size()[0] / 2
        screen_height = self.screen.get_size()[1]
        self.players = []

        sprites = [PLAYER_1_SPRITE, PLAYER_2_SPRITE, PLAYER_2_SPRITE, PLAYER_1_SPRITE]
        characters = ["VIKING", "PRIEST", "PRIEST", "VIKING"]
        for i in range(helper.PLAYERCOUNT):
            self.players.append(World(dims=helper.WORLD_SIZE, character=characters[i]))
            # self.players.append(World(dims=helper.WORLD_SIZE, player_sprite=sprites[i]))

    def setup_game(self):
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
        half_screen_height = self.screen.get_size()[1] / 2
        screen_height = self.screen.get_size()[1]
        screen_width = self.screen.get_size()[0]
        for i, player in enumerate(self.players):
            if i % 2 == 0:
                posx = 0
            else:
                posx = half_screen_width + 1
            if i < 2:
                posy = 0
            else:
                posy = half_screen_height + 1
            self.screen.blit(player.world, (posx, posy))
        if len(self.players) == 3:
            filler = pg.Surface(helper.WORLD_SIZE)
            filler = filler.convert()
            filler.fill(BLACK)
            self.screen.blit(filler, (half_screen_width+1, half_screen_height+1))
        if len(self.players) > 2:
            h_divider = pg.Surface((screen_width, 2))
            h_divider = h_divider.convert()
            h_divider.fill(BLACK)
            self.screen.blit(h_divider, (0, half_screen_height-1))

        v_divider = pg.Surface((2, screen_height))
        v_divider = v_divider.convert()
        v_divider.fill(BLACK)
        self.screen.blit(v_divider, (half_screen_width-1, 0))
        pg.display.flip()

    def draw_end_background(self):
        self.background_surface = pg.Surface(self.screen.get_size())
        self.background_surface = self.background_surface.convert()
        self.background_surface.fill(GREY)
        self.write_end_text()

    def write_end_text(self):
        winner = ""
        for player in self.players:
            if player.check_alive():
                winner = player.get_name()

        font_title = pg.font.Font(os.path.join(DATA_DIR, 'Amatic-Bold.ttf'), 36 * 3)
        text_title = font_title.render(winner + ' WINS!', 1, (255, 20, 30))
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
        elif event.type == pg.JOYBUTTONDOWN and event.button == 0 and self.game_state == MENU:
            self.game_state = GAME
            button_sound = load_sound("button_sound.mp3")
            button_sound.play()

    def process_game_event(self, event):
        if event.type == pg.KEYDOWN and event.key in P1DIRS:
            self.players[0].set_dir(P1DIRS[event.key], 1)
        elif event.type == pg.KEYUP and event.key in P1DIRS:
            self.players[0].set_dir(P1DIRS[event.key], 0)

        #controller support for player 1
        if event.type == pg.JOYHATMOTION and js.get_instance_id() == 0:
            self.players[0].set_dir(P1DIRSC[event.hat], event.value)
        if event.type == pg.JOYAXISMOTION and js.get_instance_id() == 0:
            if abs(event.value) > 0.3:
                self.players[0].set_dir(event.axis, event.value)
            else:
                self.players[0].set_dir(event.axis, 0.0)


        if event.type == pg.KEYDOWN and event.key in P2DIRS:
            self.players[1].set_dir(P2DIRS[event.key], 1)
        elif event.type == pg.KEYUP and event.key in P2DIRS:
            self.players[1].set_dir(P2DIRS[event.key], 0)

        #shop open/close keys
        if event.type == pg.KEYDOWN and event.key == pg.K_q:
            self.players[0].shop.toggle_open()
        elif event.type == pg.KEYDOWN and event.key == pg.K_p:
            self.players[1].shop.toggle_open()

        #players[0] shop controller
        if event.type == pg.JOYBUTTONDOWN and js.get_instance_id() == 0 and event.button == 4:
            self.players[0].shop.toggle_open()


        #players[0] using powers
        if event.type == pg.KEYDOWN and event.key == pg.K_f:
            if self.players[0].pay_for_power("more"):
                self.players[1].activate_power("more")
        elif event.type == pg.KEYDOWN and event.key == pg.K_g:
            if self.players[0].pay_for_power("speed"):
                self.players[1].activate_power("speed")
        elif event.type == pg.KEYDOWN and event.key == pg.K_h:
            if self.players[0].pay_for_power("heal"):
                self.players[0].activate_power("heal")


    #players[0] powers with controller
        if event.type == pg.JOYBUTTONDOWN and js.get_instance_id() == 0 and event.button == 0:
            if self.players[0].pay_for_power("more"):
                    self.players[1].activate_power("more")
        elif event.type == pg.JOYBUTTONDOWN and js.get_instance_id() == 0 and event.button == 1:
            if self.players[0].pay_for_power("speed"):
                self.players[1].activate_power("speed")
        elif event.type == pg.JOYBUTTONDOWN and js.get_instance_id() == 0 and event.button == 2:
            if self.players[0].pay_for_power("heal"):
                self.players[0].activate_power("heal")

        #players[1] using powers
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
        pass

    def menu_loop(self):
        self.screen.blit(self.background_surface, (0, 0))

    def game_loop(self):
        for i in self.players:
            i.move()
            i.update_world()
        self.draw_game_background()

        players_left = 0
        for player in self.players:
            players_left += player.check_alive()

        if players_left < 2:
            self.game_state = END
            self.draw_end_background()

    def end_loop(self):
        self.screen.blit(self.background_surface, (0, 0))


# Game Over

# this calls the 'main' function when this script is executed
game = Game()
game.main()
