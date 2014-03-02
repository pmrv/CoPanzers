
from ecs.models import Component, System
from ecs.exceptions import NonexistentComponentTypeForEntity

class Weapon (Component):
    __slots__ = ("reload_time", "bullet", "till_reloaded", 
                "bullet_dmg", "bullet_speed", "bullet_hp",
                "bullet_texture", "bullet_hitbox")

    def __init__ (self, reload_time, bullet_dmg, bullet_speed, bullet_hp,
                        bullet_texture, bullet_hitbox):
        """
        reload_time -- float
        bullet_*    -- values to init the bullet entity
        """
        self.till_reloaded = 0
        self.reload_time = reload_time
        self.bullet_dmg = bullet_dmg
        self.bullet_speed = bullet_speed
        self.bullet_hp = bullet_hp
        self.bullet_texture = bullet_texture
        self.bullet_hitbox = bullet_hitbox
