import math, pygame

from pytanks import GameObject
import pytanks.weapon as weapon

class Turret (GameObject):

    def __init__ (self, *args, **kw):

        h, w = 20, 20
        s = pygame.Surface ((h, w))
        s.set_colorkey ( (0, 0, 0) )
        pygame.draw.polygon (s, (0, 0, 150), ((0, h/2), (w, h/2), (w/2, 0)))
        self.cannon = weapon.Weapon (s, 2, 20, 40, (0, 0)) 
        self.target = None

        GameObject.__init__ (self, *args, **kw)

    def step (self, others, dt):

        self.cannon.step (dt)

        if not self.target:
            self.target = next (filter (lambda x: hasattr (x, "health"), others))
            if not self.target: return

        if self.target.health.hp <= 0:
            self.target = None
            return

        if self.cannon.reloaded > 0:
            return # our weapon is not ready to fire

        mpos = self.position
        tpos = self.target.position
        dx = mpos [0] - tpos [0]
        dy = mpos [1] - tpos [1]
        angle = math.acos (dx / math.sqrt (dx ** 2 + dy ** 2))

        bullet = self.cannon.shoot (angle, mpos)
        others.append (bullet)

    def draw (self, surface):

        GameObject.draw (self, surface)
        self.cannon.draw (surface, self.position)

        if self.target:
            pygame.draw.circle (surface, (255, 0, 0), tuple (map (int, self.target.position)), 20, 1)
