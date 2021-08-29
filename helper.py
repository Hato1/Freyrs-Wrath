import os
import pygame as pg
from pygame.locals import *
import pygame.surfarray as surfarray
from pygame.compat import geterror

import random

WIN_SIZE = ((512*3)+2, (288*3)+2)


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
    (os.path.join(DATA_DIR, 'sprite_priest', 'sprite_priest_dead.png'), 1),
    (os.path.join(DATA_DIR, 'sprite_viking', 'sprite_viking_front.png'), 1),
    (os.path.join(DATA_DIR, 'sprite_viking', 'sprite_viking_back.png'), 1),
    (os.path.join(DATA_DIR, 'sprite_viking', 'sprite_viking_right.png'), 1),
    (os.path.join(DATA_DIR, 'sprite_viking', 'sprite_viking_left.png'), 1),
    (os.path.join(DATA_DIR, 'sprite_viking', 'sprite_viking_dead.png'), 1),
    (os.path.join(DATA_DIR, 'sprite_demon', 'sprite_demon_front.png'), 1),
    (os.path.join(DATA_DIR, 'sprite_demon', 'sprite_demon_front.png'), 1),
    (os.path.join(DATA_DIR, 'sprite_demon', 'sprite_demon_back.png'), 1),
    (os.path.join(DATA_DIR, 'sprite_demon', 'sprite_demon_left.png'), 1),
    (os.path.join(DATA_DIR, 'sprite_demon', 'sprite_demon_right.png'), 1),
    (os.path.join(DATA_DIR, 'sprite_demon', 'sprite_demon_dead.png'), 1),
    (os.path.join(DATA_DIR, 'sprite_farmer', 'sprite_farmer_front.png'), 1),
    (os.path.join(DATA_DIR, 'sprite_farmer', 'sprite_farmer_back.png'), 1),
    (os.path.join(DATA_DIR, 'sprite_farmer', 'sprite_farmer_left.png'), 1),
    (os.path.join(DATA_DIR, 'sprite_farmer', 'sprite_farmer_right.png'), 1),
    (os.path.join(DATA_DIR, 'sprite_farmer', 'sprite_farmer_dead.png'), 1),
    (os.path.join(DATA_DIR, 'sprite_coin', 'sprite_coin.png'), 1),
    (os.path.join(DATA_DIR, 'sprite_shop_blank', 'more.png'), 2),
    (os.path.join(DATA_DIR, 'sprite_shop_blank', 'speed.png'), 2),
    (os.path.join(DATA_DIR, 'sprite_shop_blank', 'heal.png'), 2),
    (os.path.join(DATA_DIR, 'sprite_shop_blank', 'shop_icon.png'), 2),
    (os.path.join(DATA_DIR, 'sprite_heart.png'), 0.1),
    (os.path.join(DATA_DIR, 'sprite_heart_empty.png'), 0.1)
]

tilesets = os.path.join(DATA_DIR, 'tilesets')
for i in os.listdir(tilesets):
    if os.path.isdir(os.path.join(tilesets, i)):
        for j in os.listdir(os.path.join(tilesets, i)):
            if j.endswith('png'):
                scale = 3/16
                if j[1:].startswith('pit'):
                    if j == 'Fpit.png':
                        scale = scale * 2.5
                    elif j == "Dpit.png":
                        scale = scale * 1.5
                    elif j == "Vpit.png":
                        scale = scale * 2.9
                    elif j == "Ppit.png":
                        scale = scale * 2.7
                IMAGE_PATHS.append((os.path.join(DATA_DIR, 'tilesets', i, j), scale))
            elif j == "Environment":
                for k in os.listdir(os.path.join(tilesets, i, j)):
                    if k.endswith('png'):
                        IMAGE_PATHS.append((os.path.join(DATA_DIR, 'tilesets', i, j, k), scale))
LOADED_IMAGES = {}


def load_image(name, colorkey=(0, 0, 0, 255)):
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


def create_background(name, world_size, number_of_players):
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
    if number_of_players == 0:
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
        for i in range(len(roads)):
            while len(roads[i]) < int(world_size[0]):
                roads[i] = roads[i] + roads[i][-1]
        while len(roads) < int(world_size[1]):
            roads.append('           |    ' + ' ' * (int(world_size[0])-16))
    if number_of_players == 2:
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
    feature_counts = {
        'FARMER': 22,
        'DEMON': 19,
        'PRIEST': 17,
        'VIKING': 21
        }
    dims = (world_size[0]//48, world_size[1]//48)
    bg = pg.Surface(world_size)
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
    for i in range(dims[0]-1):
        for j in range(dims[1]-1):
            if roads[j][i] == " " and random.random() > 0.95:
                num = str(random.randint(1, feature_counts[name]))
                if len(num) == 1:
                    num = '0' + num
                img = LOADED_IMAGES[name[0] + "E" + num]
                #if name[0] + "E" + num == "DE19":
                #    print(LOADED_IMAGES[name[0] + "E" + num].get_width(), LOADED_IMAGES[name[0] + "E" + num].get_height())
                bg.blit(img, (i*48 + img.get_width(), j*48 + img.get_height()))

    LOADED_IMAGES.update({name: bg})
    return {"DOWN": name}


def create_sprite_dict(sprite):
    sprite_dict = {}
    sprite_dict["LEFT"] = sprite + "_left"
    sprite_dict["RIGHT"] = sprite + "_right"
    sprite_dict["UP"] = sprite + "_back"
    sprite_dict["DOWN"] = sprite + "_front"
    return sprite_dict

