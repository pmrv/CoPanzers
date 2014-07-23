# Copyright (C) 2014 Marvin Poul <ponder@creshal.de>
import pygame
from ecs.models import Component

from copanzers.util import make_color_surface

class Renderable (Component):
    __slots__ = ("texture", "layer")

    @classmethod
    def file (cls, path, **kw):
        return cls (pygame.image.load (path), **kw)

    @classmethod
    def color (cls, size, color, **kw):
        return cls (make_color_surface (size, color), **kw)

    def __init__ (self, texture, layer = 0):
        """
        Note that entities that are Renderable also need at least the Position Component.
        texture -- pygame.Surface, image of what should be blitted
                   to the game screen
        layer   -- int, entities with lower layer are drawn first, negative layers are legal
        """
        self.texture = texture
        self.layer   = layer
        self.texture.set_colorkey ( (255, 255, 255) )
