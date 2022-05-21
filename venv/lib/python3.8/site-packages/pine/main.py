try:
    from constants import *
    import sys
    import os
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
    import pygame
    import pygame.freetype
    from pygame.locals import *
    from rules import home_screen
except ImportError as err:
    print("couldn't load module. %s" % (err))
    sys.exit(2)

pygame.freetype.init()
FONT = pygame.freetype.Font(None, size=32)

class home_screen:
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(GREEN)

    titlefont = pygame.font.Font(None, 124)
    title = titlefont.render("Pineapple", 1, LIME)
    titlepos = title.get_rect()
    titlepos.top = SPACE * 3
    titlepos.centerx = background.get_rect().centerx

    play_1_rect = Rect((0, 0, BUTTON_WIDTH, BUTTON_HEIGHT))
    play_1_rect.centerx = background.get_rect().centerx
    play_1_rect.centery = background.get_rect().centery
    button1 = PygButton(play_1_rect, caption='One Player')

    play_2_rect = Rect((0, 0, BUTTON_WIDTH, BUTTON_HEIGHT))
    play_2_rect.centerx = background.get_rect().centerx
    play_2_rect.centery = background.get_rect().centery + BUTTON_HEIGHT + SPACE
    button2 = PygButton(play_2_rect, caption='Two Players')

    play_3_rect = Rect((0, 0, BUTTON_WIDTH, BUTTON_HEIGHT))
    play_3_rect.centerx = background.get_rect().centerx
    play_3_rect.centery = background.get_rect().centery + (BUTTON_HEIGHT + SPACE) * 2
    button3 = PygButton(play_3_rect, caption='Three Players')

    clock = pygame.time.Clock()

    players = None
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif 'click' in button1.handleEvent(event):
                players = (Player('Player1'),)
            elif 'click' in button2.handleEvent(event):
                players = (Player('Player1'), Player('Player2'))
            elif 'click' in button3.handleEvent(event):
                players = (Player('Player1'), Player('Player2'), Player('Player3'))
        if players:
            players = play(screen, players)
        else:
            screen.blit(background, (0, 0))
            screen.blit(title, titlepos)
            button1.draw(screen)
            button2.draw(screen)
            button3.draw(screen)
            pygame.display.update()
            clock.tick(FPS)

def main():
    pygame.init()
    logo = pygame.image.load(os.path.join('..', 'images', 'PineLogo.png'))
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Pineapple")

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    try:
        home_screen(screen)
    except SystemExit:
        pygame.display.quit()

