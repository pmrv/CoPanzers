"""
Objects which can be shot at and take damage.
"""

import pygame, math
from ecs.models import Component

# TODO: it seems weird to have all these different class 
# just for one or two parameters

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


class Projectile (Component):
    """
    Belongs to entities which should do damage when colliding with 
    another one. Calling this "Projectile" and not "Bullet" because
    I might want to implement Rockets or something like this.
    """
    __slots__ = "damage", "ignore"

    def __init__ (self, damage, ignore):
        """
        damage -- int
        ignore -- list of ecs.models.Entity, when the Projectile would
                  collide with an Entity and this Entity is ∈ self.ignore
                  ignore this collision.
        """
        self.damage = damage
        self.ignore = ignore


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
    """
    Describes the position and size of the health bar relative to
    the center of the entity.
    """

    def __init__ (self, center, size):
        pygame.Rect.__init__ (self, center [0] - size [0] / 2,
                                    center [1] - size [1] / 2,
                                    *size)


class Mountable (Component):
    """
    This is more of a placeholder right now, not sure whether
    we'll really need this one.
    """
    __slots__ = "root"
    def __init__ (self, root):
        self.root = root


class Mount (Component):

    __slots__ = "points", "amount", "mounts"

    def __init__ (self, points):
        """
        points -- iterable of 2 tuple of int,
                  list of relative coordinates of 
                  the centers of the mountpoints
        """

        self.points = tuple (points)
        # maximum number of enitities in this mount
        self.amount = len (self.points)
        # list of all entities in this mount
        # indices correspond with self.points
        self.mounts = [None] * self.amount


class Position (Component):
    # TODO: replace this and Movement with a real Vector Class some day

    __slots__ = "x", "y"
    def __init__ (self, x, y):
        self.x, self.y = x, y

    def __str__ (self):
        # casting to int here since the x/y values specify pixels anyway
        return "Position ({}, {})".format (int (self.x), int (self.y))

    __repr__ = __str__

    def __len__ (self): return 2

    def __getitem__ (self, i):
        if   i == 0:
            return self.x
        elif i == 1:
            return self.y
        else:
            raise IndexError ("Index for Position must be in {0, 1}.")

    def __setitem__ (self, i, v):
        if   i == 0:
            self.x = v
        elif i == 1:
            self.y = v
        else:
            raise IndexError ("Index for Position must be in {0, 1}.")


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


class Renderable (Component):
    __slots__ = ("texture",)
    def __init__ (self, texture, layer = 0):
        """
        Note that entities that are Renderable also need at least the Position Component.
        texture -- pygame.Surface, image of what should be blitted
                   to the game screen
        layer   -- int, entities with lower layer are drawn first, negative layers are legal
        """
        self.texture = texture
        self.layer   = layer


class Tags (Component, dict):
    """
    Simple component to store meta data for the entity
    """
    pass


class ExampleTurret (Component):
    __slots__ = "target"
    def __init__ (self):
        self.target = None # entity id of the object we're targeting


class Weapon (Component):
    __slots__ = ("reload_time", "till_reloaded", 
                "bullet_dmg", "bullet_speed", "bullet_hp",
                "bullet_texture", "bullet_hitbox", "triggered")

    def __init__ (self, reload_time, bullet_properties):
        """
        reload_time -- float
        bullet_properties -- 5 tuple of  
                        0: int, damage,
                        1: int, speed,
                        2: int, hit points,
                        3: pygame.Surface, texture
                        4: 2 tuple of int, hitbox
        """
        self.till_reloaded = 0
        self.reload_time = reload_time
        self.bullet_properties = bullet_properties
        self.triggered = False
