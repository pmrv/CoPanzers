# Copyright (C) 2014 Marvin Poul <ponder@creshal.de>
from ecs.models import Component

class Mountable (Component):
    """
    This is more of a placeholder right now, not sure whether
    we'll really need this one.
    """
    __slots__ = "root"
    def __init__ (self, root):
        self.root = root
