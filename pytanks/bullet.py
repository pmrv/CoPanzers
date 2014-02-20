import math, pygame

from pytanks import GameObject
from pytanks.util import Destroyed, make_color_surface
import pytanks.mobile as mobile
import pytanks.target as target

class Bullet (GameObject):

    direction = property (mobile.get_dir)
    speed     = property (mobile.get_speed)

    def __init__ (self, damage, speed, direction, hp, hitbox, *args, root = None, **kw):
        """
        damage -- int, how much damage the bullet does on impact
        speed  -- int, px/s
        direction  -- float, radians
        hp, hitbox -- see pytanks.target.init
        root   -- pytanks.GameObject, ignore this object when hitting something
                  (usually the object firing this bullet)
        """

        self.damage = damage
        self.root = root

        GameObject.__init__ (self, *args, **kw)
        mobile.init (self, speed, direction)
        target.init (self, hp, hitbox)
        self.tags ["class"] = "Bullet"

    hit = target.hit

    def step (self, others, dt):

        for o in others:
            if hasattr (o, "hit") and id (self.root) != id (o) != id (self) and self.hitbox.colliderect (o.hitbox):
                o.hit (self.damage, self)
                raise Destroyed ("Bullet hit something.")

        GameObject.step (self, others, dt)
        mobile.step (self, others, dt)
        target.step (self, others, dt)

    def draw (self, surface):
        mobile.draw (self, surface)

class ExampleBullet (Bullet):

    def __init__ (self, angle, *args, **kw):
        # as per usual, some random values as an example
        s = make_color_surface (5, 5, (255, 255, 0))
        pygame.draw.rect (s, (0, 0, 0), s.get_rect (), 1)
        Bullet.__init__ (self, 1, 80, angle, 1, (5, 5), s, *args, **kw)
        self.tags ["kind"] = "ExampleBullet"
