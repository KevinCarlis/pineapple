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


class ABGameObject:
    def __init__(self, rect=None, rect_pos=None, rect_size=None, color=None, image_name=None, inflate=None, **kwargs):
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

