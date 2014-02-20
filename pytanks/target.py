"""
Objects which can be shot at and take damage.
"""

import pygame
from .util import Destroyed, Rect

def init (self, hp, hitbox, center = None, size = None, *args):
    """
    inits a health bar when hp > 0 else 
    takes the object for invincible
    hp           -- int
    hitbox       -- 2 tuple of int, size of the hitbox of the object
    center, size -- 2 tuple of int, describing position and
                    size of the healthbar, center is relative
                    to $self.position
    """

    self.hitbox = Rect (self.position, hitbox)

    if center == None:
        center = 0, - self.hitbox.height * .75
    if size == None:
        size = (.75 * self.hitbox.width, 5)

    if hp > 0:
        self.health = HealthBar (hp, center, size, self, *args)

def draw (self, surface):
    if hasattr (self, "health"):
        self.health.draw (surface)

def step (self, a, b):
    if hasattr (self, "health") and self.health.hp <= 0:
        raise Destroyed ("{} destroyed.".format (self))

def hit (self, damage, aggressor):
    """
    damage    -- int, damage done
    aggressor -- obj, object which is hitting this one
    """
    self.health.hp -= damage

class HealthBar:

    def __init__ (self, max_hp, center, size, root, fg = (0, 255, 0), bg = (255, 0, 0)):
        """
        draws a health bar at a given point for a given number of health points
        max_hp -- int, full hp
        center -- 2 tuple of int, center of the bar
        size   -- 2 tuple of int, size of bar
        fg, bg -- 3 tuple of int or pygame Color, fore/background of the bar 
        """

        self.hp, self.max_hp = max_hp, max_hp
        self.height =  size [1] - 2
        self.dwidth = (size [0] - 2)/ max_hp
        self.center = center
        self.root = root
        self.fg, self.bg = fg, bg

    def draw (self, surface):

        pos = self.root.position
        topleft = pos [0] + self.center [0] - self.max_hp * self.dwidth / 2, pos [1] + self.center [1] - self.height / 2
        pygame.draw.rect (surface, self.fg, (topleft, (self.hp * self.dwidth - 1, self.height)))
        if self.hp < self.max_hp:
            pygame.draw.rect (surface, self.bg, ((topleft [0] + self.hp * self.dwidth, topleft [1]), 
                                       ((self.max_hp - self.hp) * self.dwidth - 1, self.height)))
        pygame.draw.rect (surface, (0, 0, 0), ((topleft [0] - 1, topleft [1] - 1),
                                               (self.dwidth * self.max_hp, self.height + 2)), 1)
