try:
    import os
    import sys
    import random
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
    import pygame as pg
    from . import constants 
    from .deck import Deck, Card
    from .cardholder import CardSlot
except ImportError as err:
    print(f"Unable to load module. \n{err}")
    sys.exit(2)


IMAGE_FOLDER = constants.IMAGE_FOLDER or os.path.join('..', 'images')
FPS = constants.FPS or 30
SCREEN_SIZE = constants.SCREEN_SIZE
LIME = constants.LIME or (50, 205, 50)
GREEN = constants.GREEN


class Controller:

    def __init__(self):
        self.deck = Deck(pos=(200, 200))
        self.cards = pg.sprite.Group()
        self.move_card = None
        self.slots = [CardSlot(), CardSlot(rect_pos=(100, 300))]
        for c in self.cards:
            c.draggable = True
            print(c)

    def draw(self, surface):
        self.deck.draw(surface)
        for slot in self.slots:
            slot.draw(surface)
        self.cards.draw(surface)
        if self.move_card:
            self.move_card.draw(surface)

    def update(self):
        self.cards.update()
        for c in self.cards:
            if not (c.loc or c.dragging):
                c.move(random.randint(0, 10), random.randint(0, 10))

    def handle(self, pg_event):
        for move_card in self.cards:
            if move_card.draggable:
                move_card.drag(pg_event)
                if move_card.dragging:
                    self.move_card = move_card
                    break
        if self.move_card and not self.move_card.dragging:
            for slot in self.slots:
                if slot.collide(self.move_card):
                    slot(self.move_card)
            self.move_card = None

def main():
    #os.environ["SDL_AUDEODRIVER"] = "dummy"
    pg.init()
    #pg.display.list_modes()
    #os.environ["SDL_VIDEODRIVER"] = "dummy"
    logo = pg.image.load(os.path.join(IMAGE_FOLDER, 'PineLogo.png'))
    pg.display.set_icon(logo)
    pg.display.set_caption("DECK TEST")

    screen = pg.display.set_mode(SCREEN_SIZE)
    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill(GREEN)

    clock = pg.time.Clock()

    test = Controller()
    for slot in test.slots:
        print(slot)

    try:
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
    except SystemExit:
        for card in test.deck._cards:
            print(f'{card} at {card.loc}')
        pg.display.quit()

