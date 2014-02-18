"""
GameObjects that can be mounted on others.
self.position will be set first by mount.insert
and then synchronized by mountable.step, therefor
by convention mountable GameObjects should be 
instantiated with position as (0, 0).
"""

def init (self):
    self.root = None
    self.relative_position = None

def step (self, game_objects, dt):

    if self.root and self.relative_position:
        pos  = self.root.position
        rpos = self.relative_position
        self.position [0] = rpos [0] + pos [0]
        self.position [1] = rpos [1] + pos [1]
        self.hitbox.center = self.position

def draw (self, _):
    # for completeness' sake
    pass
