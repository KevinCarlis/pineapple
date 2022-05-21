import os

"""Adujstibles"""
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
SCREEN_SIZE = (1000, 600)

"""File Locations"""
IMAGE_FOLDER = os.path.join('..', 'images')

"""Game Constants"""
FPS = 30
SPACE = 10

CARD_WIDTH = 70
CARD_HEIGHT = 105
CARD_SIZE = (70, 105)

BOARD_WIDTH = (CARD_WIDTH + SPACE) * 5 - SPACE
BOARD_HEIGHT = SCREEN_HEIGHT

BUTTON_HEIGHT = 40
BUTTON_WIDTH = 120

"""Colors"""
BLACK     = (  0,   0,   0)
WHITE     = (255, 255, 255)
GREEN     = (  0,  60,   0)
DARKGRAY  = ( 64,  64,  64)
GRAY      = (128, 128, 128)
LIGHTGRAY = (212, 208, 200)
LIME      = ( 50, 205,  50)
RED       = (255,   0,   0)
