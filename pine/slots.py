try:
    import os
    import sys
    import collections
    from .constants import CARD_SIZE, BLACK, LIME
    from .abgameobj import ABGameObject
except ImportError as err:
    print(f"Unable to load module. \n{err}")
    sys.exit(2)


class ABSlot:
    def __init__(self, size=None):
        self.size = size or 1
        self.elements = []

    def __call__(self, *elements):
        if not elements:
            return self.elements
        else:
            return self._handle_addition(*elements)

    def _add(self, element):
        self.elements.append(element)

    def _remove(self, elements):
        for element in elements:
            if element in self.elements:
                self.elements.remove(element)

    def _handle_addition(self, *elements):
        for value in elements:
            if value in self.elements:
                return self._handle_duplicate(value)
            elif len(self.elements) == self.size:
                return self._handle_overflow(value)
            else:
                self._add(value)
        return None

    def _handle_duplicate(self, value):
        print(f'{self} attempted to add duplicate object')
        return value

    def _handle_overflow(self, value):
        raise IndexError("Added too many objects to slot.")


class CardSlot(ABSlot, ABGameObject):
    """PyGame playing card holder
    kwargs
       size: int number of cards per slot

    """
    defaults = {
        'rect_size': CARD_SIZE,
        'color': LIME,
        'inflate': (50, 50),
        'size': 1
    }

    def __init__(self, **kwargs):
        self.__dict__.update({**CardSlot.defaults, **kwargs})
        ABSlot.__init__(self, self.size)
        ABGameObject.__init__(self, **self.__dict__)

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


class Hand(ABSlot):
    def __init__(self, size=5):
        ABSlot.__init__(self, size)
        self(*(CardSlot(rect_pos=(100 * i + 100, 100)) for i in range(5)))

    def draw(self, surface):
        for slot in self():
            slot.draw(surface)

