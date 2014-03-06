from ecs.models import Component

class Renderable (Component):
    __slots__ = ("texture",)
    def __init__ (self, texture):
        """
        Note that entities that are Renderable also need at least the Position Component.
        texture -- pygame.Surface, image of what should be blitted
                   to the game screen
        """
        self.texture = texture
