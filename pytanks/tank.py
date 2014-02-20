import pygame, math

from pytanks import GameObject, mobile, target, mount
from pytanks.weapon import ExampleWeapon
from pytanks.util import make_color_surface

class Tank (GameObject):

    direction = property (mobile.get_dir,   mobile.set_dir)
    speed     = property (mobile.get_speed, mobile.set_speed)

    def __init__ (self, mountpoints, max_speed, hp, hitbox, *args, **kw):
        """
        max_speed   -- int, maximum speed the tank can drive
        mountpoints -- see pytanks.mount.init
        hp, hitbox  -- see pytanks.target.init
        """

        GameObject.__init__ (self, *args, **kw)
        target.init (self, hp, hitbox)
        mobile.init (self, 0, 0)
        mount.init (self, mountpoints)
        self.max_speed = max_speed

    hit = target.hit
    insert = mount.insert

    def step (self, others, dt):
        target.step (self, others, dt)
        mobile.step (self, others, dt)
        mount.step  (self, others, dt)

    def draw (self, surface):
        target.draw (self, surface)
        mobile.draw (self, surface)
        mount.draw (self, surface)


class JoystickTank (Tank):

    def __init__ (self, joystick, *args, **kw):
        """
        joystick -- pygame.joystick.Joystick, joystick through which we get our input
        """

        self.joystick = joystick
        s = make_color_surface (60, 40, (0, 200, 100))
        Tank.__init__ (self, ((0, 0),), 40, 100, (60, 40), s, *args, **kw)
        self.insert (0, ExampleWeapon ()) 

    def step (self, others, dt):

        jx = self.joystick.get_axis (0)
        jy = self.joystick.get_axis (1)
        throttle = (self.joystick.get_axis (2) + 1) / 2

        # eh…
        jx = jx if abs (jx) - .14 > 0 else 0
        jy = jy if abs (jy) - .14 > 0 else 0

        self.speed = throttle * self.max_speed
        if jy == 0 and jx != 0:
            self.direction = math.pi * (jx < 0)
        elif not (jx == jy == 0):
            self.direction = math.acos (jx / math.sqrt (jx ** 2 + jy ** 2)) * jy / abs (jy)

        Tank.step (self, others, dt)
