import pygame as pg
import os

from helper import DATA_DIR, load_image

from entity import Entity, BaseAI
from shop import Shop


class World:

    def __init__(self, dims):

        self.dims = dims

        self.world = pg.Surface(self.dims)
        self.world = self.world.convert()
        self.draw_world()
        self.shop = Shop()
        self.money = 100
        self.font_money = pg.font.Font(os.path.join(DATA_DIR, 'Amatic-Bold.ttf'), 36 * 3)
        self.text_money = self.font_money.render(str(self.money), 1, (220, 20, 60))
        #'sprite_viking', 'sprite_viking_front.png'
        player_path = os.path.join(DATA_DIR, 'Fist.bmp')
        self.player = Entity(player_path, (self.world.get_width()/2, self.world.get_height()/2), ai=BaseAI())

        self.entity_list = (self.player)
        self.allsprites = pg.sprite.RenderPlain(self.entity_list)
        self.update_world()

    def update_world(self):
        self.world.fill((100, 250, 250))
        self.money -= 1
        self.update_money()
        self.update_shop()
        self.player.move()
        self.allsprites.update()


        self.allsprites.draw(self.world)
        pg.display.flip()

    def add_entity(self, sprite):
        entity = Entity(sprite, [0, 0])
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

    def update_shop(self):
        self.shop.draw_shop()

        self.world.blit(self.shop.shop, (0, 0))

    def check_alive(self):
        return self.player.is_alive()

    def player_move(self):
        self.player.move()


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
