import random
import pygame as pg

from helper import DATA_DIR, load_image


# To do:
# Handle position wrapping. (helper function?)

class Entity(pg.sprite.Sprite):
    def __init__(self, sprite, position, lives=3, speed=5, ai=None, type="Entity", info={}):
        """EG Entity([5.5, 7.64], ai=BaseAI())"""
        pg.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(sprite, -1)
        self.position = list(position)
        # self.rect.center = position
        self.lives = lives
        self.speed = speed
        self.ai = ai
        self.type = type

        self.info = info

    def __type__(self):
        return self.type

    def get_rect(self):
        return self.rect

    def get_sprite(self):
        return self.image

    def get_height(self):
        return self.image.get_height()

    def move_ip(self, x, y):
        self.rect.move_ip(x, y)

    def draw(self, surface, dims):
        wrap_around = False
        # position = sprite.get_rect()
        if self.position[0] < 0:
            # off screen left
            self.position[0] += dims[0]
            wrap_around = True

        if self.position[0] + self.image.get_width() > dims[0]:
            # off screen right
            self.position[0] += -dims[0]
            wrap_around = True

        if self.position[1] < 0:
            # off screen top
            self.position[1] += dims[1]
            wrap_around = True

        if self.position[1] + self.image.get_height() > dims[1]:
            # off screen bottom
            self.position[1] += -dims[1]
            wrap_around = True

        if wrap_around:
            surface.blit(self.image, self.position)

        self.position[0] %= dims[0]
        self.position[1] %= dims[1]

        surface.blit(self.image, self.position)

    def get_width(self):
        return self.image.get_width()

    def set_rect(self, rect):
        self.position = rect

    def get_position(self):
        return self.position

    def set_position(self, position):
        self.rect.topleft = position

    def change_control(self, new_scheme):
        self.control = new_scheme

    def check_collision(self, objects):
        raise NotImplemented("How do I check for collision again?")

    def is_alive(self):
        return self.lives > 0

    def move(self):
        if self.ai:
            x, y = self.ai_follow() # .decide_move()
            norm = (x**2 + y**2)**0.5
            if norm == 0:
                return (0, 0)
            x = x / norm
            y = y / norm
            # self.rect.topleft = (self.rect.topleft[0] + x * self.speed, self.rect.topleft[1] + y * self.speed)
            # self.rect.move_ip(x * self.speed, y * self.speed)
            self.rect.move_ip(x * self.speed, y * self.speed)
            self.position[0] += x * self.speed
            self.position[1] += y * self.speed
            # += x * self.speed
            # self.rect.center[1] += y * self.speed
            return (x, y)
        else:
            return False

    def slide(self, vec):
        #self.rect.move_ip(vec)
        self.position[0] += vec[0]
        self.position[1] += vec[1]

    def update_info(self, new_info):
        # self.ai.update_info(info)
        self.info.update(new_info)

    def ai_follow(self):
        x, y = self.position
        tx, ty = self.info['target'].get_position()
        return (tx-x, ty-y)
