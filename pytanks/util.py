import pygame

class Destroyed (Exception): pass

def Rect (center, size):
    return pygame.Rect (center [0] - size [0] / 2, center [1] - size [1] / 2, *size)
