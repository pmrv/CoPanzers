# Copyright (C) 2014 Marvin Poul <ponder@creshal.de>
from ecs.models import Component

from copanzers.util import Rect

class HealthBar (Component, Rect):
    """
    Describes the position and size of the health bar relative to
    the center of the entity.
    """

    def __init__ (self, center, size):
        Rect.__init__ (self, 0, 0, *map(int, size))
        self.center = map(int, center)
