from pytanks import GameObject
import pytanks.target as target

class Barrier (GameObject):

    def __init__ (self, hp, *args, **kw):
        GameObject.__init__ (self, *args, **kw)
        target.init (self, hp)
        self.tags ["class"] = "Barrier"

    hit = target.hit

    def step (self, o, t):
        GameObject.step (self, o, t)
        target.step (self, o, t)

    def draw (self, surface):
        GameObject.draw (self, surface)
        target.draw (self, surface)
