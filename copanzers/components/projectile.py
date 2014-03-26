# Copyright (C) 2014 Marvin Poul <ponder@creshal.de>
from ecs.models import Component

class Projectile (Component):
    """
    Belongs to entities which should do damage when colliding with 
    another one. Calling this "Projectile" and not "Bullet" because
    I might want to implement Rockets or something like this.
    """
    __slots__ = "damage", "ignore"

    def __init__ (self, damage, ignore):
        """
        damage -- int
        ignore -- list of ecs.models.Entity, when the Projectile would
                  collide with an Entity and this Entity is ∈ self.ignore
                  ignore this collision.
        """
        self.damage = damage
        self.ignore = ignore
