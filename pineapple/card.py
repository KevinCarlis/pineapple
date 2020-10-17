try:
    import sys
    import os
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
    import pygame
    import pygame.freetype
    from pygame.locals import *
    import random
    from enum import Enum
    from collections import Counter
except ImportError as err:
    print("couldn't load module. %s" % (err))
    sys.exit(2)


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


class Rank(Enum):
    Two = 2, '2'
    Three = 3, '3'
    Four = 4, '4'
    Five = 5, '5'
    Six = 6, '6'
    Seven = 7, '7'
    Eight = 8, '8'
    Nine = 9, '9'
    Ten = 10, '10'
    Jack = 11, 'J'
    Queen = 12, 'Q'
    King = 13, 'K'
    Ace = 14, 'A'

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.value[1]

    def __int__(self):
        return self.value[0]


class Suit(Enum):
    Clubs = 'C'
    Diamonds = 'D'
    Hearts = 'H'
    Spades = 'S'

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.value


class Deck:
    def __init__ (self):
        self.deck = [(rank, suit) for rank in Rank for suit in Suit]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.deck)

    def __len__ (self):
        return len(self.deck)

    def __str__(self):
        return str([str(rank) + str(suit) for rank, suit in self.deck])

    def deal (self, *args):
        if len(self) == 0:
            return None
        elif args:
            return (self.deck.pop() for _ in range(args[0]))
        else:
            return (self.deck.pop())


def hand_result(sorted_hand):
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

