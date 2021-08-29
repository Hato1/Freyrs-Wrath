import random
import pygame as pg
from pygame.locals import *
import os

import helper
from helper import DATA_DIR, load_image, LOADED_IMAGES, load_sound

from entity import Entity

CHARACTERS = {'VIKING': {'player_sprite': 'sprite_viking', 'enemy_sprite': 'sprite_demon'},
              'PRIEST': {'player_sprite': 'sprite_priest', 'enemy_sprite': 'sprite_farmer'},
              'FARMER': {'player_sprite': 'sprite_farmer', 'enemy_sprite': 'sprite_viking'},
              'DEMON': {'player_sprite': 'sprite_demon', 'enemy_sprite': 'sprite_priest'}}

class Select:

    def __init__(self, dims):
        self.dims = dims
        self.name = 'VIKING'
        self.screen = pg.Surface(self.dims)
        self.screen = self.screen.convert()

        self.sprite_dict = {'DOWN': 'sprite_viking_front'}

        self.allsprites = pg.sprite.RenderPlain()
        self.background = Entity(helper.create_background(self.name), (0, 0))
        self.player = Entity(self.sprite_dict, (self.screen.get_width() / 2, self.screen.get_height() / 2), type='Player',
                             lives=3)
        self.update_screen()


    def update_screen(self):
        self.background.draw(self.screen, self.dims)
        self.allsprites.update()
        for sprite in self.allsprites:
            sprite.draw(self.screen, self.dims)

        self.update_gui()
        self.screen.blit(self.player.get_sprite(), self.player.get_position())
        pg.display.flip()


    def change_character(self, character):
        self.name = character


    def update_gui(self):
        font_select = pg.font.Font(os.path.join(DATA_DIR, 'Amatic-Bold.ttf'), 36 * 3)
        text_select = font_select.render('Choose Your Character', 1, (220, 20, 60))
        textpos_select = text_select.get_rect(centerx=self.screen.get_width() / 2,
                                            centery=self.screen.get_height() / 5)
        self.screen.blit(text_select, textpos_select)