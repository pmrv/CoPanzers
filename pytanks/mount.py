"""
GameObjects one can mount others on.
Get the maximum number of mounting points via
self.mount_num and their relative positions via
self.mountpoints. Use the indices of the latter 
as $point_id when calling self.mount().
"""

from ecs.models import Component, System
from ecs.exceptions import NonexistentComponentTypeForEntity

from pytanks.movement import Position

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

class MountSystem (System):

    def update (self, dt):

        eman = self.entity_manager
        for e, m in eman.pairs_for_type (Mount):

            try: 
                pos = eman.compononent_for_enitity (e, Position)
            except NonexistentComponentTypeForEntity:
                print ("Weird, entity {} has no Position.".format (e))
                continue

            for i in range (m.amount):
                im = m.mounts [i]
                if im is None: continue

                try: 
                    ipos = eman.compononent_for_enitity (im, Position)
                    ipos.x += pos.x + m.points [i] [0]
                    ipos.y += pos.y + m.points [i] [1]

                except NonexistentComponentTypeForEntity:
                    print ("Weird, entity {} has no Position.".format (im))
                    continue
