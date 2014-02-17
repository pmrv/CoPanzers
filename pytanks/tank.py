import pygame, math
from pytanks import GameObject, mobile, target
from pytanks.weapon import ExampleWeapon

class Tank (GameObject):

    direction = property (mobile.get_dir,   mobile.set_dir)
    speed     = property (mobile.get_speed, mobile.set_speed)

    def __init__ (self, hp, max_speed, cannon, *args, **kw):
        """
        hp        -- int
        max_speed -- int, maximum speed the tank can drive
        cannon    -- pytanks.weapon.Weapon, cannon to mount on this tank
        """

        GameObject.__init__ (self, *args, **kw)
        target.init (self, hp)
        mobile.init (self, 0, 0)
        self.cannon = cannon
        self.max_speed = max_speed

    hit = target.hit

    def step (self, others, dt):
        mobile.step (self, others, dt)
        target.step (self, others, dt)
        self.cannon.step (dt)
        GameObject.step (self, others, dt)

    def draw (self, surface):
        mobile.draw (self, surface)
        target.draw (self, surface)
        self.cannon.draw (surface)


class JoystickTank (Tank):

    def __init__ (self, joystick, *args, **kw):
        """
        joystick -- pygame.joystick.Joystick, joystick through which we get our input
        """

        self.joystick = joystick
        s = pygame.Surface ( (60, 40) )
        s.fill ( (0, 255, 0) )
        Tank.__init__ (self, 100, 40, ExampleWeapon (self), s, *args, **kw)

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
        elif jx != 0:
            self.direction = math.acos (jx / math.sqrt (jx ** 2 + jy ** 2)) * jy / abs (jy)

        Tank.step (self, others, dt)
