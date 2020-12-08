try:
    import sys
    from collections import Counter
except ImportError as err:
    print("couldn't load module. %s" % (err))
    sys.exit(2)

def hand_result(sorted_hand):
    """Scores a list of card object
    """
    rank_list = [card.rank for card in sorted_hand]
    rank_counts = Counter(rank_list)
    suit_check = sorted_hand[0].suit
    for card in sorted_hand:
        if len(sorted_hand) == 3:
            break
        if card.suit != suit_check:
            break
    else:
        if str(sorted_hand[0].rank) == 'A':
            if int(sorted_hand[4]) == 10:
                return 'Royal Flush', 8 * 13 ** 5 + score_hand(sorted_hand)
            elif int(sorted_hand[1]) == 5 and int(sorted_hand[4]) == 2:
                return 'Five High Straight Flush', 8 * 13 ** 5 + score_hand(sorted_hand[1:] + [1])
            else:
                return 'Ace High Flush', 5 * 13 ** 5 + score_hand(sorted_hand)
        elif int(sorted_hand[0]) - int(sorted_hand[4]) == 4:
            return f'{sorted_hand[0].rank.name} High Straight Flush', 8 * 13 ** 5 + score_hand(sorted_hand)
        else:
            return f'{sorted_hand[0].rank.name} High Flush', 5 * 13 ** 5 + score_hand(sorted_hand)
    if len(rank_counts) == 1:
        return (
            f'Three of a Kind, {sorted_hand[0].rank.name}s', 
            3 * 13 ** 5 + score_hand(sorted_hand + [1, 1])
        )
    if len(rank_counts) == 2:
        if 4 in rank_counts.values():
            return f'Four of a Kind, {sorted_hand[0].rank.name}s', 7 * 13 ** 5 + score_hand(sorted_hand)
        elif 3 in rank_counts.values():
            return (
                f'Full House {sorted_hand[0].rank.name}s over {sorted_hand[4].rank.name}s', 
                6 * 13 ** 5 + score_hand(sorted_hand)
            )
        else:
            return f'Pair of {sorted_hand[0].rank.name}s', 1 * 13 ** 5 + score_hand(sorted_hand + [1, 1])
    elif len(rank_counts) == 3:
        if 3 in rank_counts.values():
            return f'Three of a Kind, {sorted_hand[0].rank.name}s', 3 * 13 ** 5 + score_hand(sorted_hand)
        elif 2 in rank_counts.values():
            return (
                f'Two Pair, {sorted_hand[0].rank.name}s over {sorted_hand[2].rank.name}s', 
                2 * 13 ** 5 + score_hand(sorted_hand)
            )
        else:
            return f'{sorted_hand[0].rank.name} High', score_hand(sorted_hand + [1, 1])
    elif len(rank_counts) == 4:
        return  f'Pair of {sorted_hand[0].rank.name}s', 1 * 13 ** 5 + score_hand(sorted_hand)
    else:
        if int(sorted_hand[0]) - int(sorted_hand[4]) == 4:
            return f'{sorted_hand[0].rank.name} High Straight', 4 * 13 ** 5 + score_hand(sorted_hand)
        elif int(sorted_hand[0]) == 14 and int(sorted_hand[1]) == 5 and int(sorted_hand[4]) == 2:
            return 'Five High Straight', 4 * 13 ** 5 + score_hand(sorted_hand[1:] + [1])
        else:
            return f'{sorted_hand[0].rank.name} High', score_hand(sorted_hand)


def score_hand(hand):
    return (int(hand[0]) * 13 ** 4 
           + int(hand[1]) * 13 ** 3 
           + int(hand[2]) * 13 ** 2 
           + int(hand[3]) * 13
           + int(hand[4]))


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







