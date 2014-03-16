
import math
from ecs.models import Component

class Movement (Component):
    ### TODO: expand this class to support accelerations for rotating/moving
    __slots__ = "rotation", "speed"
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

    
    def __str__ (self):
        return "Movement ({}, {})".format (round (math.degrees (self.rotation), 2),
                round (self.speed, 2))
    
    __repr__ = __str__
