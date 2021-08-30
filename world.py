import random
import pygame as pg
from pygame.locals import *
import os

import helper
from helper import DATA_DIR, LOADED_IMAGES, load_sound

from entity import Entity
from shop import Shop

GOLD = (254, 224, 34)
CHARACTERS = {'VIKING': {'player_sprite': 'sprite_viking', 'enemy_sprite': 'sprite_demon'},
              'PRIEST': {'player_sprite': 'sprite_priest', 'enemy_sprite': 'sprite_farmer'},
              'FARMER': {'player_sprite': 'sprite_farmer', 'enemy_sprite': 'sprite_viking'},
              'DEMON': {'player_sprite': 'sprite_demon', 'enemy_sprite': 'sprite_priest'}}


class World:

    def __init__(self, dims, character, world_size, number_of_players):

        self.dims = dims
        self.name = character
        self.dir_dict = {'UP': 0, 'DOWN': 0, 'LEFT': 0, 'RIGHT': 0}
        self.number_of_players = number_of_players
        self.world_size = world_size

        self.coin_list = []
        self.enemy_list = []
        player_sprite = CHARACTERS[character]['player_sprite']
        self.allsprites = pg.sprite.RenderPlain()

        self.world = pg.Surface(self.dims)
        self.world = self.world.convert()
        self.shop = Shop(player_sprite, (60, 60))

        self.money = 0
        self.font_money = pg.font.Font(os.path.join(DATA_DIR, 'Amatic-Bold.ttf'), 20 * 3)
        self.text_money = self.font_money.render(str(self.money), 1, (220, 20, 60))

        self.ouch_sound = load_sound("ouch.wav")
        self.ouch_sound.set_volume(0.2)
        self.coin_sound = load_sound("coin_sound.wav")
        self.coin_sound.set_volume(0.05)

        self.background = Entity(helper.create_background(self.name, self.world_size, self.number_of_players), (0, 0))
        self.pit = Entity({"DOWN": self.name[0] + 'pit'}, (0, 0))
        self.sprite_dict = {}
        self.create_sprite_dict(player_sprite)
        self.player = Entity(self.sprite_dict, (self.world.get_width() / 2, self.world.get_height() / 2),
                             lives=3)

        self.draw_world()

    def start(self):
        self.gen_enemy()
        # spawns 5 coin entities
        for i in range(5):
            self.gen_coin()
        self.player.image = 'DOWN'

    def get_name(self):
        return self.name

    def init_character(self, name):
        self.name = name
        self.background = Entity(helper.create_background(self.name, self.world_size, self.number_of_players), (0, 0))
        self.create_sprite_dict(CHARACTERS[name]['player_sprite'])
        self.player.set_sprite_dict(self.sprite_dict)
        for enemy in self.enemy_list:
            enemy_dict = helper.create_sprite_dict(CHARACTERS[name]['enemy_sprite'])
            enemy.set_sprite_dict(enemy_dict)
        self.pit.set_sprite_dict({"DOWN": self.name[0] + 'pit'})

    def draw_pit(self):
        x, y = self.background.position
        x -= self.pit.get_width() / 2
        y -= self.pit.get_height() / 2
        x += (8.5*48)
        y += (4.25*48)
        self.pit.set_position((x, y))
        self.pit.draw(self.world, self.dims)

    def create_sprite_dict(self, player_sprite):
        self.sprite_dict.update({"LEFT": player_sprite + "_left"})
        self.sprite_dict.update({"RIGHT": player_sprite + "_right"})
        self.sprite_dict.update({"UP": player_sprite + "_back"})
        self.sprite_dict.update({"DOWN": player_sprite + "_front"})
        self.sprite_dict.update({"DEAD": player_sprite + "_dead"})

    def update_world(self):
        self.player_update()
        for sprite in self.allsprites:
            sprite.move(self.world_size)
        self.draw_world()

    def draw_world(self):

        self.background.draw(self.world, self.dims)
        if not self.check_alive():
            self.player.image = "DEAD"
            self.world.blit(self.player.get_sprite(), self.player.get_position())

        for sprite in self.allsprites:
            sprite.draw(self.world, self.dims)

        if self.check_alive():
            self.world.blit(self.player.get_sprite(), self.player.get_position())
        self.draw_pit()

        self.update_gui()
        pg.display.flip()

    def draw_select(self):
        font_select = pg.font.Font(os.path.join(DATA_DIR, 'Amatic-Bold.ttf'), 36 * 3)
        text_select = font_select.render('Choose Your Character', 1, (220, 20, 60))
        textpos_select = text_select.get_rect(centerx=self.get_width() / 2,
                                              centery=self.get_height() / 5)
        self.world.blit(text_select, textpos_select)

        font_space_to_begin = pg.font.Font(os.path.join(DATA_DIR, 'AmaticSC-Regular.ttf'), 16 * 3)
        text_space_to_begin = font_space_to_begin.render("Press Spacebar to Start", 1, (220, 20, 60))
        textpos_space_to_begin = text_space_to_begin.get_rect(centerx=self.get_width() / 2,
                                                              centery=self.get_height() / 1.2)
        self.world.blit(text_space_to_begin, textpos_space_to_begin)

    def add_entity(self, sprite_dict, pos, ai=None, speed=5):
        entity = Entity(sprite_dict, pos, ai=ai, speed=speed)
        self.allsprites.add(entity)
        return entity

    def get_surface(self):
        return self.world

    def player_update(self):
        self.player.move(self.world_size)

        for coin in self.coin_list:
            if self.player.check_collision(coin):
                self.money += 1
                self.coin_sound.play()
                self.reset_entity(coin)
        for enemy in self.enemy_list:
            if self.player.check_collision(enemy) and self.player.is_alive():
                self.reset_entity(enemy)
                self.player.lives -= 1
                self.ouch_sound.play()

    def update_gui(self):
        self.update_lives()
        self.update_shop()
        self.update_money()

    def update_money(self):
        self.text_money = self.font_money.render(str(self.money), 1, (220, 20, 60))
        textpos_money = self.text_money.get_rect(topright=((self.world.get_width() - 20), 20))
        pg.draw.circle(self.world, GOLD, textpos_money.center, 40)
        self.world.blit(self.text_money, textpos_money)

    def update_shop(self):
        self.shop.draw_shop()

        self.world.blit(self.shop.shop_surface, (0, 0))

    def update_lives(self):
        full_heart = LOADED_IMAGES["sprite_heart"]
        empty_heart = LOADED_IMAGES["sprite_heart_empty"]

        heart_positions = [self.world.get_width() / 2 + full_heart.get_rect().width * -1.5,
                           self.world.get_width() / 2 + full_heart.get_rect().width * -0.5,
                           self.world.get_width() / 2 + full_heart.get_rect().width * 0.5]

        counter = 0
        for heart_pos in heart_positions:
            if self.player.lives > counter:
                self.world.blit(full_heart, [int(heart_pos), 0])
            else:
                self.world.blit(empty_heart, [int(heart_pos), 0])
            counter += 1

    def check_alive(self):
        return self.player.is_alive()

    def move(self):
        if not self.check_alive():
            return
        x = self.dir_dict['LEFT'] - self.dir_dict['RIGHT']
        y = self.dir_dict['UP'] - self.dir_dict['DOWN']
        norm = (x ** 2 + y ** 2) ** 0.5
        norm = norm / 2  # Double move speed
        if norm == 0:
            return
        x = x / norm
        y = y / norm
        for sprite in self.allsprites:
            # print(x,y)
            sprite.slide([x, y])
            self.player.set_dir([x, y])
        self.background.slide([x, y])

    def reset_entity(self, entity):
        side = random.randint(0, 1)
        ran = random.random()
        height = entity.get_height()
        width = entity.get_width()
        if side == 0:
            entity.set_position([ran*self.dims[0], -height/2])
        else:
            entity.set_position([-width/2, ran*self.dims[1]])

    def gen_coin(self):
        coin_sprite_dict = {"DOWN": "sprite_coin"}
        side = random.randint(0, 3)
        ran = random.random()
        if side == 0:
            coin = self.add_entity(coin_sprite_dict, (ran*self.dims[0], 1))
            self.coin_list.append(coin)
        else:
            coin = self.add_entity(coin_sprite_dict, (1, ran*self.dims[1]))
            self.coin_list.append(coin)

    def gen_enemy(self, speed=1):
        enemy_sprite_dict = helper.create_sprite_dict(CHARACTERS[self.name]['enemy_sprite'])
        pos = random.choice([(random.randint(1, self.dims[0]), 0), (0, random.randint(1, self.dims[1]))])
        enemy = self.add_entity(enemy_sprite_dict,
                                pos, ai='follow',
                                speed=speed)
        enemy.update_info({'target': self.player, 'me': enemy})
        self.enemy_list.append(enemy)

    def set_dir(self, key, val):
        if type(val) == int:
            self.dir_dict[key] = val
        elif type(val) == tuple:
            if val[0] == 1:
                self.dir_dict['RIGHT'] = 1
            elif val[0] == -1:
                self.dir_dict['LEFT'] = 1
            else:
                self.dir_dict['RIGHT'] = 0
                self.dir_dict['LEFT'] = 0
            if val[1] == 1:
                self.dir_dict['UP'] = 1
            elif val[1] == -1:
                self.dir_dict['DOWN'] = 1
            else:
                self.dir_dict['UP'] = 0
                self.dir_dict['DOWN'] = 0
        elif type(val) == float:
            if key % 2 == 0:
                if val > 0:
                    self.dir_dict['LEFT'] = 0
                    self.dir_dict['RIGHT'] = abs(val)
                else:
                    self.dir_dict['LEFT'] = abs(val)
                    self.dir_dict['RIGHT'] = 0
            elif key % 2 != 0:
                if val > 0:
                    self.dir_dict['UP'] = 0
                    self.dir_dict['DOWN'] = abs(val)
                else:
                    self.dir_dict['UP'] = abs(val)
                    self.dir_dict['DOWN'] = 0

    def get_dir(self):
        return self.dir_dict

    def activate_power(self, power_name):
        if power_name == "speed":
            for enemy in self.enemy_list:
                enemy.speed += 0.3

        elif power_name == "more":
            self.gen_enemy()

        elif power_name == "heal":
            self.player.lives += 1

    def pay_for_power(self, power_name):
        if not self.shop.open or (power_name == "heal" and self.player.max_lives == self.player.lives):
            return False
        else:
            shop_power = self.shop.get_shopcard(power_name)
            if self.money >= shop_power.price:
                self.money -= shop_power.price
                self.shop.increase_price_of_power(power_name)
                return True
            return False

    def get_width(self):
        return self.dims[0]

    def get_height(self):
        return self.dims[1]

    def reset(self):
        self.player.lives = 3
        self.money = 0
        for index, enemy in enumerate(self.enemy_list):
            del self.enemy_list[index]
        self.allsprites.empty()
        self.shop.close_shop()
