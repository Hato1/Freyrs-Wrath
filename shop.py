import os

import pygame as pg

from helper import DATA_DIR, load_image, LOADED_IMAGES


class Shop:

    def __init__(self, player_sprite, closed_dims):
        self.open = False
        self.open_surface = pg.Surface((closed_dims[0], closed_dims[1] * 4.5))
        self.closed_surface = pg.Surface(closed_dims)
        self.shop_surface = self.closed_surface
        self.shop_surface = self.shop_surface.convert()
        self.shop_bg_color = (10, 150, 50)
        self.shop_card_list = []
        self.populate_card_list(player_sprite)

    def populate_card_list(self, player_sprite):
        image_size = (self.closed_surface.get_width(), self.closed_surface.get_height())

        if player_sprite == "sprite_viking":
            self.shop_card_list = [
                ShopCard("shop_icon", LOADED_IMAGES["shop_icon_q"], 0, image_size=image_size),
                ShopCard("ability1", LOADED_IMAGES["shop_ability_f"], 2, image_size=image_size),
                ShopCard("ability2", LOADED_IMAGES["shop_ability_g"], 2, image_size=image_size),
                ShopCard("ability3", LOADED_IMAGES["shop_ability_h"], 2, image_size=image_size)
            ]

        else:
            self.shop_card_list = [
                ShopCard("shop_icon", LOADED_IMAGES["shop_icon_p"], 0, image_size=image_size),
                ShopCard("ability1", LOADED_IMAGES["shop_ability_k"], 2, image_size=image_size),
                ShopCard("ability2", LOADED_IMAGES["shop_ability_l"], 2, image_size=image_size),
                ShopCard("ability3", LOADED_IMAGES["shop_ability_;"], 2, image_size=image_size)
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

    def set_displayed_price_of_power(self, power_number, price):
        pass


class ShopCard:

    def __init__(self, name, image, price, image_size, control="f"):
        self.name = name
        self.image = pg.transform.scale(image, image_size)
        self.price = price
        self.control = control
