import os
import pygame as pg
from pygame.compat import geterror

MAIN_DIR = os.path.split(os.path.abspath(__file__))[0]
DATA_DIR = os.path.join(MAIN_DIR, "data")
IMAGE_PATHS = [
    (os.path.join(DATA_DIR, 'sprite_priest/sprite_priest_front.png'), 1),
    (os.path.join(DATA_DIR, 'sprite_priest/sprite_priest_back.png'), 1),
    (os.path.join(DATA_DIR, 'sprite_priest/sprite_priest_right.png'), 1),
    (os.path.join(DATA_DIR, 'sprite_priest/sprite_priest_left.png'), 1),
    (os.path.join(DATA_DIR, 'sprite_viking/sprite_viking_front.png'), 1),
    (os.path.join(DATA_DIR, 'sprite_viking/sprite_viking_back.png'), 1),
    (os.path.join(DATA_DIR, 'sprite_viking/sprite_viking_right.png'), 1),
    (os.path.join(DATA_DIR, 'sprite_viking/sprite_viking_left.png'), 1),
    (os.path.join(DATA_DIR, 'sprite_coin/sprite_coin.png'), 1),
    (os.path.join(DATA_DIR, 'sprite_shop/shop_icon_p.png'), 1),
    (os.path.join(DATA_DIR, 'sprite_shop/shop_ability_f.png'), 1),
    (os.path.join(DATA_DIR, 'sprite_shop/shop_ability_g.png'), 1),
    (os.path.join(DATA_DIR, 'sprite_shop/shop_ability_h.png'), 1),
    (os.path.join(DATA_DIR, 'sprite_shop/shop_ability_k.png'), 1),
    (os.path.join(DATA_DIR, 'sprite_shop/shop_ability_l.png'), 1),
    (os.path.join(DATA_DIR, 'sprite_shop/shop_ability_;.png'), 1),
    (os.path.join(DATA_DIR, 'sprite_shop/shop_icon_q.png'), 1),
    (os.path.join(DATA_DIR, 'sprite_priest/sprite_priest_front.png'), 1),
    (os.path.join(DATA_DIR, 'sprite_priest/sprite_priest_back.png'), 1),
    (os.path.join(DATA_DIR, 'sprite_priest/sprite_priest_left.png'), 1),
    (os.path.join(DATA_DIR, 'sprite_priest/sprite_priest_right.png'), 1),
    (os.path.join(DATA_DIR, 'sprite_coin/sprite_coin.png'), 1),
    (os.path.join(DATA_DIR, 'dirt.png'), 0.1),
    (os.path.join(DATA_DIR, 'sand.png'), 0.1),
    (os.path.join(DATA_DIR, 'ground.jpg'), 0.5),
]
LOADED_IMAGES = {}


def load_image(name, colorkey=-1):
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
        image_name = image_path.split('/')[-1]
        image_name = image_name.split('.')[0]
        img = load_image(image_path)
        dims = (int(img[0].get_height()*scale), int(img[0].get_width()*scale))
        img = (pg.transform.scale(img[0], dims).convert(), img[1])
        LOADED_IMAGES.update({image_name: img})
