
import pygame
from ecs.models import Component

# TODO: Hitbox and HealthBar are nigh identical except for
# the initialization, not sure whether this is sensible
class Hitbox (Component, pygame.Rect):
    """
    Describes the area in which the entity can be hit _relative_
    to the Position, that is, before using its .collide* methods
    you will have to correctly set its center.
    Only its .width/.height attributes matter.
    """

    def __init__ (self, size):
        pygame.Rect.__init__ (self, 0, 0, *size)
