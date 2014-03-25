import math, logging
from copy import copy
from functools import partial
from ecs.managers import EntityManager
from ecs.exceptions import NonexistentComponentTypeForEntity

from pytanks.util import RefFloat
from pytanks.components import (Position, 
                                Movement,
                                Weapon,
                                Health,
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
        # whether the interface refers to an destroyed entity (so you know when
        # you can stop shooting
        self.destroyed = False 

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
    def hp (self):
        return self.eman.component_for_entity (self.e, Health).hp

    @property
    @unsure
    def position (self):
        # we make a shallow copy here so the script routine cannot modify the
        # position of themselves or other entities
        return copy (self.eman.component_for_entity (self.e, Position))

    @property
    @unsure
    def rotation (self):
        return self.eman.component_for_entity (self.e, Movement).rotation

    @property
    @unsure
    def speed (self):
        return self.eman.component_for_entity (self.e, Movement).speed

    @property
    @unsure
    def velocity (self):
        m = self.eman.component_for_entity (self.e, Movement)
        return m.dx, m.dy

    @property
    @unsure
    def mounts (self):
        # TODO: not optimal to instanstiate the interface on every call again
        return [ROInterface (m, self.eman) if m else None
            for m in self.eman.component_for_entity (self.e, Mount).mounts]

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
        # TODO: not optimal to instanstiate the interface on every call again
        return [RWInterface (m, self.eman) if m else None
            for m in self.eman.component_for_entity (self.e, Mount).mounts]

    @unsure
    def shoot (self):
        self.eman.component_for_entity (self.e, Weapon).triggered = True

    @property
    @unsure
    def till_reloaded (self):
        return self.eman.component_for_entity (self.e, Weapon).till_reloaded

    @property
    @unsure
    def reload_time (self):
        return self.eman.component_for_entity (self.e, Weapon).reload_time

class EntityView (EntityManager):
    """
    represents all entities in the game in a manner the script routines 
    can handle comfortably
    subclasses ecs.managers.EntityManager for simplicity
    """

    def __init__ (self, time):
        """
        time -- pytanks.utils.RefFloat, tracks the total elapsed time
        """
        self.time = time
        super ().__init__ ()
        self.__interfaces = []

    def create_entity (self):
        e = super ().create_entity ()
        self.__interfaces.append (ROInterface (e, self))
        return e

    def remove_entity (self, e):
        # that's why we compare directly to the given element in
        # ROInterface.__eq__
        for i in self.__interfaces:
            if i == e:
                # so scripts using this interface know the underlying interface
                # was destroyed
                i.destroyed = True
                break

        self.__interfaces.remove (e) 
        super ().remove_entity (e)

    def __iter__ (self):
        return iter (copy (self.__interfaces))
