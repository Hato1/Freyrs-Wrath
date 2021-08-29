import os

import pygame as pg

from helper import LOADED_IMAGES, DATA_DIR

STARTING_PRICE_LIST = [0, 2, 2, 2]
STARTING_ABILITY_IMAGE_LIST = ["shop_icon", "heal", "speed", "more"]
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GOLD = (254, 224, 34)


CHARACTER_KEYS = {"sprite_viking": {"shop_icon": "q", "more": "f", "speed": "g", "heal": "h"},
                  "sprite_priest": {"shop_icon": "p", "more": "k", "speed": "l", "heal": ";"},
                  "sprite_farmer": {"shop_icon": "1", "more": "2", "speed": "3", "heal": "4"},
                  "sprite_demon": {"shop_icon": "5", "more": "6", "speed": "7", "heal": "8"}}


class Shop:

    def __init__(self, player_sprite, closed_dims):
        self.open = False
        self.open_surface = pg.Surface((closed_dims[0], closed_dims[1] * 4.5))
        self.closed_surface = pg.Surface(closed_dims)
        self.shop_surface = self.closed_surface
        self.shop_surface = self.shop_surface.convert()
        self.shop_bg_color = (10, 150, 50)
        self.shop_card_dict = {}

        self.populate_card_list(player_sprite)

    def populate_card_list(self, player_sprite):
        image_size = (self.closed_surface.get_width(), self.closed_surface.get_height())

        self.shop_card_list = [
            ShopCard(STARTING_ABILITY_IMAGE_LIST[0], LOADED_IMAGES[STARTING_ABILITY_IMAGE_LIST[0]], STARTING_PRICE_LIST[0], image_size, CHARACTER_KEYS[player_sprite][STARTING_ABILITY_IMAGE_LIST[0]]),
            ShopCard(STARTING_ABILITY_IMAGE_LIST[1], LOADED_IMAGES[STARTING_ABILITY_IMAGE_LIST[1]], STARTING_PRICE_LIST[1], image_size, CHARACTER_KEYS[player_sprite][STARTING_ABILITY_IMAGE_LIST[1]]),
            ShopCard(STARTING_ABILITY_IMAGE_LIST[2], LOADED_IMAGES[STARTING_ABILITY_IMAGE_LIST[2]], STARTING_PRICE_LIST[2], image_size, CHARACTER_KEYS[player_sprite][STARTING_ABILITY_IMAGE_LIST[2]]),
            ShopCard(STARTING_ABILITY_IMAGE_LIST[3], LOADED_IMAGES[STARTING_ABILITY_IMAGE_LIST[3]], STARTING_PRICE_LIST[3], image_size, CHARACTER_KEYS[player_sprite][STARTING_ABILITY_IMAGE_LIST[3]])
        ]

    def draw_shop(self):
        if self.open:
            self.draw_open_shop()
        else:
            self.draw_closed_shop()

    def draw_open_shop(self):
        self.shop_surface.fill(self.shop_bg_color)

        padding = 0.1
        for i, shop_card in enumerate(self.shop_card_list):
            offset = i + 0.5 + (padding * i)
            shop_icon_image_pos = shop_card.image.get_rect(
                centerx=0 + shop_card.image.get_rect().width / 2,
                centery=self.shop_surface.get_height() - shop_card.image.get_rect().height * (offset))
            self.shop_surface.blit(shop_card.image, shop_icon_image_pos)

    def draw_closed_shop(self):
        self.shop_surface.fill(self.shop_bg_color)
        self.shop_surface.blit(self.shop_card_list[0].image, self.shop_surface.get_rect())

    def toggle_open(self):
        if self.open:
            self.shop_surface = self.closed_surface
            self.open = False
        else:
            self.shop_surface = self.open_surface
            self.open = True

    def increase_price_of_power(self, power_name):
        for card in self.shop_card_list:
            if card.name == power_name:
                card.set_price(card.price*2)

    def get_shopcard(self, name):
        for shop_card in self.shop_card_list:
            if shop_card.name == name:
                return shop_card
        return None

class ShopCard:

    def __init__(self, name, image, price, image_size, control="q"):
        self.name = name
        self.base_image = pg.transform.scale(image, image_size)
        self.image = self.base_image
        self.price = price
        self.price_base = pg.Surface((15,10))
        self.price_base.fill(GOLD)
        self.font_name = 'MomcakeBold-WyonA.otf'
        self.set_control(control)
        self.set_price(price)

    def set_control(self, control):
        if self.name != "shop_icon":
            font = pg.font.Font(os.path.join(DATA_DIR, self.font_name), 18)
            text_control = font.render(control, 1, (255, 255, 255))
            text_pos = text_control.get_rect(centerx=self.base_image.get_width() / 2,
                                             centery=self.base_image.get_height() / 1.1)
            self.base_image.blit(text_control, text_pos)
        else:
            font = pg.font.Font(os.path.join(DATA_DIR, self.font_name), 36)
            text_control = font.render(control, 1, WHITE)
            text_pos = text_control.get_rect(centerx=self.base_image.get_width() / 2,
                                             centery=self.base_image.get_height() / 1.6)
            self.base_image.blit(text_control, text_pos)

    def set_price(self, price):
        self.price = price
        if self.name != "shop_icon":

            font = pg.font.Font(os.path.join(DATA_DIR, self.font_name), 18)
            text_control = font.render(str(price), 1, BLACK)
            text_pos = text_control.get_rect(centerx=self.base_image.get_width() / 1.5,
                                             centery=self.base_image.get_height() / 5.8)
            self.image.blit(self.price_base, (text_pos[0]-1, text_pos[1]+1))
            self.image.blit(text_control, text_pos)
