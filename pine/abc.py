try:
    import os
    import sys
    import collections

    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
    import pygame as pg
    from .constants import IMAGE_FOLDER, CARD_SIZE, BLACK, LIME
except ImportError as err:
    print(f"Unable to load module. \n{err}")
    sys.exit(2)


def load_png(name, rect=None, image_folder=None):
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
    image_folder = image_folder or IMAGE_FOLDER
    fullname = os.path.join(image_folder, name)
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


class DragMixin:
    def __init__(self, draggable=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.draggable = draggable or False
        self.dragging = False

    def drag(self, pg_event):
        if pg_event.type not in (pg.MOUSEMOTION, pg.MOUSEBUTTONUP, pg.MOUSEBUTTONDOWN) or not self.draggable:
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

    def update(self):
        if not self.dragging:
            if self.loc:
                self.rect = (self.loc.rect.x, self.loc.rect.y)


class ABGameObject:
    def __init__(self,
                 rect=None, rect_pos=None, rect_size=None, inflate=None,
                 color=None, image_name=None,
                 **kwargs):
        self.image = None
        self.inflate = inflate or (0, 0)
        if rect:
            self.rect = rect
        else:
            rect_pos = rect_pos or (0, 0)
            rect_size = rect_size or (0, 0)
            self.rect = pg.Rect(rect_pos, rect_size)
        if image_name:
            self.image = load_png(image_name, rect=self.rect)
        elif color:
            self.image = pg.Surface(self.rect.size)
            self.image.fill(color)
        for kwarg in ['rect_pos', 'rect_size', 'color']:
            self.__dict__.pop(kwarg, None)

    def draw(self, surface):
        if self.image:
            surface.blit(self.image, self.rect)

    def collide(self, obj):
        if self.rect.inflate(*self.inflate).colliderect(obj.rect):
            print(f'{self} collide {obj}, {obj.loc}')
            return True
        return False

    def move(self, x, y):
        self.rect.move_ip(x, y)


class SlotMixin:
    def __init__(self, size=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
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

