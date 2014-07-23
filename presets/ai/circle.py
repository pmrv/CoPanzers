from functools import partial
import math

Now = lambda: True

def kill (tank, target):
    gun = tank.mounts [0]
    gun.rotation = (target - tank.position).angle
    if gun.till_reloaded == 0:
        gun.shoot ()

    return True

def drive_circle (tank, game, center, number, action = Now):
    """
    center -- Vec2d, about which point to drive circles
    number -- float, how many circles to drive
    """

    start  = game.time
    phase  = (center - tank.position).angle - math.pi / 2
    radius = (center - tank.position).length
    period = (2 * math.pi * radius) / tank.max_speed

    while start + number * period > game.time:
        tank.rotation = tank.speed * (game.time - start) / radius + phase

        yield action

def main (tank, game):
    gun = tank.mounts [0]
    radius = 80
    center = Vec2d (*map (lambda x: x / 2, game.size))

    tank.throttle = 1
    tank.rotation = (center - tank.position).angle

    yield (lambda: abs (tank.position - center) <= radius)

    shoot_center = partial (kill, tank, center)
    yield from drive_circle (tank, game, center, .5,
                shoot_center)

    vr = 10 # radial speed
    vc = math.sqrt (tank.max_speed ** 2 - vr ** 2)
    start = game.time
    a = math.atan2 (vr, vc)

    while 1:
        while abs (center - tank.position) < 120:
            p = (center - tank.position).angle
            tank.rotation = -math.pi / 2 - a + p
            yield shoot_center

        yield from drive_circle (tank, game, center, 2,
                    shoot_center)

        while abs (center - tank.position) >  80:
            p = (center - tank.position).angle
            tank.rotation = -math.pi / 2 + a + p
            yield shoot_center

        yield from drive_circle (tank, game, center, 2,
                    shoot_center)

    tank.throttle = 0
