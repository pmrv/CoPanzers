# Copyright (C) 2014 Marvin Poul <ponder@creshal.de>
import math
from functools import partial

from pytanks.util import RefFloat
from pytanks.scripts import get_logger

def drive_circle (t, time, length, start = RefFloat (0)):
    # the whole mess with $start is pretty quick and dirty
    if start == 0:
        start += abs (time)

    if start + length <= time:
        start -= abs (start)
        return True

    t.rotation = (time - start) * length / math.pi
    return False

def main (tank, view):

    log = get_logger ("DemoTank")

    x, y = tank.position

    tank.throttle = 1
    log.info ("Imma driving a circle!")
    yield partial (drive_circle, tank, view.time, 10)
    log.info ("Should I do it again?")

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
    yield (lambda: abs (tank.position.y - y) <= 10)

    yield partial (drive_circle, tank, view.time, 10)

    tank.throttle = 0
    tank.rotation = 0
