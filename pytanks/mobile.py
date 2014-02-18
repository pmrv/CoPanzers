"""
Objects that can move in a certain direction with a certain speed
and (might) change that direction.
Direction/Speed is set/get via a property
(propert (mobile.get_*, mobile.set_*)).
If direction or speed should be immutable, modify the property
accordingly, but make sure they are always set with the provided
setter functions.
"""

import math, pygame

def init (self, speed, angle):
    """
    speed     -- int
    direction -- float, in radians
    """
    self._speed = speed
    self._dir   = angle
    # first time initialization in case the object uses
    # direction/speed as read only values
    self.dx = math.cos (angle) * self.speed
    self.dy = math.sin (angle) * self.speed

def step (self, _, dt):

    if self.speed:
        self.position [0] += self.dx * dt
        self.position [1] += self.dy * dt
        self.hitbox.center = self.position

def draw (self, surface):

    pos = self.position
    tsurf = pygame.transform.rotate (self.texture, math.degrees (-self.direction))
    dest = tsurf.get_rect ()
    dest.center = (pos [0], pos [1])
    surface.blit (tsurf, dest) 

def get_speed (self):
    return self._speed

def set_speed (self, speed):

    self._speed = speed
    self.dx = math.cos (self.direction) * self._speed
    self.dy = math.sin (self.direction) * self._speed

def get_dir (self):
    return self._dir

def set_dir (self, angle):

    self._dir = angle
    if not self.speed: return

    self.dx = math.cos (angle) * self.speed
    self.dy = math.sin (angle) * self.speed
