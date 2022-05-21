try:
    import sys
    import os
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
    import pygame
    import pygame.freetype
    from pygame.locals import *
    from .button import PygButton
    from .player import Player
    from .card import Deck
    from .board import Board
    from .score import score_boards, winner
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
BUTTON_HEIGHT = 40
BUTTON_WIDTH = 120


def play(screen, players):
    Board.deck = Deck()
    boards = [Board(player) for player in players]

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(GREEN)

    next_rect = Rect((SCREEN_WIDTH - BUTTON_WIDTH - SPACE, SCREEN_HEIGHT / 2, BUTTON_WIDTH, BUTTON_HEIGHT))
    next_button = PygButton(next_rect, caption="End Turn")
    next_button.visible = False

    show1_rect = Rect((SCREEN_WIDTH - BUTTON_WIDTH - SPACE, SPACE * 2, BUTTON_WIDTH, BUTTON_HEIGHT))
    show1_button = PygButton(show1_rect)
    show1_button.visible = False

    show2_rect = Rect(
        (SCREEN_WIDTH - BUTTON_WIDTH - SPACE, BUTTON_HEIGHT + SPACE * 3, BUTTON_WIDTH, BUTTON_HEIGHT)
    )
    show2_button = PygButton(show2_rect)
    show2_button.visible = False

    if len(boards) > 1:
        show1_button.visible = True
    if len(boards) > 2:
        show2_button.visible = True

    clock = pygame.time.Clock()

    for turns in range(5):
        for play_board in boards:
            other_boards = [oth_board for oth_board in boards if oth_board is not play_board]
            if show1_button.visible:
                show1_button.def_caption = "Show " + other_boards[0].player.name
            if show2_button.visible:
                show2_button.def_caption = "Show " + other_boards[1].player.name
            show_board = play_board
            running = True
            while running:
                if turns == 0:
                    if len(play_board.hand.cards) == 0:
                         next_button.visible = True
                elif len(play_board.hand.cards) > 1:
                    next_button.visible = False
                    for slot in play_board.hand:
                        if slot.card:
                            slot.card.draggable = True
                else:
                    next_button.visible = True
                    for slot in play_board.hand:
                        if slot.card:
                            slot.card.draggable = False
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    elif 'click' in show1_button.handleEvent(event):
                        if show2_button.caption != show2_button.def_caption:
                            show2_button.reset_text()
                        if show1_button.caption == show1_button.def_caption:
                            show_board = other_boards[0]
                            show1_button.caption = 'Return'
                        else:
                            show_board = play_board
                            show1_button.reset_text()
                    elif 'click' in show2_button.handleEvent(event):
                        if show1_button.caption != show1_button.def_caption:
                            show1_button.reset_text()
                        if show2_button.caption == show2_button.def_caption:
                            show_board = other_boards[1]
                            show2_button.caption = 'Return'
                        else:
                            show_board = play_board
                            show2_button.reset_text()
                    elif 'click' in next_button.handleEvent(event):
                        if turns == 4 and play_board is boards[-1]:
                            next_button.visible = False
                            running = False
                        elif next_button.caption == "End Turn":
                            if len(boards) > 1:
                                play_board.lock()
                                play_board.empty_hand()
                                next_button.caption = "Next Player"
                            else:
                                next_button.visible = False
                                running = False
                        else:
                            next_button.visible = False
                            next_button.caption = "End Turn"
                            running = False
                    elif show_board is play_board:
                        play_board.handle_dragging(event)
                screen.blit(background, (0, 0))
                next_button.draw(screen)
                show1_button.draw(screen)
                show2_button.draw(screen)
                if show_board is play_board:
                    show_board.draw(screen)
                else:
                    show_board.draw(screen, hand=False)
                pygame.display.update()
                clock.tick(FPS)
            play_board.collapse_full()
            play_board.lock()
            if turns != 4:
                play_board.deal(3)
    return win_screen(screen, boards)


def win_screen(screen, boards):
    score_boards(boards)
    winner(boards)

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(GREEN)

    replay_rect = Rect(
        (
            SCREEN_WIDTH - BUTTON_WIDTH - SPACE, 
            SPACE, 
            BUTTON_WIDTH, 
            BUTTON_HEIGHT
        )
    )
    replay_button = PygButton(replay_rect, caption="Play Again")

    home_rect = Rect(
        (
            SCREEN_WIDTH - BUTTON_WIDTH - SPACE, 
            BUTTON_HEIGHT + SPACE * 2, 
            BUTTON_WIDTH, 
            BUTTON_HEIGHT
        )
    )
    home_button = PygButton(home_rect, caption="Home")

    for count, board in enumerate(boards):
        board.rect = (SCREEN_HEIGHT / 5, (SCREEN_WIDTH * (count + 1))/(len(boards) + 1))

    player_text = [FONT.render(board.player.name, fgcolor=LIME) for board in boards]
    i = 0
    for image, rect in player_text:
        rect.top = SPACE * 2
        rect.centerx = (SCREEN_WIDTH * (i + 1)) / (len(boards) + 1)
        i += 1

    fouls = []
    for board in boards:
        if board['top'].score == 0:
            fouls.append(FONT.render('FOUL', fgcolor=RED))
        else:
            fouls.append(None)
    i = 0
    for foul in fouls:
        if foul:
            image, rect = foul
            rect.top = 32 + SPACE * 3
            rect.centerx = (SCREEN_WIDTH * (i + 1)) / (len(boards) + 1)
        i += 1

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif 'click' in replay_button.handleEvent(event):
                return (board.player for board in boards)
            elif 'click' in home_button.handleEvent(event):
                return
        screen.blit(background, (0, 0))
        for board in boards:
            board.draw(screen)
        for image, rect in player_text:
            screen.blit(image, rect)
        for foul in fouls:
            if foul:
                image, rect = foul
                screen.blit(image, rect)
        replay_button.draw(screen)
        home_button.draw(screen)
        pygame.display.update()
        clock.tick(FPS)


def home_screen(screen):
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

