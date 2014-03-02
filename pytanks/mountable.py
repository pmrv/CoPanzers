"""
GameObjects that can be mounted on others.
self.position will be set first by mount.insert
and then synchronized by mountable.step, therefor
by convention mountable GameObjects should be 
instantiated with position as (0, 0).
"""

from ecs.models import Component

class Mountable (Component):
    """
    This is more of a placeholder right now, not sure whether
    we'll really need this one.
    """
    __slots__ = "root"
    def __init__ (self, root):
        self.root = root
