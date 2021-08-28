import os
import pygame as pg
from pygame.locals import *
import pygame.surfarray as surfarray
# import numpy as np
from pygame.compat import geterror

PLAYERCOUNT = 2
WIN_SIZE = (512*2, 288*2)

WORLD_SIZE = ((WIN_SIZE[0]-2)/2, WIN_SIZE[1])
if PLAYERCOUNT > 2:
    WORLD_SIZE = ((WIN_SIZE[0]-2)/2, WIN_SIZE[1]/2)
# WORLD_DIMS = (255*2, 288*2)

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
    (os.path.join(DATA_DIR, 'sprite_coin', 'sprite_coin.png'), 1),
    (os.path.join(DATA_DIR, 'sprite_shop', 'shop_icon_p.png'), 1),
    (os.path.join(DATA_DIR, 'sprite_shop', 'shop_ability_f.png'), 1),
    (os.path.join(DATA_DIR, 'sprite_shop', 'shop_ability_g.png'), 1),
    (os.path.join(DATA_DIR, 'sprite_shop', 'shop_ability_h.png'), 1),
    (os.path.join(DATA_DIR, 'sprite_shop', 'shop_ability_k.png'), 1),
    (os.path.join(DATA_DIR, 'sprite_shop', 'shop_ability_l.png'), 1),
    (os.path.join(DATA_DIR, 'sprite_shop', 'shop_ability_;.png'), 1),
    (os.path.join(DATA_DIR, 'sprite_shop', 'shop_icon_q.png'), 1),
    (os.path.join(DATA_DIR, 'sprite_demon', 'sprite_demon_front.png'), 1),
    (os.path.join(DATA_DIR, 'sprite_demon', 'sprite_demon_back.png'), 1),
    (os.path.join(DATA_DIR, 'sprite_demon', 'sprite_demon_left.png'), 1),
    (os.path.join(DATA_DIR, 'sprite_demon', 'sprite_demon_right.png'), 1),
    (os.path.join(DATA_DIR, 'sprite_coin', 'sprite_coin.png'), 1),
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
            if j.endswith('png'):
                IMAGE_PATHS.append((os.path.join(DATA_DIR, 'tilesets', i, j), 1))
LOADED_IMAGES = {}


def load_image(name, colorkey=(0, 0, 0, 255)):
    fullname = os.path.join(DATA_DIR, name)
    try:
        image = pg.image.load(fullname)
    except pg.error:
        print("Cannot load image:", fullname)
        raise SystemExit(str(geterror()))
    image = image.convert()
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
        img = (pg.transform.scale(img[0], dims).convert(), img[1])
        LOADED_IMAGES.update({image_name: img[0]})
    make_images()


def make_images():
    pass
    #brown = np.zeros((16, 18, 3))
    #brown[:] = (158, 119, 119)
    ## random boolean mask for which values will be changed
    #mask = np.random.randint(0, 5, size=(16, 8, 3))

    ## random matrix the same shape of your data
    ## r = np.random.rand(*x.shape)*np.max(x)
    #dark = np.zeros((16, 18, 3))
    #dark[:] = (111, 76, 91)
    ## dark[] = (255, 255, 255)

    ## use your mask to replace values in your input array
    #brown[mask] = dark[mask]

    #brown = pg.surfarray.make_surface(brown)
    #brown = pg.transform.scale(brown, (256, 288))
    #LOADED_IMAGES.update({'background': (brown, brown)})
