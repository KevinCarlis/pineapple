from enum import Enum
import random
import pygame as pg
try:
    from constants import *
except:
    pass

IMAGE_FOLDER = os.path.join('..', 'images')


def load_png(name, rect=None):
    """ Load image and return image object"""
    fullname = os.path.join(IMAGE_FOLDER, name)
    try:
        image = pg.image.load(fullname)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
        if rect:
            image = pg.transform.scale(image, rect.size)
            return image
    except pg.error as message:
        print('Cannot load image:', fullname)
        raise SystemExit(message)    
    else:
        return image, image.get_rect()


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

class Card(pg.sprite.Sprite):

    def __init__(self, rank, suit, loc, rect=None, image_name=None, outline=False):
        self.rank = rank
        self.suit = suit
        self.loc = loc
        self.rect = rect or (0, 0)
        self.image_name = image_name or str(self) + '.png'
        if outline:
            pg.draw.rect(self._image, BLACK, self._rect, 1)
        self.image = None
        self.draggable = True
        self._dragging = False

    def __repr__(self):
        return f'{self.rank.name} of {self.suit.name}'

    def __str__(self):
        return str(self.rank) + str(self.suit)

    def __int__(self):
        return int(self.rank)

    def handle_event(self, event):
        state = []
        if event.type not in (pg.MOUSEMOTION, pg.MOUSEBUTTONUP, pg.MOUSEBUTTONDOWN):
            return state

        if self.rect.collidepoint(event.pos):
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.draggable:
                    self._dragging = True
                    state.append('clicked')

        if self._dragging:
            if event.type == pg.MOUSEMOTION:
                self.rect.center = event.pos
                state.append('moving')
            elif event.type == pg.MOUSEBUTTONUP:
                self._dragging = False
                state.append('dropped')

        return state

    def move(self, x, y):
        self.rect.move_ip(x,y)

    def update(self):
        if not self._dragging:
            self.rect = self.loc.rect.center

    @property
    def rect(self):
        return self._rect

    @rect.setter
    def rect(self, rect):
        if isinstance(rect, tuple):
            self._rect = pg.Rect(rect, CARD_SIZE)
        elif isinstance(rect, pg.Rect):
            self._rect = rect