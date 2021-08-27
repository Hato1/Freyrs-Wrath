import pygame as pg
import os
MAIN_DIR = os.path.split(os.path.abspath(__file__))[0]
DATA_DIR = os.path.join(MAIN_DIR, "data")


class World:

    def __init__(self, dims):
        self.dims = dims

        self.world = pg.Surface(self.dims)
        self.world = self.world.convert()
        self.drawWorld()

        self.money = 100
        self.font_money = pg.font.Font(os.path.join(DATA_DIR, 'Amatic-Bold.ttf'), 36 * 3)
        self.text_money = self.font_money.render(str(self.money), 1, (220, 20, 60))
        self.updateMoney()



    def updateWorld(self):
        self.money -= 1
        self.updateMoney()


    def getSurface(self):
        return self.world


    def drawWorld(self):
        self.world.fill((100, 250, 250))

    def updateMoney(self):
        textpos_money = self.text_money.get_rect(centerx = self.world.get_width() / 2, centery = self.world.get_height() / 4)
        self.world.blit(self.text_money, textpos_money)





    def getGameState(self):
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
