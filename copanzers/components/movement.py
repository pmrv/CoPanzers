# Copyright (C) 2014 Marvin Poul <ponder@creshal.de>
import math
from ecs.models import Component

class Movement (Component):
    ### TODO: expand this class to support accelerations for rotating/moving
    __slots__ = "rotation", "_speed", "max_speed"
    def __init__ (self, rotation, speed, max_speed = 0):
        """
        the rotation parameter is also used for entities that can rotate but
        not move (like weapons)
        rotation -- float, direction in which the entity is pointing
        speed    -- float, how fast the entity currently is in px/s 
        """
        self.rotation = rotation
        self._speed = speed
        self.max_speed = max_speed

    @property
    def speed (self):
        return self._speed

    @speed.setter
    def speed (self, val):
        self._speed = max (0, min (val, self.max_speed))

    @property
    def dx (self):
        return self._speed * math.cos (self.rotation)

    @property
    def dy (self):
        return self._speed * math.sin (self.rotation)

    
    def __str__ (self):
        return "Movement ({}, {})".format (round (math.degrees (self.rotation), 2),
                round (self.speed, 2))
    
    __repr__ = __str__
