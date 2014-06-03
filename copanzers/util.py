# Copyright (C) 2014 Marvin Poul <ponder@creshal.de>
from functools import total_ordering
import pygame, math

def make_color_surface (size, color, colorkey = (255, 255, 255)):
    surface = pygame.Surface (size)
    surface.set_colorkey (colorkey)
    surface.fill (color)
    pygame.draw.rect (surface, (0, 0, 0), surface.get_rect (), 1)
    return surface

def Rect (center, size):
    return pygame.Rect (center [0] - size [0] / 2, center [1] - size [1] / 2, *size)

@total_ordering
class RefFloat:
    """ Mutable float. Only implements addition, since this appears to be
    everything we need. """
    def __init__ (self, f):
        self.__f = f

    def __eq__ (self, o):
        return self.__f.__eq__ (o)

    def __lt__ (self, o):
        return self.__f.__lt__ (o)

    def __add__ (self, o):
        if isinstance (o, RefFloat):
            # this only works because self and o are of the same class
            return self.__f.__add__ (o.__f)
        else:
            return self.__f.__add__ (o)

    def __sub__ (self, o):
        if isinstance (o, RefFloat):
            # this only works because self and o are of the same class
            return self.__f.__sub__ (o.__f)
        else:
            return self.__f.__sub__ (o)

    def __radd__ (self, o):
        return self.__f.__radd__ (o)

    def __rsub__ (self, o):
        return self.__f.__rsub__ (o)


    def __iadd__ (self, o):
        self.__f += o
        return self

    def __isub__ (self, o):
        self.__f -= o
        return self

    def __str__ (self):
        return str (self.__f)

    def __repr__ (self):
        return "RefFloat({})".format (self.__f)

    def __abs__ (self):
        return self.__f

class Vec2d:
    """ Simple two-dimensional vector implementation """

    __slots__ = "x", "y", "_Vec2d__nullangle"

    def __init__ (self, x, y):
        self.x = x
        self.y = y
        self.__nullangle = self.angle if x != y else 0
        """ allow the null vector to be rotated, mostly for convenience in the
        Movement component """

    def __len__ (self):
        return 2

    def __getitem__ (self, i):
        if   i == 0:
            return self.x
        elif i == 1:
            return self.y
        else:
            raise IndexError ("Index must be in {0, 1}.")

    def __setitem__ (self, i, v):
        if   i == 0:
            self.x = v
        elif i == 1:
            self.y = v
        else:
            raise IndexError ("Index must be in {0, 1}.")

    def __abs__ (self):
        return math.sqrt (self.x ** 2 + self.y ** 2) 

    @property
    def length (self):
        return abs (self)

    @length.setter
    def length (self, v):
        l = abs (self)
        if l == 0:
            self.x = v * math.cos (self.__nullangle)
            self.y = v * math.sin (self.__nullangle)
        else:
            self *= v / l

    @property
    def angle (self):

        x, y = self
        if x == y == 0:
            return self.__nullangle
        return math.atan2 (y, x)

    @angle.setter
    def angle (self, a):

        l = abs (self)
        if l == 0:
            self.__nullangle = a
        else:
            self.x = l * math.cos (a)
            self.y = l * math.sin (a)

    def distanceto (self, o):

        if not isinstance (o, Vec2d):
            raise ValueError ("Argument must be Vec2d.")

        return abs (self - o)

    def __add__ (self, o):

        if not isinstance (o, Vec2d):
            raise ValueError ("Argument must be Vec2d.")

        return Vec2d (self.x + o.x, self.y + o.y)

    def __sub__ (self, o):

        if not isinstance (o, Vec2d):
            raise ValueError ("Argument must be Vec2d.")

        return Vec2d (self.x - o.x, self.y - o.y)

    def __mul__ (self, f):

        return Vec2d (self.x * f, self.y * f)

    def __truediv__ (self, f):

        return Vec2d (self.x / f, self.y / f)

    def __iadd__ (self, o):

        if not isinstance (o, Vec2d):
            raise ValueError ("Argument must be Vec2d.")

        self.x += o.x
        self.y += o.y

        return self

    def __isub__ (self, o):

        if not isinstance (o, Vec2d):
            raise ValueError ("Argument must be Vec2d.")

        self.x -= o.x
        self.y -= o.y

        return self

    def __imul__ (self, f):

        self.x *= f
        self.y *= f

        return self

    def __itruediv__ (self, f):

        self.x /= f
        self.y /= f

        return self

    def __repr__ (self):
        return "Vec2d({0.x:f},{0.y:f})".format (self)

    __str__ = __repr__
