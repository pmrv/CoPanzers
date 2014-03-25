
from ecs.models import Component

class Weapon (Component):
    __slots__ = ("reload_time", "till_reloaded", 
                "bullet_properties", "triggered")

    def __init__ (self, reload_time, bullet_properties):
        """
        reload_time       -- float
        bullet_properties -- 5 tuple, see pytanks.make.bullet for a details 
        """
        self.till_reloaded = 0
        self.reload_time = reload_time
        self.bullet_properties = bullet_properties
        self.triggered = False
