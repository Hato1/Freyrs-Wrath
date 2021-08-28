import os

import pygame as pg

from helper import DATA_DIR, load_image, LOADED_IMAGES


class Shop:

    def __init__(self):
        self.open = True
        #TODO handle shop open/closed state instead of manually setting surfaces
        self.shop = pg.Surface((150, 30))
        self.shop = self.shop.convert()
        self.shop_icon_image = LOADED_IMAGES["shop_icon_q"][0]
        self.shop_f_image = LOADED_IMAGES["shop_ability_f"][0]
        self.shop_g_image = LOADED_IMAGES["shop_ability_g"][0]
        self.shop_h_image = LOADED_IMAGES["shop_ability_h"][0]

    def draw_shop(self):
        if self.open:
            self.draw_open_shop()
        else:
            self.draw_closed_shop()

    def draw_open_shop(self):
        self.shop.fill((10, 150, 50))
        self.shop_icon_image = pg.transform.scale(self.shop_icon_image, (30,30))
        shop_icon_image_pos = self.shop_icon_image.get_rect(
            centerx=self.shop.get_width() - self.shop_icon_image.get_rect().width*0.5,
            centery=self.shop.get_height() / 2)
        self.shop.blit(self.shop_icon_image, shop_icon_image_pos)

        self.shop_f_image = pg.transform.scale(self.shop_f_image, (30, 30))
        shop_f_image_pos = self.shop_f_image.get_rect(
            centerx=self.shop_f_image.get_rect().width * 0.5,
            centery=self.shop.get_height() / 2)
        self.shop.blit(self.shop_f_image, shop_f_image_pos)

        self.shop_g_image = pg.transform.scale(self.shop_g_image, (30, 30))
        shop_g_image_pos = self.shop_g_image.get_rect(
            centerx=self.shop_f_image.get_rect().width * 1.5,
            centery=self.shop.get_height() / 2)
        self.shop.blit(self.shop_g_image, shop_g_image_pos)

        self.shop_h_image = pg.transform.scale(self.shop_h_image, (30, 30))
        shop_h_image_pos = self.shop_h_image.get_rect(
            centerx=self.shop_f_image.get_rect().width * 2.5,
            centery=self.shop.get_height() / 2)
        self.shop.blit(self.shop_h_image, shop_h_image_pos)

    def draw_closed_shop(self):
        self.shop.fill((10, 200, 250))
        shop_icon_image, rect = LOADED_IMAGES["sprite_shop_shop_p"]
        shop_icon_image = pg.transform.scale(shop_icon_image, (30, 30))
        shop_icon_surface = pg.Surface((30, 30))
        self.shop.blit(shop_icon_image, shop_icon_surface.get_rect())

    def set_open(self, open):
        if open:
            self.shop = pg.Surface((150, 30))
        else:
            pg.Surface((30, 30))
        self.shop = self.shop.convert()
