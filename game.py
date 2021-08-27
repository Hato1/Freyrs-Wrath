import os
import pygame as pg
from pygame.locals import *
from pygame.compat import geterror

if not pg.font:
    print("Warning, fonts disabled")
if not pg.mixer:
    print("Warning, sound disabled")

MAIN_DIR = os.path.split(os.path.abspath(__file__))[0]
DATA_DIR = os.path.join(MAIN_DIR, "data")

MENU = 1
GAME = 2
END = 3
GAME_STATE = MENU
WHITE = (255, 255, 255)


# functions to create our resources
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


def main():
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the function returns."""
    # Initialize Everything
    pg.init()
    screen = pg.display.set_mode((512, 288), pg.SCALED | pg.RESIZABLE)
    pg.display.set_caption("Prototype")

    # Create The Backgound
    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill((67, 112, 173))

    # Put Text On The Background, Centered
    if pg.font:
        font = pg.font.Font(os.path.join(DATA_DIR, 'Sadtember.ttf'), 36*3)
        text = font.render("Hostile", 1, (220, 20, 60))
        textpos = text.get_rect(centerx=background.get_width() / 2, centery=background.get_height() / 2)
        background.blit(text, textpos)

    # Add a rectangle
    pg.draw.rect(background, (100, 0, 100), pg.Rect(30, 30, 60, 60))

    # Display The Background
    screen.blit(background, (0, 0))
    pg.display.flip()  # Flipping display is recommended practice to be sure display updates???

    # Prepare Game Objects
    clock = pg.time.Clock()
    allsprites = pg.sprite.RenderPlain(())

    set_menu(background)

    # Main Loop
    going = True
    while going:
        clock.tick(60)

        if GAME_STATE == MENU:
            menu_loop(background)

            # Handle Input Events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                going = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                going = False

            elif event.type == pg.KEYDOWN and event.key == pg.K_f:
                pg.display.toggle_fullscreen()
            elif event.type == pg.VIDEORESIZE:
                pg.display._resize_event(event)

        allsprites.update()

            # Draw Everything
        screen.blit(background, (0, 0))
        allsprites.draw(screen)
        pg.display.flip()

    pg.quit()

def game_loop():
    pass

def menu_loop(background):
    pass

def set_menu(background):
    background.fill(WHITE)
    write_menu_text(background)


def write_menu_text(background):
    font_title = pg.font.Font(os.path.join(DATA_DIR, 'Amatic-Bold.ttf'), 36 * 3)
    text_title = font_title.render("Name of the Game", 1, (220, 20, 60))
    textpos_title = text_title.get_rect(centerx=background.get_width() / 2, centery=background.get_height() / 4)
    background.blit(text_title, textpos_title)

    font_team = pg.font.Font(os.path.join(DATA_DIR, 'Amatic-Bold.ttf'), 12 * 3)
    text_team = font_team.render("Fishing Minigame Metaphor", 1, (220, 20, 60))
    textpos_team = text_team.get_rect(centerx=background.get_width() / 2, centery=background.get_height() / 2)
    background.blit(text_team, textpos_team)

# Game Over

# this calls the 'main' function when this script is executed
main()