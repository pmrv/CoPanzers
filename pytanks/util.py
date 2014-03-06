import pygame

from pytanks.movement import Movement, Position
from pytanks.mount import Mount
from pytanks.mountable import Mountable
from pytanks.target import Hitbox, Health, HealthBar

def make_color_surface (size, color, colorkey = (255, 255, 255)):
    surface = pygame.Surface (size)
    surface.set_colorkey (colorkey)
    surface.fill (color)
    return surface

def Rect (center, size):
    return pygame.Rect (center [0] - size [0] / 2, center [1] - size [1] / 2, *size)
