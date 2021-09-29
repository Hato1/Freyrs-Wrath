import random
import math
import pygame as pg

from helper import LOADED_IMAGES


class Entity(pg.sprite.Sprite):

    def __init__(self, sprite_dict, position, lives=3, speed=2, ai=None):
        pg.sprite.Sprite.__init__(self)

        self.image = "DOWN"
        self.sprite_dict = sprite_dict

        x, y = list(position)
        x -= self.get_width() / 2
        y -= self.get_height() / 2
        self.position = [x, y]

        self.lives = lives
        self.max_lives = lives
        self.speed = speed

        self.ai = ai
        self.info = {}

    def get_speed(self):
        return self.speed

    def get_height(self):
        return LOADED_IMAGES[self.sprite_dict[self.image]].get_height()

    def get_width(self):
        return LOADED_IMAGES[self.sprite_dict[self.image]].get_width()

    def get_position(self):
        return self.position

    def get_center(self, world_size):
        return ((self.position[0] + self.get_width()/2) % world_size[0],
                (self.position[1] + self.get_height()/2) % world_size[1])

    def get_sprite(self):
        return LOADED_IMAGES[self.sprite_dict[self.image]]

    def get_sprite_id(self):
        """Used to help delete background sprite from LOADED_IMAGES"""
        return self.sprite_dict[self.image]

    def is_alive(self):
        return self.lives > 0

    def set_sprite_dict(self, sprite_dict):
        self.sprite_dict = sprite_dict

    def set_position(self, position):
        self.position = [position[0]-self.get_width()/2, position[1]-self.get_height()/2]

    def update_info(self, new_info):
        self.info.update(new_info)

    def change_control(self, new_scheme):
        self.control = new_scheme

    def slide(self, vec):
        self.position[0] += vec[0]
        self.position[1] += vec[1]

    def set_dir(self, vector):
        if vector[0] > 0.5:
            self.image = "LEFT"
        elif vector[0] < -0.5:
            self.image = "RIGHT"
        elif vector[1] > 0:
            self.image = "UP"
        elif vector[1] < 0:
            self.image = "DOWN"

    def draw(self, surface, dims):
        wrap_x = False
        wrap_y = False
        self.position[0] %= dims[0]
        self.position[1] %= dims[1]
        image = LOADED_IMAGES[self.sprite_dict[self.image]]
        # position = sprite.get_rect()
        if self.position[0] < 0:
            # off screen left
            xmod = dims[0]
            wrap_x = True

        if self.position[0] + image.get_width() > dims[0]:
            # off screen right
            xmod = -dims[0]
            wrap_x = True

        if self.position[1] < 0:
            # off screen top
            ymod = dims[1]
            wrap_y = True

        if self.position[1] + image.get_height() > dims[1]:
            # off screen bottom
            ymod = -dims[1]
            wrap_y = True

        if wrap_x and wrap_y:
            x, y = self.position
            surface.blit(image, (x+xmod, y))
            surface.blit(image, (x, y+ymod))
            surface.blit(image, (x+xmod, y+ymod))
            self.position[0] += xmod
            self.position[1] += ymod
        elif wrap_x:
            self.position[0] += xmod
            surface.blit(image, self.position)
        elif wrap_y:
            self.position[1] += ymod
            surface.blit(image, self.position)

        self.position[0] %= dims[0]
        self.position[1] %= dims[1]
        surface.blit(image, self.position)

    def check_collision(self, object):
        """Fails if object completely encompases me"""
        my_pos = [self.position[0] + self.get_width()/2, self.position[1] + self.get_height()/2]

        object_pos = object.get_position()
        left = object_pos[0]
        top = object_pos[1]
        bottom = object_pos[1] + object.get_height()
        right = object_pos[0] + object.get_width()

        if top <= my_pos[1] <= bottom:
            if left <= my_pos[0] <= right:
                return True

    def move(self, world_size):
        if self.ai:
            if self.ai == 'follow':
                x, y = self.ai_follow(world_size)
            elif self.ai == 'distance':
                x, y = self.ai_distance(world_size)
            elif self.ai == 'amble':
                x, y = self.ai_amble(world_size)
            elif self.ai == 'madman':
                x, y = self.ai_madman(world_size)
            else:
                raise ValueError('No such ai method {}'.format(self.ai))
            norm = (x**2 + y**2)**0.5
            if norm == 0:
                return (0, 0)
            x = x / norm
            y = y / norm

            # self.rect.move_ip(x * self.speed, y * self.speed)
            self.position[0] += x * self.speed
            self.position[1] += y * self.speed
            self.set_dir([-x, -y])
            return (x, y)
        else:
            return False

    def ai_amble(self, world_size):
        if 'amble' not in self.info:
            self.info['amble'] = [(random.random(), random.random()), random.randint(60, 240)]

        v, idle_frames = self.info['amble']
        if idle_frames:
            self.info['amble'][1] -= 1
            return (0, 0)

        elif random.random() > 0.99:
            self.info['amble'][1] = random.randint(60, 240)
            self.info['amble'][0] = (random.uniform(-1, 1), random.uniform(-1, 1))
            return (0, 0)

        else:
            angle = random.uniform(-1, 1)
            return v

    def ai_follow(self, world_size):
        x, y = self.get_center(world_size)
        tx, ty = self.info['target'].get_center(world_size)
        return (tx-x, ty-y)

    def ai_distance(self, world_size):
        me = self.get_center(world_size)
        nearest = None
        min_dist = math.inf
        for entity in self.info['distance']:
            them = entity.get_center(world_size)
            dist = distance(me, them)
            if dist < min_dist and self is not entity:
                nearest = them
                min_dist = dist

        target = self.info['target'].get_center(world_size)
        dist = distance(me, target)
        if dist < min_dist or dist < 100:
            tx, ty = target
            return (tx-me[0], ty-me[1])
        else:
            return (me[0]-nearest[0], me[1]-nearest[1])

        closest = distance(self.get_center(), self.info['target'].get_center(world_size))

    def ai_madman(self, world_size):
        if 'mad' not in self.info:
            self.speed = 20
            self.info['mad'] = [(random.uniform(-1, 1), random.uniform(-1, 1)), 5]

        if self.info['mad'][1] <= 0:
            self.info['mad'][1] = 5
            x, y = self.info['mad'][0]
            angle = math.radians(random.uniform(-15, 15))
            self.info['mad'][0] = (x*math.cos(angle) - y*math.sin(angle), x*math.sin(angle) + y*math.cos(angle))

        self.info['mad'][1] -= 1
        return self.info['mad'][0]


def distance(a, b):
    return ((a[0] - b[0])**2 + (a[1] - b[1])**2)**0.5
