import pygame

class Destroyed (Exception): pass

def make_color_surface (width, height, color, colorkey = (255, 255, 255)):
    surface = pygame.Surface ( (width, height) )
    surface.set_colorkey (colorkey)
    surface.fill (color)
    return surface

def Rect (center, size):
    return pygame.Rect (center [0] - size [0] / 2, center [1] - size [1] / 2, *size)
