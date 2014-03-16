
from ecs.models import Component

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
