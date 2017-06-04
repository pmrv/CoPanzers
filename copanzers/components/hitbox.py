# Copyright (C) 2014 Marvin Poul <ponder@creshal.de>
from ecs.models import Component

from copanzers.util import Rect

# TODO: Hitbox and HealthBar are nigh identical except for
# the initialization, not sure whether this is sensible
class Hitbox (Component, Rect):
    """
    Describes the area in which the entity can be hit _relative_
    to the Position, that is, before using its .collide* methods
    you will have to correctly set its center.
    Only its .width/.height attributes matter.
    """

    def __init__ (self, size):
        Rect.__init__ (self, 0, 0, *map(int, size))
