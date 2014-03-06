"""
Objects that can move in a certain direction with a certain speed
and (might) change that direction.
Direction/Speed is set/get via a property
(propert (mobile.get_*, mobile.set_*)).
If direction or speed should be immutable, modify the property
accordingly, but make sure they are always set with the provided
setter functions.
"""

import math
from ecs.models import Component, System

class Position (Component):

    __slots__ = "x", "y"
    def __init__ (self, x, y):
        self.x, self.y = x, y

class Movement (Component):
    ### TODO: expand this class to support accelerations for rotating/moving
    __slots__ = "rotation", "speed", "dx", "dy"
    def __init__ (self, rotation, speed):
        """
        the rotation parameter is also used for entities that can rotate but
        not move (like weapons)
        rotation -- float, direction in which the entity is pointing
        speed    -- float, how fast the entity currently is in px/s 
        """
        self.rotation = rotation
        self.speed = speed

    @property
    def dx (self):
        return self.speed * math.cos (self.rotation)

    @property
    def dy (self):
        return self.speed * math.sin (self.rotation)

