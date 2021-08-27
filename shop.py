import pygame as pg


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

    def set_open(self, open):
        if open:
            self.shop = pg.Surface((150, 30))
        else:
            pg.Surface((30, 30))
        self.shop = self.shop.convert()
