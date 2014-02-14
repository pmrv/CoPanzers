import math, pygame

from pytanks.bullet import Bullet
from pytanks.util   import Rect

class Weapon:

    def __init__ (self, surface, reload_time, damage, 
                  muzzle_speed, relative_position):
        """
        surface           -- pygame.Surface, what the weapon looks like
        reload_time       -- float
        relative_position -- 2 tuple of int, center of the weapon 
                             relative to object it is attached to
        damage            -- int
        muzzle_speed      -- int, px/sec
        """

        self.relative_position = relative_position
        self.muzzle_speed = muzzle_speed
        self.reload_time = reload_time
        self.surface = surface
        self.damage = damage

        self.rotation = 0 # direction in which the last bullet was fired
        self.reloaded = 0

    def shoot (self, angle, pos):
        """
        returns a bullet, caller has to add it to the list of game objects
        angle -- float, direction in which to fire
        pos   -- 2 tuple of int, center of the object to which this weapon belongs
        """

        if self.reloaded > 0: return None

        self.reloaded = self.reload_time
        self.rotation = angle
        rpos = self.relative_position
        return Bullet (self.muzzle_speed, -angle, self.damage, 
                       (255, 255, 0), (pos [0] + rpos [0], pos [1] + rpos [1]), (5, 5))

    def step (self, dt):
        self.reloaded -= dt

    def draw (self, surface, pos):
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
        Weapon.__init__ (self, s, .1, 1, 80, (0, 0), *args, **kw) 
