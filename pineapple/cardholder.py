
class CardHolder:

    def __init__(self, rect=None):
        self.rect = rect or (0, 0)

    def __init__(self, cards=None, rect=None, image=False, hitbox=10):
        self.inflate = hitbox * 5
        self._cards = cards
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

    def collide(self, rect):
        if self._rect.inflate(self.inflate, self.inflate).colliderect(rect):
            print('collide')
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

    @property
    def card(self):
        return self._card

    @card.setter
    def card(self, card):
        if card:
            card.loc = self
        self._card = card

class Hand:

    def __init__(self, size, cards=None, rect=None, color=None):
        self.size = size
        self._cards = [None] * self.size
        self.add(cards)

    @property
    def cards(self):
        return self._cards
    
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