try:
    import os
    import sys
    from enum import Enum
    import random
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
    import pygame as pg
    from . import constants
except ImportError as err:
    print(f"Unable to load module. \n{err}")
    sys.exit(2)


IMAGE_FOLDER = constants.IMAGE_FOLDER or os.path.join('..', 'images')
CARD_SIZE = constants.CARD_SIZE or (70, 105)
BLACK = constants.BLACK or (0, 0, 0)
LIME = constants.LIME or (50, 205, 50)


def load_png(name, rect=None):
    """Loads image

    Parameters:
    name: str, path
        name of image in image_folder

    Keywords:
    rect: pygame.rect
        object with size attribute for resizing

    Returns:
    image: image object
    rect: if rect not given as keyword
    """
    fullname = os.path.join(IMAGE_FOLDER, name)
    if pg.get_init():
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

    def __init__(self, rank, suit, loc=None, rect=None, image_name=None, outline=False):
        pg.sprite.Sprite.__init__(self)
        self.rank = rank
        self.suit = suit
        self.loc = loc or (0, 0)
        self.rect = rect or (0, 0)
        self.image_name = image_name or str(self) + '.png'
        if outline:
            pg.draw.rect(self.image, BLACK, self.rect, 1)
        self.image = None
        self.draggable = False
        self.dragging = False

    def __repr__(self):
        return f'{self.rank.name} of {self.suit.name}'

    def __str__(self):
        return str(self.rank) + str(self.suit)

    def __int__(self):
        return int(self.rank)

    def drag(self, pg_event):
        if pg_event.type not in (pg.MOUSEMOTION, pg.MOUSEBUTTONUP, pg.MOUSEBUTTONDOWN):
            return

        if self.dragging:
            if pg_event.type == pg.MOUSEMOTION:
                self.rect.center = pg_event.pos
            if pg_event.type == pg.MOUSEBUTTONUP:
                print(self, self.loc, self.rect)
                self.dragging = False
        elif self.draggable and self.rect.collidepoint(pg_event.pos):
            if pg_event.type == pg.MOUSEBUTTONDOWN:
                self.dragging = True

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def move(self, x, y):
        self.rect.move_ip(x, y)

    def update(self):
        if not self.image:
            self.image = load_png(self.image_name, rect=self._rect)
        if not self.dragging:
            if self.loc:
                self.rect = (self.loc.rect.x, self.loc.rect.y)

    @property
    def rect(self):
        return self._rect

    @rect.setter
    def rect(self, rect):
        if isinstance(rect, tuple):
            self._rect = pg.Rect(rect, CARD_SIZE)
        elif isinstance(rect, pg.Rect):
            self._rect = rect
        else:
            raise TypeError(f"Card.rect must be tuple or Rect not {type(rect)}")


class Deck:
    """Iterable Deck of Cards
    Once iterated deck needs to be shuffled using shuffle method

    Keywords:
        image_name: name of image file located in image directory
        rect: pg.Rect
        pos: tuple of (x, y) coordinates
        size: tuple of (height, width) for deck size

    Access:
        for card in deck: iterates through rest of deck
        deck(n): gives n cards as tuple
        deck(): gives next card

    Methods:
        shuffle(): shuffles deck
        draw(surface): draws deck image on surface
    """
    def __init__(self, image_name='blue_back.png', rect=None, pos=None, size=None):
        if rect:
            self.rect = rect
        else:
            self.pos = pos or (0, 0)
            size = size or CARD_SIZE
            self.rect = pg.Rect(self.pos, size)
        self.image = load_png(image_name, rect=self.rect)
        self._dealt = 0
        self.cards = [Card(rank, suit, self.pos, size) for rank in Rank for suit in Suit]
        self.shuffle()

    def __str__(self):
        return f"Deck containing {len(self)} cards."

    def __len__(self):
        return len(self.cards)

    def __next__(self):
        if self.cards:
            card = self.cards[0]
            card.loc = None
            card.update()
            self._dealt += 1
            return card
        else:
            raise StopIteration("Deck is out of cards. Try shuffling.")

    def __iter__(self):
        return self

    def __call__(self, cards=1):
        if cards <= len(self):
            return tuple(next(self) for _ in range(cards))
        else:
            raise IndexError("Asking for more cards than left in deck.")

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def shuffle(self):
        self._dealt = 0
        random.shuffle(self._cards)

    @property
    def rect(self):
        return self._rect

    @rect.setter
    def rect(self, rect):
        try:
            self._rect = pg.Rect(rect)
        except TypeError:
            self._rect = pg.Rect(rect, self.rect.size)

    @property
    def cards(self):
        return self._cards[self._dealt:]

    @cards.setter
    def cards(self, cards):
        self._cards = cards
        if len(cards) < 52:
            print('Deck created with less than 52 cards')

