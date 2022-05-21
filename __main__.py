try:
    import sys
    import os
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
    import pygame
    import pygame.freetype
    from pygame.locals import *
    from pine.rules import home_screen, win_screen, play
except ImportError as err:
    print("couldn't load module. %s" % (err))
    sys.exit(2)

pygame.freetype.init()
FONT = pygame.freetype.Font(None, size=32)
FPS = 30
SPACE = 10
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
CARD_WIDTH = 70
CARD_HEIGHT = 105
BOARD_WIDTH = (CARD_WIDTH + SPACE) * 5 - SPACE
BOARD_HEIGHT = SCREEN_HEIGHT
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
GREEN = (  0,  60,   0)
LIME  = ( 50, 205,  50)
RED   = (255,   0,   0)


def main():
    pygame.init()
    logo = pygame.image.load(os.path.join('images', 'PineLogo.png'))
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Pineapple")

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    try:
        home_screen(screen)
    except SystemExit:
        pygame.display.quit()

if __name__=="__main__":
    main()
