import math, pygame

from pytanks import GameObject, mobile, mountable
from pytanks.bullet import ExampleBullet
from pytanks.util   import Rect, make_color_surface

class Weapon (GameObject):

    direction = property (mobile.get_dir, mobile.set_dir)
    speed     = property (mobile.get_speed)

    def __init__ (self, reload_time, bullet, *args, **kw):
        """
        surface           -- pygame.Surface, what the weapon looks like
        reload_time       -- float
        bullet            -- pytanks.bullet.Bullet, bullets this weapon shoots
        """

        self.reload_time = reload_time
        self.bullet = bullet

        self.reloaded = 0
        GameObject.__init__ (self, *args, **kw)
        mobile.init (self, 0, 0)
        mountable.init (self)

    def shoot (self, angle):
        """
        returns a bullet, caller has to add it to the list of game objects
        angle -- float, direction in which to fire
        pos   -- 2 tuple of int, center of the object to which this weapon belongs
        """

        if self.reloaded > 0: return None

        self.reloaded  = self.reload_time
        self.direction = angle
        pos  = self.root.position
        rpos = self.relative_position
        # we need to place the bullet just outside the weapon because it looks
        # stupid when the bullets spawn at the center of the weapon
        d = self.texture.get_height () / 2
        dposx = math.cos (angle) * d 
        dposy = math.sin (angle) * d
        b = self.bullet (angle, (pos [0] + rpos [0] + dposx, pos [1] + rpos [1] + dposy),
                         root = self.root)

        b.tags ["team"] = self.root.tags ["team"]
        return b

    def step (self, game_objects, dt):
        if self.reloaded > 0:
            self.reloaded -= dt 

        pos  = self.root.position
        rpos = self.relative_position
        self.position [0] += pos [0] + rpos [0]
        self.position [1] += pos [1] + rpos [1]

        mobile.step (self, game_objects, dt)
        mountable.step (self, game_objects, dt)

    def draw (self, surface):
        mobile.draw (self, surface)

class ExampleWeapon (Weapon):

    def __init__ (self):

        h, w = 20, 20
        s = pygame.Surface ((h, w))
        s.set_colorkey ( (0, 0, 0) )
        pygame.draw.polygon (s, (0, 0, 150), ((w/2, 0), (w/2, h), (w, h/2)))

        # some arbitrarily chosen values
        # our hitbox is (0, 0) since we are no target
        # we give (0, 0) as position, since our real position will
        # later be set by mount.insert
        Weapon.__init__ (self, .1, ExampleBullet, s, (0, 0), (0, 0)) 
