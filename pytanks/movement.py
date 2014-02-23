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
from ecs.exceptions import NonexistentComponentTypeForEntity
### TODO: implement Hitbox & .target

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

class MovingSystem (System):

    def update (self, dt):
        for e, vel in self.entity_manager.pairs_for_type (Movement):
            try:
                pos = self.entity_manager.component_for_entity (e, Position)
            except NonexistentComponentTypeForEntity:
                print ("No position component found for moving.")
                continue # shouldn't be happening, but just to be sure

            pos.x += vel.speed * math.cos (vel.rotation)
            pos.y += vel.speed * math.sin (vel.rotation)

            try:
                hitbox = self.entity_manager.component_for_entity (e, Hitbox)
                hitbox.center = pos.x, pos.y
            except NonexistentComponentTypeForEntity:
                print ("Entity has no hitbox, don't try to move it.")
                continue
