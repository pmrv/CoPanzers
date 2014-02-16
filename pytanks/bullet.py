import math

from pytanks import GameObject
from pytanks.util import Destroyed
import pytanks.mobile as mobile
import pytanks.target as target

class Bullet (GameObject):

    direction = property (mobile.get_dir)
    speed     = property (mobile.get_speed)

    def __init__ (self, hp, damage, speed, direction, *args, **kw):
        """
        hp     -- int, how much damage the bullet itself can take
        damage -- int, how much damage the bullet does on impact
        """

        self.damage = damage

        GameObject.__init__ (self, *args, **kw)
        mobile.init (self, speed, direction)
        target.init (self, hp)
        self.tags ["class"] = "Bullet"

    def step (self, others, dt):

        for o in others:
            if self.hitbox.colliderect (o.hitbox) and hasattr (o, "hit"):
                o.hit (self.damage, self)
                raise Destroyed ("Bullet hit something.")

        GameObject.step (self, others, dt)
        mobile.step (self, others, dt)
        target.step (self, others, dt)

    def draw (self, surface):
        mobile.draw (self, surface)

