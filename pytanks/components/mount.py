
from ecs.models import Component

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
