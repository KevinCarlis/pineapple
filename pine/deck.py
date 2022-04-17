try:
    import os
    import sys
    from enum import Enum
    import random
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
    import pygame as pg
    from . import constants
    from . import abc
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


class Card(abc.DragMixin, abc.ABGameObject):

    defaults = {
        'rect_size': CARD_SIZE,
        'inflate': (50, 50),
    }

    def __init__(self, rank, suit, outline=False, **kwargs):
        self.rank = rank
        self.suit = suit
        self.image_name = str(self) + '.png'
        self.__dict__.update({**Card.defaults, **kwargs})
        super().__init__(**self.__dict__)
        if outline:
            pg.draw.rect(self.image, BLACK, self.rect, 1)
        self.draggable = False
        self.dragging = False

    def __repr__(self):
        return f'{self.rank.name} of {self.suit.name}'

    def __str__(self):
        return str(self.rank) + str(self.suit)

    def __int__(self):
        return int(self.rank)


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
            pos = pos or (0, 0)
            size = size or CARD_SIZE
            self.rect = pg.Rect(pos, size)
        self.image = load_png(image_name, rect=self.rect)
        self._dealt = 0
        self.cards = [Card(rank, suit, rect_pos=self.rect.topleft, rect_size=size) for rank in Rank for suit in Suit]
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


class CardSlot(abc.SlotMixin, abc.ABGameObject):
    """PyGame playing card holder
    kwargs
       size: int number of cards per slot

    """
    defaults = {
        'size': 1,
        'rect_size': CARD_SIZE,
        'color': LIME,
        'inflate': (50, 50),
    }

    def __init__(self, **kwargs):
        self.__dict__.update({**CardSlot.defaults, **kwargs})
        super().__init__(**self.__dict__)

    def __repr__(self):
        if self():
            return f"Slot containing {self()}"
        else:
            return f"Slot at {self.rect.topleft}"

    def _handle_overflow(self, value):
        ret = self().pop()
        self._remove([ret])
        self._add(value)
        return ret


class Hand(abc.SlotMixin):
    defaults = {
        'size': 5,
        'rect_size': CARD_SIZE,
        'x' : 100,
        'y': 100,
    }
    def __init__(self, **kwargs):
        self.__dict__.update({**Hand.defaults, **kwargs})
        super().__init__(self.size)
        self(*(CardSlot(rect_pos=(2 * self.rect_size[0] * i + self.x, self.y)) for i in range(self.size)))

    def draw(self, surface):
        for slot in self():
            slot.draw(surface)

