# Copyright (C) 2014 Marvin Poul <ponder@creshal.de>
import math
from ecs.models import Component

from copanzers.util import Vec2d

class Movement (Component, Vec2d):
    ### TODO: expand this class to support accelerations for rotating/moving
    def __init__ (self, rotation = 0, speed = 0, max_speed = -1):
        """
        the rotation parameter is also used for entities that can rotate but
        not move (like weapons)
        rotation  -- float, direction in which the entity is pointing
        speed     -- float, how fast the entity currently is in px/s
        max_speed -- float, maximum speed
        """

        super ().__init__ (speed, 0)
        self.angle = rotation
        self.max_speed = max_speed

    @Vec2d.length.setter
    def length (self, val):
        l = abs (self)
        if l == 0:
            self.x = val
        else:
            if self.max_speed >= 0:
                self *= max (0, min (val, self.max_speed)) / l
            else:
                self *= max (0, val) / l

    def __str__ (self):
        return "Movement ({0.x:f}, {0.y:f})".format (self)

    __repr__ = __str__
