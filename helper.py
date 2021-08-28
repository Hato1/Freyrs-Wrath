import os
import pygame as pg
from pygame.compat import geterror

MAIN_DIR = os.path.split(os.path.abspath(__file__))[0]
DATA_DIR = os.path.join(MAIN_DIR, "data")
IMAGE_PATHS = [
    os.path.join(DATA_DIR, 'sprite_shop/sprite_shop0.png'),
    os.path.join(DATA_DIR, 'sprite_shop/sprite_shop1.png'),
    os.path.join(DATA_DIR, 'sprite_shop/sprite_shop2.png'),
    os.path.join(DATA_DIR, 'sprite_shop/sprite_shop3.png'),
    os.path.join(DATA_DIR, 'sprite_shop/sprite_shop4.png'),
    os.path.join(DATA_DIR, 'sprite_shop/sprite_shop5.png')
]
LOADED_IMAGES = {}

def load_image(name, colorkey=None):
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
    for image_path in IMAGE_PATHS:
        image_name = image_path.split('/')[-1]
        image_name = image_name.split('.')[0]
        LOADED_IMAGES.update({image_name: load_image(image_path)})
