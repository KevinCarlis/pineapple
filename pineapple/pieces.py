try:
    import sys
    import os
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
    import pygame
    import pygame.freetype
    from pygame.locals import *
    from deck import Deck
    from constants import *
except ImportError as err:
    print("couldn't load module. %s" % (err))
    sys.exit(2)


IMAGE_FOLDER = os.path.join('..', 'images')


def load_png(name, rect=True, dimensions=None):
    """ Load image and return image object"""
    fullname = os.path.join(IMAGE_FOLDER, name)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
        if dimensions:
            image = pygame.transform.scale(image, dimensions)
    except pygame.error as message:
        print('Cannot load image:', fullname)
        raise SystemExit(message)
    if rect:
        return image, image.get_rect()
    else:
        return image







class Dealer:

    def __init__(self, image_name='blue_back.png', rect=None, rules=None):
        self._cards = Deck()
        self._image, self._rect = load_png(image_name, dimensions=CARD_SIZE)

    def draw(self, surface):
        surface.blit(self._image, self._rect)

    def deal(*hands, num_cards=1):
        for hand in hands:
            hand.add_card(
            


class CardSprite:
    def __init__ (self, rank, suit, outline=False, image=None):
        self.rank = rank
        self.suit = suit
        self.draggable = True
        self.dragging = False
        self.loc = 'deck'
        image = image or str(self) + '.png'
        self.image, self._rect = load_png(image, dimensions=(CARD_WIDTH, CARD_HEIGHT))
        if outline:
            pygame.draw.rect(self.image, BLACK, self.rect, 1)

    def __str__(self):
        return str(self.rank) + str(self.suit)

    def __int__(self):
        return int(self.rank)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
    
    @property
    def rect(self):
        return self._rect

    @rect.setter
    def rect(self, rect):
        self._rect = pygame.Rect(rect)


class CardHolder(pygame.sprite.Sprite):
    def __init__(self, lefttop=(0, 0)):
        self._rect = pygame.Rect(lefttop, (CARD_WIDTH, CARD_HEIGHT))
        self.image = pygame.Surface(self.rect.size)
        self.image.fill(LIME)
        self._hitbox = self.rect.inflate(SPACE * 5, SPACE * 5)
        self._card = None
        pygame.sprite.Sprite.__init__(self)

    @property
    def rect(self):
        return self._rect

    @rect.setter
    def rect(self, lefttop):
        self._rect = pygame.Rect(lefttop, (CARD_WIDTH, CARD_HEIGHT))
        self._hitbox = self.rect.inflate(SPACE * 5, SPACE * 5)

    @property
    def card(self):
        return self._card

    @card.setter
    def card(self, card):
        if card:
            card.rect = self.rect
        self._card = card


class BoardRow:
    def __init__(self, row_name, slots):
        self.collapsed = False
        self._slots = []
        self.name = row_name
        self._rect = pygame.Rect((0, 0), ((CARD_WIDTH + SPACE) * len(self._slots) - SPACE, CARD_HEIGHT))
        self.slots = int(slots)

    def __len__(self):
        return len(self._slots)

    def __getitem__(self, key):
        return self._slots[key]

    def __str__(self):
        string = ""
        for slot in self:
            if string:
                string += ", "
            if slot.card:
                string += str(slot.card)
            else:
                string += "Empty"
        return string

    def draw(self, surface):
        if self.name != 'hand' and not self.collapsed:
            for slot in self:
                surface.blit(slot.image, slot.rect)
        for card in self.cards:
            card.draw(surface)

    def get_slots(self, slots):
        return [CardHolder() for _ in range(slots)]

    def set_rects(self):
        for count, slot in enumerate(self):
            if not self.collapsed:
                slot.rect = (
                    self._rect.left + (CARD_WIDTH + SPACE) * count, 
                    self._rect.top
                )
                slot.card = slot.card
            else:
                slot.rect = (
                    self._rect.left + ((SPACE + 2) * count),
                    self._rect.top
                )
                slot.card = slot.card

    def organize(self):
        sorted_hand = sorted(self.cards, key=int, reverse=True)
        rank_list = [card.rank for card in sorted_hand]
        rank_counts = Counter(rank_list)
        kickers = []
        if 3 in rank_counts.values():
            if 2 in rank_counts.values():
                if sorted_hand[0].rank == sorted_hand[2].rank:
                    for slot, card in zip(self.slots, sorted_hand):
                        slot.card = card
                else:
                    sorted_hand = sorted_hand[2:] + sorted_hand[:2]
                    for slot, card in zip(self.slots, sorted_hand):
                        slot.card = card
        for rank, count in rank_counts.items():
            if count == 1:
                for card in sorted_hand:
                    if card.rank == rank:
                        sorted_hand.remove(card) 
                        kickers.append(card)
        kickers = sorted(kickers, key=int, reverse=True)
        sorted_hand += kickers
        for count in range(len(sorted_hand)):
            self[count].card = sorted_hand[count]

    def result(self):
        self.organize()
        self.result, self.score = hand_result(self.cards)

    @property
    def rect(self):
        return self._rect

    @rect.setter
    def rect(self, topcenter):
        top, centerx = topcenter
        if not self.collapsed:
            self._rect = pygame.Rect(
                (0, top), 
                ((CARD_WIDTH + SPACE) * len(self._slots) - SPACE, CARD_HEIGHT)
            )
        else:
            self._rect = pygame.Rect(
                (0, top), 
                (CARD_WIDTH + (SPACE * (len(self._slots) - 1)), CARD_HEIGHT)
            )
        self._rect.centerx = centerx
        self.set_rects()

    @property
    def slots(self):
        return self._slots
    
    @slots.setter
    def slots(self, slots):
        if slots < len(self.cards):
            raise RunTimeError("More cards in row than slots")
        cards = self.cards
        self._slots = self.get_slots(slots)
        self.rect = (self._rect.top, self._rect.centerx)
        for count in range(len(cards)):
            self[count].card = cards[count]

    @property
    def cards(self):
        return [slot.card for slot in self if slot.card]
    
    @cards.setter
    def cards(self, new_cards):
        new_count = len(new_cards)
        for old_card in new_cards:
            if old_card in self.cards:
                new_count -= 1
        if new_count <= len(self) - len(self.cards):
            for new_card in new_cards:
                if new_card not in self.cards:
                    for slot in self:
                        if not slot.card:
                            slot.card = new_card
                            break
        else:
            new_cards += [None] * (len(self) - len(new_cards))
            removed_cards = self.cards
            for count in range(len(new_cards)):
                self[count].card = new_cards[count]
                if new_cards[count] in removed_cards:
                    removed_cards.remove(new_cards[count])
            self.dropped_cards = removed_cards


class Board:
    def __init__(self, player=None, lefttop=None):
        """Create a new board object.
            """
        if lefttop:
            self._rect = pygame.Rect(lefttop, (BOARD_WIDTH, BOARD_HEIGHT))
        else:
            self._rect = pygame.Rect((SCREEN_WIDTH - BOARD_WIDTH)//2, SPACE, BOARD_WIDTH, BOARD_HEIGHT)

        self.player = player or Player('Player')
        self.visible = True

        self._rows = {
            'top':    BoardRow(   'top', 3),
            'middle': BoardRow('middle', 5),
            'bottom': BoardRow('bottom', 5),
            'hand':   BoardRow(  'hand', 5)
        }
        self._update()
        self.deal(5)

    def __len__(self):
        return len(self.rows)

    def __getitem__(self, key):
        if isinstance(key, (int, slice)):
            return [self.rows['top'], self.rows['middle'], self.rows['bottom']][key]
        else:
            return self.rows[key]

    def __iter__(self):
        for row in self.rows.values():
            yield row

    def draw(self, surface, hand=True):
        """Draws slots and cards onto surface"""
        if self.visible:
            if hand:
                for row in self:
                    row.draw(surface)
            else:
                for row in self:
                    if row.name != 'hand':
                        row.draw(surface)
            for row in self:
                for card in row.cards:
                    if card.dragging:
                        card.draw(surface)

    def _update(self):
        """Call this method when you move the board."""
        top = self._rect.top
        self['top'].rect = (top, self._rect.centerx)
        self['middle'].rect = (top + CARD_HEIGHT + SPACE, self._rect.centerx)
        self['bottom'].rect = (top + CARD_HEIGHT * 2 + SPACE * 2, self._rect.centerx)
        if self.hand:
            self.hand.rect = (SCREEN_HEIGHT - CARD_HEIGHT - SPACE, self._rect.centerx)

    def handle_dragging(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for row in self:
                    for slot in row:
                        if slot.card and (slot.card.draggable or row.name != 'hand'):
                            if slot.card.rect.collidepoint(event.pos) and not row.collapsed:
                                slot.card.dragging = True
                                mouse_x, mouse_y = event.pos
                                global offset_x, offset_y
                                offset_x = slot.card.rect.x - mouse_x
                                offset_y = slot.card.rect.y - mouse_y
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                move_card = None
                for old_row in self:
                    for old_slot in old_row:
                        if old_slot.card and old_slot.card.dragging:
                            move_card = old_slot.card
                            move_card.dragging = False
                            break
                    if move_card:
                        break
                if move_card:
                    if old_row.name == 'hand':
                        for new_row in self:
                            for new_slot in new_row:
                                if new_slot._hitbox.contains(move_card.rect):
                                    if not new_slot.card:
                                        new_slot.card = move_card
                                        old_slot.card = None
                                        break
                                    else:
                                        if len(new_row.cards) != len(new_row.slots):
                                            for slot in reversed(new_row):
                                                if not slot.card:
                                                    slot.card = new_slot.card
                                                    new_slot.card = move_card
                                                    old_slot.card = None
                                                    break
                                            if not old_slot.card:
                                                break
                            if not old_slot.card:
                                break
                        else:
                            old_slot.card = move_card
                    else:
                        for new_row in self:
                            for new_slot in new_row:
                                if new_slot._hitbox.contains(move_card.rect):
                                    if new_row is old_row:
                                        old_slot.card = new_slot.card
                                        new_slot.card = move_card
                                        break
                                    elif move_card.draggable:
                                        if len(new_row.cards) != len(new_row):
                                            for slot in reversed(new_row):
                                                if not slot.card:
                                                    slot.card = new_slot.card
                                                    new_slot.card = move_card
                                                    old_slot.card = None
                                                    break
                                            if not old_slot.card:
                                                break
                            else:
                                continue
                            break
                        else:
                            if move_card.draggable:
                                for new_slot in self.hand:
                                    if not new_slot.card:
                                        new_slot.card = move_card
                                        old_slot.card = None
                                        break
                            else:
                                old_slot.card = move_card
        elif event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos
            for row in self:
                for slot in row:
                    if slot.card and slot.card.dragging:
                        if row.name != 'hand':
                            slot.card.rect.x = mouse_x + offset_x
                        if slot.card.draggable:
                            slot.card.rect.x = mouse_x + offset_x
                            slot.card.rect.y = mouse_y + offset_y

    def lock(self):
        for row in self:
            for card in row.cards:
                card.draggable = False

    def empty_hand(self):
        for slot in self.hand:
            if slot.card:
                slot.card = None

    def deal(self, num_cards):
        self.empty_hand()
        self.hand = num_cards
        cards = [CardSprite(rank, suit) for rank, suit in Board.deck.deal(num_cards)]
        for slot, card in zip(self.hand, cards):
            slot.card = card
        self.hand.organize()

    def collapse_full(self):
        for row in self:
            if row.name != 'hand':
                if not row.collapsed and len(row) == len(row.cards):
                    row.organize()
                    row.collapsed = True
                    self._update()

    @property
    def rows(self):
        return self._rows

    @rows.setter
    def rows(self, rows):
        self._rows = rows

    @property
    def rect(self):
        return self._rect

    @rect.setter
    def rect(self, topcenter):
        top, centerx = topcenter
        self._rect.top = top
        self._rect.centerx = centerx
        self._update()
    
    @property
    def hand(self):
        if 'hand' in self.rows.keys():
            return self['hand']
        else:
            return None
    
    @hand.setter
    def hand(self, size):
        if len(self['hand'].slots) != size:
            self['hand'].slots = size
            self._update()

    @hand.deleter
    def hand(self):
        self.rows.pop('hand', None)




if __name__ == "__main__":
    pygame.init()
    logo = pygame.image.load(os.path.join(IMAGE_FOLDER, 'PineLogo.png'))
    pygame.display.set_icon(logo)
    pygame.display.set_caption("PIECES TEST")
    
    screen = pygame.display.set_mode((SCREEN_SIZE))
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(GREEN)

    clock = pygame.time.Clock()


    image_name = 'blue_back.png'
    d = PlayingDeck(image_name)


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        else:
            screen.blit(background, (0, 0))
            d.draw(screen)
            pygame.display.update()
            clock.tick(FPS)

    