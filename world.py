import pygame as pg
import os

from entity import Entity

MAIN_DIR = os.path.split(os.path.abspath(__file__))[0]
DATA_DIR = os.path.join(MAIN_DIR, "data")


class World:

    def __init__(self, dims):

        self.dims = dims

        self.world = pg.Surface(self.dims)
        self.world = self.world.convert()
        self.draw_world()

        self.money = 100
        self.font_money = pg.font.Font(os.path.join(DATA_DIR, 'Amatic-Bold.ttf'), 36 * 3)
        self.text_money = self.font_money.render(str(self.money), 1, (220, 20, 60))


        self.player = Entity((self.world.get_width()/2, self.world.get_height()/2))

        self.entity_list = [self.player]

        self.update_world()



    def update_world(self):
        self.world.fill((100, 250, 250))
        self.money -= 1
        self.update_money()

        for entity in self.entity_list:
            entity.move()


    def add_entity(self):
        entity = Entity([0,0])
        self.entity_list.append(entity)

    def get_surface(self):
        return self.world

    def draw_world(self):
        self.world.fill((100, 250, 250))

    def update_money(self):
        self.text_money = self.font_money.render(str(self.money), 1, (220, 20, 60))

        textpos_money = self.text_money.get_rect(centerx=self.world.get_width() / 2,
                                                 centery=self.world.get_height() / 4)

        self.world.blit(self.text_money, textpos_money)

    def check_alive(self):
        return self.player.is_alive()


    def player_move(self):
        return


#     Screen.player = Entity()
#     Screen.entities = []
#     Screen.money = 1337
#     Entity class:
# Player:
#     Lives = 3
#     Position (able to move)
#
# Enemy:
# Lives = 1
# Position (AI movement)
# Controls: Enemy_ai class
#     Shop class:
#     Overlay displayed: True/False
#     More enemies
#     Faster enemies
#
#     Extra life
#     Faster speed
