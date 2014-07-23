
from ecs.models import Component

class Weapon (Component):
    __slots__ = ("reload_time", "till_reloaded", 
                "bullet_type", "triggered")

    def __init__ (self, reload_time, bullet_type):
        """
        reload_time -- float
        bullet_type -- str, name of the used bullet, must be known to the
                       copanzers.make module
        """
        self.till_reloaded = 0
        self.reload_time = reload_time
        self.bullet_type = bullet_type
        self.triggered = False
