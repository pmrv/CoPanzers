
from ecs.models import Component

class Weapon (Component):
    __slots__ = ("reload_time", "till_reloaded", 
                "bullet_dmg", "bullet_speed", "bullet_hp",
                "bullet_texture", "bullet_hitbox", "triggered")

    def __init__ (self, reload_time, bullet_properties):
        """
        reload_time -- float
        bullet_properties -- 5 tuple of  
                        0: int, damage,
                        1: int, speed,
                        2: int, hit points,
                        3: pygame.Surface, texture
                        4: 2 tuple of int, hitbox
        """
        self.till_reloaded = 0
        self.reload_time = reload_time
        self.bullet_properties = bullet_properties
        self.triggered = False
