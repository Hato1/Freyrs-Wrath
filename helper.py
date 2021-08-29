import os
import pygame as pg
from pygame.locals import *
import pygame.surfarray as surfarray
# import numpy as np
from pygame.compat import geterror

import random

PLAYERCOUNT = 4
WIN_SIZE = ((512*3)+2, (288*3)+2)

WORLD_SIZE = ((512*3)//2, (288*3))
if PLAYERCOUNT > 2:
    WORLD_SIZE = ((512*3)//2, (288*3)//2)
# WORLD_DIMS = (255*2, 288*2)

# tilesize = 512/8 = 32
# 2 players: 16 accross 18 high
# 3-4 players: 16 accross 9 high

MAIN_DIR = os.path.split(os.path.abspath(__file__))[0]
DATA_DIR = os.path.join(MAIN_DIR, "data")
IMAGE_PATHS = [
    (os.path.join(DATA_DIR, 'sprite_priest', 'sprite_priest_front.png'), 1),
    (os.path.join(DATA_DIR, 'sprite_priest', 'sprite_priest_back.png'), 1),
    (os.path.join(DATA_DIR, 'sprite_priest', 'sprite_priest_right.png'), 1),
    (os.path.join(DATA_DIR, 'sprite_priest', 'sprite_priest_left.png'), 1),
    (os.path.join(DATA_DIR, 'sprite_viking', 'sprite_viking_front.png'), 1),
    (os.path.join(DATA_DIR, 'sprite_viking', 'sprite_viking_back.png'), 1),
    (os.path.join(DATA_DIR, 'sprite_viking', 'sprite_viking_right.png'), 1),
    (os.path.join(DATA_DIR, 'sprite_viking', 'sprite_viking_left.png'), 1),
    (os.path.join(DATA_DIR, 'sprite_demon', 'sprite_demon_front.png'), 1),
    (os.path.join(DATA_DIR, 'sprite_demon', 'sprite_demon_front.png'), 1),
    (os.path.join(DATA_DIR, 'sprite_demon', 'sprite_demon_back.png'), 1),
    (os.path.join(DATA_DIR, 'sprite_demon', 'sprite_demon_left.png'), 1),
    (os.path.join(DATA_DIR, 'sprite_demon', 'sprite_demon_right.png'), 1),
    (os.path.join(DATA_DIR, 'sprite_farmer', 'sprite_farmer_front.png'), 1),
    (os.path.join(DATA_DIR, 'sprite_farmer', 'sprite_farmer_back.png'), 1),
    (os.path.join(DATA_DIR, 'sprite_farmer', 'sprite_farmer_left.png'), 1),
    (os.path.join(DATA_DIR, 'sprite_farmer', 'sprite_farmer_right.png'), 1),
    (os.path.join(DATA_DIR, 'sprite_coin', 'sprite_coin.png'), 1),
    (os.path.join(DATA_DIR, 'sprite_shop', 'shop_icon_p.png'), 2),
    (os.path.join(DATA_DIR, 'sprite_shop', 'shop_ability_f.png'), 2),
    (os.path.join(DATA_DIR, 'sprite_shop', 'shop_ability_g.png'), 2),
    (os.path.join(DATA_DIR, 'sprite_shop', 'shop_ability_h.png'), 2),
    (os.path.join(DATA_DIR, 'sprite_shop', 'shop_ability_k.png'), 2),
    (os.path.join(DATA_DIR, 'sprite_shop', 'shop_ability_l.png'), 2),
    (os.path.join(DATA_DIR, 'sprite_shop', 'shop_ability_;.png'), 2),
    (os.path.join(DATA_DIR, 'sprite_shop', 'shop_icon_q.png'), 2),
    (os.path.join(DATA_DIR, 'dirt.png'), 0.2),
    (os.path.join(DATA_DIR, 'sand.png'), 0.4),
    (os.path.join(DATA_DIR, 'ground.jpg'), 0.5),
    (os.path.join(DATA_DIR, 'sprite_heart.png'), 0.1),
    (os.path.join(DATA_DIR, 'sprite_heart_empty.png'), 0.1)
]

tilesets = os.path.join(DATA_DIR, 'tilesets')
for i in os.listdir(tilesets):
    if os.path.isdir(os.path.join(tilesets, i)):
        for j in os.listdir(os.path.join(tilesets, i)):
            print(j)
            if j.endswith('png'):
                scale = 3/16
                if j in ['Vpit.png', 'Fpit.png']:
                    scale = scale * 2.5
                elif j == "Dpit.png":
                    scale = scale * 1.5
                IMAGE_PATHS.append((os.path.join(DATA_DIR, 'tilesets', i, j), scale))
LOADED_IMAGES = {}


def load_image(name, colorkey=(0,0,0,255)):
    fullname = os.path.join(DATA_DIR, name)
    try:
        image = pg.image.load(fullname)
    except pg.error:
        print("Cannot load image:", fullname)
        raise SystemExit(str(geterror()))
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pg.RLEACCEL)
    return image, image.get_rect()


def load_sound(name):
    class NoneSound:
        def play(self):
            pass

    if not pg.mixer or not pg.mixer.get_init():
        return NoneSound()
    fullname = os.path.join(DATA_DIR, name)
    try:
        sound = pg.mixer.Sound(fullname)
    except pg.error:
        print("Cannot load sound: %s" % fullname)
        raise SystemExit(str(geterror()))
    return sound


def load_all_images():
    for image_path, scale in IMAGE_PATHS:
        image_name = os.path.basename(image_path).split('.')[0]
        img = load_image(image_path)
        dims = (int(img[0].get_height()*scale), int(img[0].get_width()*scale))
        img = (pg.transform.scale(img[0], dims), img[1])
        LOADED_IMAGES.update({image_name: img[0]})
    make_images()


def create_background(name):
    # return {"DOWN": 'sand'}
    # U = UR
    # R = RD
    # D = DL
    # L = LU
    roads = [
        '           |    ',
        '           |    ',
        '---D    R--L  R-',
        '   U-D 123    | ',
        '     U-456----L ',
        '       789      ',
        '        |       ',
        '        U--D    ',
        '           |    '
        ]
    if PLAYERCOUNT < 3:
        roads = [
            '           |    ',
            '           |    ',
            '---D    R--L  R-',
            '   U-D 123    | ',
            '     U-456----L ',
            '       789      ',
            '        |       ',
            '        U--D    ',
            '           |    ',
            '           |    ',
            '           |    ',
            '           |    ',
            '           |    ',
            '           |    ',
            '           |    ',
            '           |    ',
            '           |    ',
            '           |    ',
            ]
    dims = (WORLD_SIZE[0]//48, WORLD_SIZE[1]//48)
    bg = pg.Surface(WORLD_SIZE)
    for i in range(dims[0]):
        for j in range(dims[1]):
            if roads[j][i] == ' ':
                tile = random.choice(['43', '52'])
            elif roads[j][i] == '-':
                tile = '41'
            elif roads[j][i] == '|':
                tile = '38'
            elif roads[j][i] == 'U':
                tile = '34'
            elif roads[j][i] == 'R':
                tile = '28'
            elif roads[j][i] == 'L':
                tile = '36'
            elif roads[j][i] == 'D':
                tile = '30'
            elif roads[j][i] == "2":
                tile = '11'
            elif roads[j][i] == "4":
                tile = '13'
            elif roads[j][i] == "6":
                tile = '15'
            elif roads[j][i] == "8":
                tile = '17'
            elif roads[j][i].isdigit():
                tile = str(18+int(roads[j][i]))

            bg.blit(LOADED_IMAGES[name[0] + tile], (i*48, j*48))
    x = LOADED_IMAGES[name[0] + 'pit'].get_rect(center=(8.5*48, 4.25*48))
    bg.blit(LOADED_IMAGES[name[0] + 'pit'], x)
    # bg.blit(LOADED_IMAGES[name[0] + 'pit'], (8*48, 4*48))
    LOADED_IMAGES.update({name: bg})
    return {"DOWN": name}


def create_sprite_dict(sprite):
    sprite_dict = {}
    sprite_dict["LEFT"] = sprite + "_left"
    sprite_dict["RIGHT"] = sprite + "_right"
    sprite_dict["UP"] = sprite + "_back"
    sprite_dict["DOWN"] = sprite + "_front"
    return sprite_dict


def make_images():
    pass
    # brown = np.zeros((16, 18, 3))
    # brown[:] = (158, 119, 119)
    # # random boolean mask for which values will be changed
    # mask = np.random.randint(0, 5, size=(16, 8, 3))

    # # random matrix the same shape of your data
    # # r = np.random.rand(*x.shape)*np.max(x)
    # dark = np.zeros((16, 18, 3))
    # dark[:] = (111, 76, 91)
    # # dark[] = (255, 255, 255)

    # # use your mask to replace values in your input array
    # brown[mask] = dark[mask]

    # brown = pg.surfarray.make_surface(brown)
    # brown = pg.transform.scale(brown, (256, 288))
    # LOADED_IMAGES.update({'background': (brown, brown)})
