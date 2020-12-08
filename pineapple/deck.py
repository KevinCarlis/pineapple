
import os
import sys
from enum import Enum
import random
import pygame as pg
try:
    from constants import *
except:
    pass

IMAGE_FOLDER = os.path.join('..', 'images')


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
            pg.draw.rect(self.image, BLACK, self.rect, 1)
        self.image = None
        self.draggable = False
        self.dragging = False
        pg.sprite.Sprite.__init__(self)

    def __repr__(self):
        return f'{self.rank.name} of {self.suit.name}'

    def __str__(self):
        return str(self.rank) + str(self.suit)

    def __int__(self):
        return int(self.rank)

    def drag(self, event):
        if event.type not in (pg.MOUSEMOTION, pg.MOUSEBUTTONUP, pg.MOUSEBUTTONDOWN):
            return

        if self.dragging:
            if event.type == pg.MOUSEMOTION:
                self.rect.center = event.pos
            if event.type == pg.MOUSEBUTTONUP:
                print(self, self.loc, self.rect)
                self.dragging = False
        elif self.draggable and self.rect.collidepoint(event.pos):
            if event.type == pg.MOUSEBUTTONDOWN:
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

    def __init__ (self, image_name='blue_back.png', rect=None):
        self.rect = rect or (0,0)
        self.image = load_png(image_name, rect=self.rect)
        self._dealt = 0
        self.cards = [Card(rank, suit, self) for rank in Rank for suit in Suit]
        self.shuffle()

    def __str__(self):
        return f"Deck containing {len(self)} cards."

    def __len__ (self):
        return len(self.cards) - self._dealt

    def __next__(self):
        if len(self) > 0:
            card = self.cards[self._dealt]
            card.loc = None
            card.update()
            self._dealt += 1
            return card
        else:
            raise StopIteration("Deck is out of cards. Try shuffling.")

    def __iter__(self):
        return self

    def __call__(self, cards: int):
        if cards < len(self):
            return tuple(next(self) for _ in range(cards))
        else:
            raise IndexError("Asking for more cards than left in deck.")

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def shuffle(self):
        self._dealt = 0
        random.shuffle(self.cards)

    @property
    def rect(self):
        return self._rect

    @rect.setter
    def rect(self, rect):
        if isinstance(rect, tuple):
            self._rect = pg.Rect(rect, CARD_SIZE)
        elif isinstance(rect, pg.Rect):
            self._rect = rect


class CardHolder:

    def __init__(self, card=None, rect=None, color=None, image_name=None, hitbox=10):
        self.inflate = hitbox * 5
        self.card = card
        self.rect = rect or (0, 0)
        self.color = color or LIME
        self.image = pg.Surface(self.rect.size)
        self.image.fill(self.color)
        if image_name:
            self.image = self.load_png(image_name, rect=self.rect)

    def __call__(self, card):
        if not self.card:
            self.card = card
            return None
        return card

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def collide(self, obj):
        if self._rect.inflate(self.inflate, self.inflate).colliderect(obj.rect):
            print(f's{self} collide {obj}, {obj.loc}')
            return True
        return False

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
            raise TypeError("rect must be rect or tuple)

    @property
    def card(self):
        return self._card

    @card.setter
    def card(self, card):
        if card:
            card.loc = self
        self._card = card


class Controller:

    def __init__(self):
        self.deck = Deck(rect=(200,200))
        self.cards = pg.sprite.Group()
        self.cards.add(*self.deck(2))
        self.move_card = None
        self.slots = [CardHolder(), CardHolder(rect=(100,300))]
        for card in self.cards:
            card.draggable = True
            print(card)

    def draw(self, screen):
        self.deck.draw(screen)
        for slot in self.slots:
            slot.draw(screen)
        self.cards.draw(screen)
        if self.move_card:
            self.move_card.draw(screen)

    def update(self):
        self.cards.update()
        for card in self.cards:
            if not card.loc and not card.dragging:
                card.move(random.randint(0, 10), random.randint(0,10))

    def handle(self, event):
        for card in self.cards:
            if card.draggable:
                card.drag(event)
                if card.dragging:
                    self.move_card = card
                    break
        if self.move_card and not self.move_card.dragging:
            for slot in self.slots:
                if slot.collide(self.move_card):
                    slot(self.move_card)
            self.move_card = None

if __name__ == "__main__":
    pg.init()
    logo = pg.image.load(os.path.join(IMAGE_FOLDER, 'PineLogo.png'))
    pg.display.set_icon(logo)
    pg.display.set_caption("DECK TEST")

    screen = pg.display.set_mode((SCREEN_SIZE))
    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill(GREEN)

    clock = pg.time.Clock()

    test = Controller()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            else:
                test.handle(event)
        else:
            screen.blit(background, (0, 0))
            test.draw(screen)
            test.update()

            pg.display.update()
            clock.tick(FPS)
    