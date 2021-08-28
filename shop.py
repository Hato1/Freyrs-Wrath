import os

import pygame as pg

from helper import DATA_DIR, load_image


class Shop:

    def __init__(self):
        self.open = False
        self.shop = pg.Surface((30, 30))
        self.shop = self.shop.convert()

    def draw_shop(self):
        if self.open:
            self.draw_open_shop()
        else:
            self.draw_closed_shop()

    def draw_open_shop(self):
        self.shop.fill((10, 150, 50))

    def draw_closed_shop(self):
        self.shop.fill((10, 200, 250))
        shop_shop_path = os.path.join(DATA_DIR, 'sprite_shop_shop/sprite_shop_shop_p.png')
        shop_icon_image, rect = load_image(shop_shop_path, -1)
        shop_icon_image = pg.transform.scale(shop_icon_image, (30, 30))
        shop_icon_surface = pg.Surface((30, 30))
        self.shop.blit(shop_icon_image, shop_icon_surface.get_rect())

    def set_open(self, open):
        if open:
            self.shop = pg.Surface((150, 30))
        else:
            pg.Surface((30, 30))
        self.shop = self.shop.convert()
