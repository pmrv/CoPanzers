
from ecs.models import Component

class ExampleTurret (Component):
    __slots__ = "target"
    def __init__ (self):
        self.target = None # entity id of the object we're targeting
