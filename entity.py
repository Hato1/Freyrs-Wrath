import random
import pygame as pg

from helper import DATA_DIR, load_image, LOADED_IMAGES, WORLD_DIMS


# To do:
# Handle position wrapping. (helper function?)

class Entity(pg.sprite.Sprite):
    def __init__(self, sprite_dict, position, lives=3, speed=5, ai=None, type="Entity", info={}):
        """EG Entity([5.5, 7.64], ai='follow')"""
        pg.sprite.Sprite.__init__(self)
        self.image, self.rect = LOADED_IMAGES[sprite_dict["DOWN"]]
        self.sprite_dict = sprite_dict
        self.position = list(position)
        self.position[0] -= self.image.get_width() / 2
        self.position[1] -= self.image.get_height() / 2
        # self.rect.center = position
        self.lives = lives
        self.max_lives = lives
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

    def draw(self, surface, dims):
        wrap_x = False
        wrap_y = False
        # position = sprite.get_rect()
        if self.position[0] < 0:
            # off screen left
            # self.position[0] += dims[0]
            xmod = dims[0]
            wrap_x = True

        if self.position[0] + self.image.get_width() > dims[0]:
            # off screen right
            # self.position[0] += -dims[0]
            xmod = -dims[0]
            wrap_x = True

        if self.position[1] < 0:
            # off screen top
            # self.position[1] += dims[1]
            ymod = dims[1]
            wrap_y = True

        if self.position[1] + self.image.get_height() > dims[1]:
            # off screen bottom
            # self.position[1] += -dims[1]
            ymod = -dims[1]
            wrap_y = True

        if wrap_x and wrap_y:
            x, y = self.position
            surface.blit(self.image, (x+xmod, y))
            surface.blit(self.image, (x, y+ymod))
            surface.blit(self.image, (x+xmod, y+ymod))
            self.position[0] += xmod
            self.position[1] += ymod
        elif wrap_x:
            self.position[0] += xmod
            surface.blit(self.image, self.position)
        elif wrap_y:
            self.position[1] += ymod
            surface.blit(self.image, self.position)

        self.position[0] %= dims[0]
        self.position[1] %= dims[1]

        surface.blit(self.image, self.position)

    def get_width(self):
        return self.image.get_width()

    def set_rect(self, rect):
        self.position = rect

    def set_sprite(self, sprite):
        self.image = sprite

    def get_position(self):
        return self.position

    def set_position(self, position):
        self.position = position

    def change_control(self, new_scheme):
        self.control = new_scheme

    def check_collision(self, object):
        # entity_L = self.position[0] + self.get_height() * 0.2
        # entity_T = self.position[1] + self.get_width() * 0.4
        # entity_B = self.position[1] + self.get_height() * 0.8
        # entity_R = self.position[0] + self.get_width() * 0.6

        entity_C = [self.position[0] + self.get_width()/2, self.position[1] + self.get_height()/2]

        object_pos = object.get_position()
        object_L = object_pos[0]
        object_T = object_pos[1]
        object_B = object_pos[1] + object.get_height()
        object_R = object_pos[0] + object.get_width()

        # if not(object_R <= entity_L or object_L >= entity_R):
        #     if not(object_B <= entity_T or object_T >= entity_B):
        #         return True
        if object_T <= entity_C[1] <= object_B:
            if object_L <= entity_C[0] <= object_R:
                return True




    def is_alive(self):
        return self.lives > 0

    def move(self):
        if self.ai:
            if self.ai == 'follow':
                x, y = self.ai_follow()
            else:
                raise ValueError('No such ai method {}'.format())
            norm = (x**2 + y**2)**0.5
            if norm == 0:
                return (0, 0)
            x = x / norm
            y = y / norm

            self.rect.move_ip(x * self.speed, y * self.speed)
            self.position[0] += x * self.speed
            self.position[1] += y * self.speed
            self.set_dir([-x,-y])
            return (x, y)
        else:
            return False

    def slide(self, vec):
        self.position[0] += vec[0]
        self.position[1] += vec[1]

    def update_info(self, new_info):
        self.info.update(new_info)

    def get_center(self):
        return ((self.position[0] + self.image.get_width()/2) % WORLD_DIMS[0],
                (self.position[1] + self.image.get_height()/2) % WORLD_DIMS[1])

    def ai_follow(self):
        x, y = self.get_center()
        tx, ty = self.info['target'].get_center()
        return (tx-x, ty-y)

    def set_dir(self, vector):
        if vector[0] > 0.5:
            self.image, self.rect = LOADED_IMAGES[self.sprite_dict["LEFT"]]
        elif vector[0] < -0.5:
            self.image, self.rect = LOADED_IMAGES[self.sprite_dict["RIGHT"]]
        elif vector[1] > 0:
            self.image, self.rect = LOADED_IMAGES[self.sprite_dict["UP"]]
        elif vector[1] < 0:
            self.image, self.rect = LOADED_IMAGES[self.sprite_dict["DOWN"]]
