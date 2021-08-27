import random
import pygame as pg

from helper import DATA_DIR, load_image


# To do:
# Handle position wrapping. (helper function?)


class Entity(pg.sprite.Sprite):
    def __init__(self, sprite, position, lives=3, speed=5, ai=None):
        """EG Entity([5.5, 7.64], ai=BaseAI())"""
        pg.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(sprite, -1)
        self.rect.topleft = position
        self.lives = lives
        self.speed = speed
        self.ai = ai

    def get_position(self):
        return self.rect.topleft

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
            x, y = self.ai.decide_move()
            norm = (x**2 + y**2)**0.5
            x = x / norm
            y = y / norm
            #self.rect.topleft[0] += x * self.speed
            #self.rect.topleft[1] += y * self.speed
            self.rect.topleft = (self.rect.topleft[0] + x * self.speed, self.rect.topleft[1] + y * self.speed)
            return (x, y)
        else:
            return False


class BaseAI():
    """Generic AI goes down and right"""
    def __init__(self, info={}):
        """Info is a dictionary of decision making materials."""
        self.info = info

    def decide_move(self):
        """Using info, decides the best direction vector to use"""
        best_move = (2, 1)  # Down and right. More right than down.
        return(best_move)

    def update_info(self, new_info):
        self.info.update(new_info)


class Follow(BaseAI):
    """Moves from 'me' toward 'target'."""
    def decide_move(self):
        x, y = self.info['me'].get_position()
        tx, ty = self.info['target'].get_position()
        return (tx-x, ty-y)
