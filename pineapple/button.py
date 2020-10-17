try:
    import sys
    import os
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
    import pygame
    import pygame.freetype
    from pygame.locals import *
    import random
    from enum import Enum
    from collections import Counter
except ImportError as err:
    print("couldn't load module. %s" % (err))
    sys.exit(2)


BUTTON_HEIGHT = 40
BUTTON_WIDTH = 120
BLACK     = (  0,   0,   0)
WHITE     = (255, 255, 255)
DARKGRAY  = ( 64,  64,  64)
GRAY      = (128, 128, 128)
LIGHTGRAY = (212, 208, 200)


class PygButton(object):

    def __init__(self, rect=None, caption='', bgcolor=None, fgcolor=None, 
        font=None, normal=None, down=None, highlight=None):
        """Create a new button object. Parameters:
            rect - The size and position of the button as a pygame.Rect object
                or 4-tuple of integers.
            caption - The text on the button (default is blank)
            bgcolor - The background color of the button (default is a light
                gray color)
            fgcolor - The foreground color (i.e. the color of the text).
                Default is black.
            font - The pygame.font.Font object for the font of the text.
                Default is freesansbold in point 14.
            normal - A pygame.Surface object for the button's normal
                appearance.
            down - A pygame.Surface object for the button's pushed down
                appearance.
            highlight - A pygame.Surface object for the button's appearance
                when the mouse is over it.
            If the Surface objects are used, then the caption, bgcolor,
            fgcolor, and font parameters are ignored (and vice versa).
            Specifying the Surface objects lets the user use a custom image
            for the button.
            The normal, down, and highlight Surface objects must all be the
            same size as each other. Only the normal Surface object needs to
            be specified. The others, if left out, will default to the normal
            surface.
            """
        if rect:
            self._rect = pygame.Rect(rect)
        else:
            self._rect = pygame.Rect(0, 0, 30, 60)

        self._def_caption = caption
        self._caption = caption
        self._bgcolor = bgcolor or LIGHTGRAY
        self._fgcolor = fgcolor or BLACK
        self._font = font or pygame.font.Font('freesansbold.ttf', 14)

        # tracks the state of the button
        self.buttonDown = False
        # is the button currently pushed down?
        self.mouseOverButton = False
        # is the mouse currently hovering over the button?
        self.lastMouseDownOverButton = False
        # was the last mouse down event over the mouse button? (Used to track clicks.)
        self._visible = True
        # is the button visible
        self.customSurfaces = False
        # button starts as a text button instead of having custom images for each surface

        if normal is None:
            # create the surfaces for a text button
            self.surfaceNormal = pygame.Surface(self._rect.size)
            self.surfaceDown = pygame.Surface(self._rect.size)
            self.surfaceHighlight = pygame.Surface(self._rect.size)
            self._update() # draw the initial button images
        else:
            # create the surfaces for a custom image button
            self.setSurfaces(normal, down, highlight)

    def handleEvent(self, eventObj):
        """All MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN event objects
        created by Pygame should be passed to this method. handleEvent() will
        detect if the event is relevant to this button and change its state.
        There are two ways that your code can respond to button-events. One is
        to inherit the PygButton class and override the mouse*() methods. The
        other is to have the caller of handleEvent() check the return value
        for the strings 'enter', 'move', 'down', 'up', 'click', or 'exit'.
        Note that mouseEnter() is always called before mouseMove(), and
        mouseMove() is always called before mouseExit(). Also, mouseUp() is
        always called before mouseClick().
        buttonDown is always True when mouseDown() is called, and always False
        when mouseUp() or mouseClick() is called. lastMouseDownOverButton is
        always False when mouseUp() or mouseClick() is called."""

        if eventObj.type not in (MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN) or not self._visible:
            # The button only cares bout mouse-related events (or no events, if it is invisible)
            return []

        retVal = []

        hasExited = False
        if not self.mouseOverButton and self._rect.collidepoint(eventObj.pos):
            # if mouse has entered the button:
            self.mouseOverButton = True
            self.mouseEnter(eventObj)
            retVal.append('enter')
        elif self.mouseOverButton and not self._rect.collidepoint(eventObj.pos):
            # if mouse has exited the button:
            self.mouseOverButton = False
            hasExited = True 
            # call mouseExit() later, since we want mouseMove() to be handled before mouseExit()

        if self._rect.collidepoint(eventObj.pos):
            # if mouse event happened over the button:
            if eventObj.type == MOUSEMOTION:
                self.mouseMove(eventObj)
                retVal.append('move')
            elif eventObj.type == MOUSEBUTTONDOWN:
                self.buttonDown = True
                self.lastMouseDownOverButton = True
                self.mouseDown(eventObj)
                retVal.append('down')
        else:
            if eventObj.type in (MOUSEBUTTONUP, MOUSEBUTTONDOWN):
                # if an up/down happens off the button, then the next up won't cause mouseClick()
                self.lastMouseDownOverButton = False

        # mouse up is handled whether or not it was over the button
        doMouseClick = False
        if eventObj.type == MOUSEBUTTONUP:
            if self.lastMouseDownOverButton:
                doMouseClick = True
            self.lastMouseDownOverButton = False

            if self.buttonDown:
                self.buttonDown = False
                self.mouseUp(eventObj)
                retVal.append('up')

            if doMouseClick:
                self.buttonDown = False
                self.mouseClick(eventObj)
                retVal.append('click')

        if hasExited:
            self.mouseExit(eventObj)
            retVal.append('exit')

        return retVal

    def draw(self, surfaceObj):
        """Blit the current button's appearance to the surface object."""
        if self._visible:
            if self.buttonDown:
                surfaceObj.blit(self.surfaceDown, self._rect)
            elif self.mouseOverButton:
                surfaceObj.blit(self.surfaceHighlight, self._rect)
            else:
                surfaceObj.blit(self.surfaceNormal, self._rect)


    def _update(self):
        """Redraw the button's Surface object. Call this method when the button has changed appearance."""
        if self.customSurfaces:
            self.surfaceNormal    = pygame.transform.smoothscale(self.origSurfaceNormal, self._rect.size)
            self.surfaceDown      = pygame.transform.smoothscale(self.origSurfaceDown, self._rect.size)
            self.surfaceHighlight = pygame.transform.smoothscale(
                self.origSurfaceHighlight, self._rect.size
            )
            return

        w = self._rect.width # syntactic sugar
        h = self._rect.height # syntactic sugar

        # fill background color for all buttons
        self.surfaceNormal.fill(self.bgcolor)
        self.surfaceDown.fill(self.bgcolor)
        self.surfaceHighlight.fill(self.bgcolor)

        # draw caption text for all buttons
        captionSurf = self._font.render(self._caption, True, self.fgcolor, self.bgcolor)
        captionRect = captionSurf.get_rect()
        captionRect.center = int(w / 2), int(h / 2)
        self.surfaceNormal.blit(captionSurf, captionRect)
        self.surfaceDown.blit(captionSurf, captionRect)

        # draw border for normal button
        pygame.draw.rect(self.surfaceNormal, BLACK, pygame.Rect((0, 0, w, h)), 1) 
        # black border around everything
        pygame.draw.line(self.surfaceNormal, WHITE, (1, 1), (w - 2, 1))
        pygame.draw.line(self.surfaceNormal, WHITE, (1, 1), (1, h - 2))
        pygame.draw.line(self.surfaceNormal, DARKGRAY, (1, h - 1), (w - 1, h - 1))
        pygame.draw.line(self.surfaceNormal, DARKGRAY, (w - 1, 1), (w - 1, h - 1))
        pygame.draw.line(self.surfaceNormal, GRAY, (2, h - 2), (w - 2, h - 2))
        pygame.draw.line(self.surfaceNormal, GRAY, (w - 2, 2), (w - 2, h - 2))

        # draw border for down button
        pygame.draw.rect(self.surfaceDown, BLACK, pygame.Rect((0, 0, w, h)), 1) 
        # black border around everything
        pygame.draw.line(self.surfaceDown, WHITE, (1, 1), (w - 2, 1))
        pygame.draw.line(self.surfaceDown, WHITE, (1, 1), (1, h - 2))
        pygame.draw.line(self.surfaceDown, DARKGRAY, (1, h - 2), (1, 1))
        pygame.draw.line(self.surfaceDown, DARKGRAY, (1, 1), (w - 2, 1))
        pygame.draw.line(self.surfaceDown, GRAY, (2, h - 3), (2, 2))
        pygame.draw.line(self.surfaceDown, GRAY, (2, 2), (w - 3, 2))

        # draw border for highlight button
        self.surfaceHighlight = self.surfaceNormal


    def mouseClick(self, event):
        pass # This class is meant to be overridden.
    def mouseEnter(self, event):
        pass # This class is meant to be overridden.
    def mouseMove(self, event):
        pass # This class is meant to be overridden.
    def mouseExit(self, event):
        pass # This class is meant to be overridden.
    def mouseDown(self, event):
        pass # This class is meant to be overridden.
    def mouseUp(self, event):
        pass # This class is meant to be overridden.


    def setSurfaces(self, normalSurface, downSurface=None, highlightSurface=None):
        """Switch the button to a custom image type of button (rather than a
        text button). You can specify either a pygame.Surface object or a
        string of a filename to load for each of the three button appearance
        states."""
        if downSurface is None:
            downSurface = normalSurface
        if highlightSurface is None:
            highlightSurface = normalSurface

        if type(normalSurface) == str:
            self.origSurfaceNormal = pygame.image.load(normalSurface)
        if type(downSurface) == str:
            self.origSurfaceDown = pygame.image.load(downSurface)
        if type(highlightSurface) == str:
            self.origSurfaceHighlight = pygame.image.load(highlightSurface)

        if self.origSurfaceNormal.get_size() != self.origSurfaceDown.get_size() \
            != self.origSurfaceHighlight.get_size():
            raise Exception('foo')

        self.surfaceNormal = self.origSurfaceNormal
        self.surfaceDown = self.origSurfaceDown
        self.surfaceHighlight = self.origSurfaceHighlight
        self.customSurfaces = True
        self._rect = pygame.Rect(
            (self._rect.left, self._rect.top, 
             self.surfaceNormal.get_width(), self.surfaceNormal.get_height())
        )

    def reset_text(self):
        self.caption = self.def_caption

    @property
    def def_caption(self):
        return self._def_caption

    @def_caption.setter
    def def_caption(self, caption_text):
        self._def_caption = caption_text
        self.caption = caption_text

    @property
    def caption(self):
        return self._caption

    @caption.setter
    def caption(self, caption_text):
        self.customSurfaces = False
        self._caption = caption_text
        self._update()

    @property
    def rect(self):
        return self._rect

    @rect.setter
    def rect(self, new_rect):
        # Note that changing the attributes of the Rect won't update the button. 
        # You have to re-assign the rect member.
        self._update()
        self._rect = new_rect

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, setting):
        self._visible = setting

    @property
    def fgcolor(self):
        return self._fgcolor

    @fgcolor.setter
    def fgcolor(self, setting):
        self.customSurfaces = False
        self._fgcolor = setting
        self._update()

    @property
    def bgcolor(self):
        return self._bgcolor

    @bgcolor.setter
    def bgcolor(self, setting):
        self.customSurfaces = False
        self._bgcolor = setting
        self._update()

    @property
    def font(self):
        return self._font

    @font.setter
    def font(self, setting):
        self.customSurfaces = False
        self._font = setting
        self._update()

