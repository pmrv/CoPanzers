import math

from pytanks import GameObject
from pytanks.util import Destroyed

class Bullet (GameObject):

    def __init__ (self, speed, direction, damage, *args, **kw):
        """
        speed     -- int, how fast is the bullet moving
        direction -- float, in radians
        damage    -- int
        """

        self.damage = damage
        self.dx = math.cos (direction) * speed
        self.dy = math.sin (direction) * speed

        GameObject.__init__ (self, *args, **kw)
        self.tags ["class"] = "Bullet"

    def step (self, others, dt):

        for o in others:
            if self.hitbox.colliderect (o.hitbox) and hasattr (o, "hit"):
                o.hit (self.damage, self)
                raise Destroyed ("Bullet hit something.")

        self.position [0] += self.dx * dt
        self.position [1] += self.dy * dt

        GameObject.step (self, others, dt)

