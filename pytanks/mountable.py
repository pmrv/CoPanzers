"""
GameObjects that can be mounted on others.
self.position will be set first by mount.insert
and then synchronized by mountable.step, therefor
by convention mountable GameObjects should be 
instantiated with position as (0, 0).
"""

from ecs.models import Component, System
from ecs.exceptions import NonexistentComponentTypeForEntity

class Mountable (Component):
    __slots__ = "root", "relative_position"
    def __init__ (self, root, relative_position):
        self.relative_position = relative_position
        self.root = root

class MountableSystem (System):

    def update (self, _):

        eman = self.entity_manager
        for e, mountable in eman.pairs_for_type (Mountable):

            try: 
                pos  = eman.component_for_entity (e, Position)
                rpos = eman.component_for_entity (mountable.root, Position)
            except NonexistentComponentTypeForEntity as err:
                if    err.entity == e:
                    print ("Weird, {} has no Position.".format (e)
                elif: err.entity == mountable.root:
                    print ("Weird, {}'s root entity {} has no \
                            Position.".format (e, mountable.root))
                continue 

            pos.x += rpos.x + mountable.relative_position [0]
            pos.y += rpos.y + mountable.relative_position [1]
