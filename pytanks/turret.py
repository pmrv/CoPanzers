import math, pygame

from pytanks import GameObject
from pytanks import weapon
from pytanks import target
from pytanks.util import make_color_surface

class Turret (GameObject):

    def __init__ (self, hp, cannon, *args, **kw):
        """
        hp     -- int, hitpoints for the turret
        cannon -- pytanks.weapon.Weapon, the cannon for this turret
        """

        self.cannon = cannon
        self.target = None

        GameObject.__init__ (self, *args, **kw)
        target.init (self, hp)
        self.tags ["class"] = "Turret"

    hit = target.hit

    def step (self, others, dt):

        self.cannon.step (dt)
        target.step (self, others, dt)

    def draw (self, surface):

        GameObject.draw (self, surface)
        self.cannon.draw (surface)
        target.draw (self, surface)

class ExampleTurret (Turret):

    __amount = 0 # amount of turrets instantiated 

    def __init__ (self, *args, **kw):

        s = make_color_surface (30, 30, (255, 255, 255))
        pygame.draw.polygon (s, (0, 155, 0), ((0, 15), (15, 0), (30, 15), (15, 30)))
        pygame.draw.polygon (s, (0, 0, 0), ((0, 15), (15, 0), (30, 15), (15, 30)), 1)
        Turret.__init__ (self, 80, weapon.ExampleWeapon (self), s, s.get_size (), *args, **kw)

        self.__amount += 1
        self.tags ["kind"] = "ExampleTurret"
        self.tags ["name"] = "{} {}".format (self.tags ["kind"], self.__amount)

    def step (self, others, dt):

        Turret.step (self, others, dt)

        if not self.target:
            try:
                self.target = next (filter (lambda x: x.tags ["class"] == "Barrier" and id (x) != id (self), others))
            except StopIteration:
                return 

        if self.target.health.hp <= 0:
            self.target = None
            return

        if self.cannon.reloaded > 0:
            return # our weapon is not ready to fire

        mpos = self.position
        tpos = self.target.position
        dx = tpos [0] - mpos [0]
        dy = tpos [1] - mpos [1]

        angle = math.acos (dx / math.sqrt (dx ** 2 + dy ** 2))

        bullet = self.cannon.shoot (-angle)
        others.append (bullet)
