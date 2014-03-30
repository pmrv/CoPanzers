# Copyright (C) 2014 Marvin Poul <ponder@creshal.de>
import math
from functools import partial

from copanzers.scripts import get_logger

def destroy_target (w, target):
    if w.till_reloaded <= 0:
        w.shoot ()
    return target.destroyed

def drive_circle (t, time, length):

    start = abs (time)
    while start + length > time:
        t.rotation = (time - start) / length * math.pi * 2
        yield (lambda: True)

def main (tank, time):

    x, y = tank.position

    tank.throttle = 1
    tank.rotation = - math.pi / 2
    yield (lambda: tank.position.y <= 50)

    tank.rotation = 0
    yield (lambda: tank.position.x >= 500)

    tank.rotation = math.pi / 2
    yield (lambda: tank.position.y >= 250)

    tank.rotation = - 5/6 * math.pi
    tank.throttle = 1
    yield (lambda: tank.position.x <= x)

    diff = y - tank.position.y
    tank.rotation = math.pi / 2 * diff / abs (diff)

    log = get_logger ("DemoTank")
    log.info ("Imma driving a circle!")
    tank.throttle = .5
    yield from drive_circle (tank, time, 4)

    tank.throttle = 0
    tank.rotation = 0

    log.info ("I'll be shooting everything in a radius of 200px.")
    cannon = tank.mounts [0]
    radar  = tank.mounts [1]

    for o in radar.visible:
        d = o.position - tank.position
        if abs (d) <= 200 and o != tank and o not in tank.mounts:
            cannon.rotation = d.angle
            yield partial (destroy_target, cannon, o)

