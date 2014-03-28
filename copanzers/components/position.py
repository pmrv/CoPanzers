# Copyright (C) 2014 Marvin Poul <ponder@creshal.de>
from ecs.models import Component

from copanzers.util import Vec2d

class Position (Component, Vec2d):

    def __str__ (self):
        # casting to int here since the x/y values specify pixels anyway
        return "Position ({0.x:f}, {0.y:f})".format (self)

    __repr__ = __str__
