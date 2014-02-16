import math, pygame

from pytanks.bullet import Bullet
from pytanks.util   import Rect

class Weapon:

    def __init__ (self, surface, reload_time, bullet_hp, damage, 
                  muzzle_speed, relative_position, kind, root):
        """
        surface           -- pygame.Surface, what the weapon looks like
        reload_time       -- float
        relative_position -- 2 tuple of int, center of the weapon 
                             relative to object it is attached to
        bullet_hp         -- int, how much damage the bullet itself can take
        damage            -- int, how much damage the bullet does on impact
        muzzle_speed      -- int, px/sec
        kind              -- str, the kind with which our bullets are tagged
        root              -- pytanks.GameObject, the object this weapon is placed on
        """

        self.relative_position = relative_position
        self.muzzle_speed = muzzle_speed
        self.reload_time = reload_time
        self.bullet_hp = bullet_hp
        self.surface = surface
        self.damage = damage
        self.root = root
        self.kind = kind 

        self.direction = 0 # direction in which the last bullet was fired
        self.reloaded = 0

    def shoot (self, angle):
        """
        returns a bullet, caller has to add it to the list of game objects
        angle -- float, direction in which to fire
        pos   -- 2 tuple of int, center of the object to which this weapon belongs
        """

        if self.reloaded > 0: return None

        self.reloaded = self.reload_time
        self.rotation = -angle
        pos  = self.root.position
        rpos = self.relative_position
        b = Bullet (self.bullet_hp, self.damage, self.muzzle_speed, angle, 
                    (255, 255, 0), (pos [0] + rpos [0], pos [1] + rpos [1]), (5, 5))

        # not really content with that
        b.tags ["kind"] = self.kind
        b.tags ["team"] = self.root.tags ["team"]
        return b

    def step (self, dt):
        self.reloaded -= dt

    def draw (self, surface):
        pos  = self.root.position
        rpos = self.relative_position
        tsurf = pygame.transform.rotate (self.surface, math.degrees (self.rotation - math.pi / 2))
        dest = tsurf.get_rect ()
        dest.center = (pos [0] + rpos [0], pos [1] + rpos [1])
        surface.blit (tsurf, dest) 

class ExampleWeapon (Weapon):

    def __init__ (self, *args, **kw):

        h, w = 20, 20
        s = pygame.Surface ((h, w))
        s.set_colorkey ( (0, 0, 0) )
        pygame.draw.polygon (s, (0, 0, 150), ((0, h/2), (w, h/2), (w/2, 0)))

        # some arbitrarily chosen values
        Weapon.__init__ (self, s, .1, 1, 1, 80, (0, 0), "ExampleWeapon", *args, **kw) 
