"""
GameObjects one can mount others on.
Get the maximum number of mounting points via
self.mount_num and their relative positions via
self.mountpoints. Use the indices of the latter 
as $point_id when calling self.mount().
"""

def init (self, mountpoints):
    """
    mountpoints -- iterable of 2 tuple of int,
                   list of relative coordinates of 
                   the centers of the mountpoints
    """

    self.mountpoints = list (mountpoints)
    self.mount_num   = len (self.mountpoints)
    if self.mount_num == 0:
        raise ValueError ("A mount without mounting points is pointless.")
    self.mounts = [None] * self.mount_num

def insert (self, point_id, gadget):
    """
    point_id  -- int, from 0 to $self.mount_num, specifies 
                 which mounting point to use
    gadget -- pytanks.GameObject, the object to be place on
                 the mounting point, must implement the mountable
                 behaviour
    """

    if point_id >= self.mount_num:
        raise KeyError ("Point id to high.")
    if self.mounts [point_id]: 
        raise KeyError ("Mounting point already taken.")

    gadget.root = self
    gadget.relative_position = self.mountpoints [point_id]

    pos  = self.position
    rpos = gadget.relative_position
    gadget.position [0] = rpos [0] + pos [0]
    gadget.position [1] = rpos [1] + pos [1]
    if hasattr (gadget, "hitbox"):
        gadget.hitbox.center = gadget.position

    self.mounts [point_id] = gadget

def step (self, game_objects, dt):
    for m in self.mounts:
        if m: 
            m.step (game_objects, dt)

def draw (self, surface):
    for m in self.mounts:
        if m: m.draw (surface)
