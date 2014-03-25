from functools import total_ordering
import pygame
from ecs.exceptions import NonexistentComponentTypeForEntity

from pytanks.components import Mount

def make_color_surface (size, color, colorkey = (255, 255, 255)):
    surface = pygame.Surface (size)
    surface.set_colorkey (colorkey)
    surface.fill (color)
    pygame.draw.rect (surface, (0, 0, 0), surface.get_rect (), 1)
    return surface

def Rect (center, size):
    return pygame.Rect (center [0] - size [0] / 2, center [1] - size [1] / 2, *size)

def components_for_entity (eman, entity, components):
    """
    Return a tuple of component instances for a given entity.
    Will not catch any NonexistentComponentTypeForEntity Errors.
    """

    return tuple (eman.component_for_entity (entity, c) for c in components)

def remove_entity (eman, e):
    """
    remove an entity and all mounted entities from the entity manager
    """
    try:
        for m in eman.component_for_entity (e, Mount):
            eman.remove_entity (m)
    except NonexistentComponentTypeForEntity:
        pass
    finally:
        eman.remove_entity (e)

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
        return "RefInt({})".format (self.__f)

    def __abs__ (self):
        return self.__f
