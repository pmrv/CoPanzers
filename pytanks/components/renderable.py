# Copyright (C) 2014 Marvin Poul <ponder@creshal.de>
from ecs.models import Component

class Renderable (Component):
    __slots__ = ("texture",)
    def __init__ (self, texture, layer = 0):
        """
        Note that entities that are Renderable also need at least the Position Component.
        texture -- pygame.Surface, image of what should be blitted
                   to the game screen
        layer   -- int, entities with lower layer are drawn first, negative layers are legal
        """
        self.texture = texture
        self.layer   = layer
