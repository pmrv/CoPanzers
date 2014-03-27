import math, logging
from copy import copy
from functools import partial
from ecs.managers import EntityManager
from ecs.exceptions import NonexistentComponentTypeForEntity

from copanzers.util import RefFloat
from copanzers.components import (Position, 
                                Destroyed,
                                Movement,
                                Weapon,
                                Health,
                                Vision,
                                Mount,
                                Tags)

def get_logger (name):
    """
    name -- str, name of the script routine this logger is for
    """
    return logging.getLogger (__name__ + "." + name)

def unsure (meth):
    def f (*args, **kw):
        try:
            return meth (*args, **kw)
        except NonexistentComponentTypeForEntity:
            raise AttributeError ("'{}' object has no attribute '{}'".format (
                args [0].__class__.__name__, meth.__name__)) from None

    f.__name__ = meth.__name__
    return f


# TODO: We should maybe think about making the interfaces flyweights
class ROInterface:
    """
    read only interface to the components of a entity
    """

    def __init__ (self, entity, entity_manager):
        """
        entity         -- ecs.models.Entity, the entity this 
                          interface represents
        entity_manager -- ecs.managers.EntityManager, the manager
                          where we get the entities components from
        """

        if entity is None:
            raise ValueError ("Can't create a interface to None")

        self.e = entity
        self.eman = entity_manager
        self.__throttle = 0

    def __eq__ (self, other):
        if hasattr (other, "e"):
            return self.e == other.e
        else:
            # in case we want to compare directly an entity
            return self.e == other 

    def __getitem__ (self, i):
        try:
            return self.eman.component_for_entity (self.e, Tags) [i]
        except NonexistentComponentTypeForEntity:
            raise KeyError (i)

    @property
    @unsure
    # not exactly happy with that, maybe unsure should just raise an error or
    # something
    def destroyed (self):
        return Destroyed in self.eman.database and self.e in self.eman.database [Destroyed]

    @property
    @unsure
    def hp (self):
        """
        Current hit points of entity.
        """
        return self.eman.component_for_entity (self.e, Health).hp

    @property
    @unsure
    def max_hp (self):
        """
        Maximum hit points of entity.
        """
        return self.eman.component_for_entity (self.e, Health).max_hp

    @property
    @unsure
    def size (self):
        """
        Size of the hit box of the entity.
        """
        return self.eman.component_for_entity (self.e, Hitbox).size

    @property
    @unsure
    def position (self):
        """
        Position of the entity.
        """
        # we make a shallow copy here so the script routine cannot modify the
        # position of themselves or other entities
        return copy (self.eman.component_for_entity (self.e, Position))

    @property
    @unsure
    def rotation (self):
        """
        Rotation of the entity, in radians, rotation 0 is parallel to the 
        x-axis.
        """
        return self.eman.component_for_entity (self.e, Movement).rotation

    @property
    @unsure
    def speed (self):
        """
        Speed of the entity as a scalar, in px/s.
        """
        return self.eman.component_for_entity (self.e, Movement).speed

    @property
    @unsure
    def velocity (self):
        """
        Velocity of the entity as a 2-tuple, in px/s.
        """
        m = self.eman.component_for_entity (self.e, Movement)
        return m.dx, m.dy

    @property
    @unsure
    def mounts (self):
        """
        List of either interfaces of mounted entities or None if the respective
        mount point is empty.
        """
        # TODO: not optimal to instanstiate the interface on every call again
        return [ROInterface (m, self.eman) if m else None
            for m in self.eman.component_for_entity (self.e, Mount).mounts]

    @property
    @unsure
    def root (self):
        """
        Entity this entity is mounted on.
        """
        return self.eman.component_for_entity (self.e, Mountable).root

class RWInterface (ROInterface):
    """
    read/write interface to the components of a entity, intended to be used by
    the script routines
    """

    @ROInterface.speed.setter
    @unsure
    def speed (self, val):
        self.eman.component_for_entity (self.e, Movement).speed = val

    @ROInterface.rotation.setter
    @unsure
    def rotation (self, val):
        self.eman.component_for_entity (self.e, Movement).rotation = val

    @property
    @unsure
    def throttle (self):
        """
        speed of the entity in percent, getter clamps 
        value between 0 and 1
        """
        return self.__throttle

    @throttle.setter
    @unsure
    def throttle (self, val):
        self.__throttle = min (1, max (0, val))
        mov = self.eman.component_for_entity (self.e, Movement)
        mov.speed = val * mov.max_speed

    @property
    @unsure
    def mounts (self):
        """
        List of either interfaces of mounted entities or None if the respective
        mount point is empty.
        """
        # TODO: not optimal to instanstiate the interface on every call again
        return [RWInterface (m, self.eman) if m else None
            for m in self.eman.component_for_entity (self.e, Mount).mounts]

    @unsure
    def shoot (self):
        """
        Shoots a bullet if this entity is a weapon.
        """
        self.eman.component_for_entity (self.e, Weapon).triggered = True

    @property
    @unsure
    def till_reloaded (self):
        """
        Seconds until this weapon can fire again.
        """
        return self.eman.component_for_entity (self.e, Weapon).till_reloaded

    @property
    @unsure
    def reload_time (self):
        """
        Seconds between shots.
        """
        return self.eman.component_for_entity (self.e, Weapon).reload_time

    @property
    @unsure
    def bullet_damage (self):
        """
        Damage done by the bullets of this weapon.
        """
        return self.eman.component_for_entity (
                self.e,
                Weapon
        ).bullet_properties [0]

    @property
    @unsure
    def bullet_speed (self):
        """
        Speed of the bullets of this weapon, in px/s.
        """
        return self.eman.component_for_entity (
                self.e,
                Weapon
        ).bullet_properties [1]

    @property
    @unsure
    def bullet_hp (self):
        """
        Hit points of the bullets of this weapon.
        """
        return self.eman.component_for_entity (
                self.e,
                Weapon
        ).bullet_properties [2]

    @property
    @unsure
    def bullet_size (self):
        """
        Size of the bullets of this weapon.
        """
        return self.eman.component_for_entity (
                self.e,
                Weapon
        ).bullet_properties [3]

    @property
    @unsure
    def visible (self):
        """
        Return all entities that are plainly visible.
        """
        return self.eman.component_for_entity (
                self.e,
                Vision
        ).visible