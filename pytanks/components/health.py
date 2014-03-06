"""
Objects which can be shot at and take damage.
"""

import pygame
from ecs.models import Component, System
from ecs.exceptions import NonexistentComponentTypeForEntity

# it seems weird to have all these different class 
# just for one or two parameters

### TODO: write helper functions to set sane defaults
class Hitbox (Component, pygame.Rect):
    """
    describes the area in which the entity can be hit _relative_
    to the Position, that is, before using its .collide* methods
    you will have to correctly set its center.
    Only its .width/.height attributes matter.
    """
    pass

class Health (Component):
    __slots__ = "hp", "max_hp"
    def __init__ (self, hp, max_hp = None):
        """
        hp     -- int, health points this entity (currently) has
        max_hp -- int, health points this entity can have at most
        """
        self.hp = hp
        self.max_hp = max_hp if max_hp else hp

class HealthBar (Component, pygame.Rect):
    pass
