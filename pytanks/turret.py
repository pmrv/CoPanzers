import math, pygame

from pytanks import GameObject, target, mount
from pytanks.weapon import ExampleWeapon
from pytanks.util import make_color_surface

class Turret (GameObject):

    def __init__ (self, hp, mountpoints, *args, **kw):
        """
        hp     -- int, hitpoints for the turret
        mountpoints -- see pytanks.mount.init
        """

        self.target = None

        GameObject.__init__ (self, *args, **kw)
        self.tags ["class"] = "Turret"

        target.init (self, hp)
        mount.init (self, mountpoints)

    hit = target.hit
    insert = mount.insert

    def step (self, others, dt):

        target.step (self, others, dt)
        mount.step (self, others, dt)

    def draw (self, surface):

        GameObject.draw (self, surface)
        target.draw (self, surface)
        mount.draw (self, surface)

class ExampleTurret (Turret):

    __amount = 0 # amount of turrets instantiated 

    def __init__ (self, *args, **kw):

        s = make_color_surface (30, 30, (255, 255, 255))
        pygame.draw.polygon (s, (0, 155, 0), ((0, 15), (15, 0), (30, 15), (15, 30)))
        pygame.draw.polygon (s, (0, 0, 0), ((0, 15), (15, 0), (30, 15), (15, 30)), 1)
        Turret.__init__ (self, 80, ((0, 0),), s, s.get_size (), *args, **kw)
        self.insert (0, ExampleWeapon ())

        self.__amount += 1
        self.tags ["kind"] = "ExampleTurret"
        self.tags ["name"] = "{} {}".format (self.tags ["kind"], self.__amount)

    def step (self, others, dt):

        Turret.step (self, others, dt)
        if self.mounts [0] == None:
            return # we've nothing mounted yet

        if self.mounts [0].reloaded > 0:
            return

        if not self.target:
            try:
                self.target = next (filter (lambda x: x.tags ["class"] == "Barrier" and id (x) != id (self), others))
            except StopIteration:
                return 

        if self.target.health.hp <= 0:
            self.target = None
            return

        mpos = self.position
        tpos = self.target.position
        dx = tpos [0] - mpos [0]
        dy = tpos [1] - mpos [1]

        if dy == 0:
            angle = math.pi * (dx > 0)
        else:
            angle = math.acos (dx / math.sqrt (dx ** 2 + dy ** 2))

        bullet = self.mounts [0].shoot (-angle)
        others.append (bullet)
