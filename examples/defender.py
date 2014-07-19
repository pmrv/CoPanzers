from collections import defaultdict
import math

from copanzers.scripts import get_logger
L = get_logger ("Defender")

def main (tank, game):
    gun = tank.mounts [0]
    center = Vec2d (*map (lambda x: x / 2, game.size))

    tank.throttle = 1
    tank.rotation = (center - tank.position).angle

    start = game.time
    dt = (center - tank.position).length / tank.max_speed
    yield (lambda: start + dt <= game.time)
    tank.throttle = 0

    positions = defaultdict (list)
    dealtwith = set ()
    targets   = set ()

    width = max (tank.size)
    delta = gun.reload_time

    while 1:
        incoming = set (filter (lambda x: x ["Class"] == "Bullet", tank.visible))
        incoming.difference_update (dealtwith)

        for b in incoming:
            ps = positions [b]
            ps.append (Vec2d (*b.position))
            if len (ps) < 2:
                L.info ("Don't have a velocity estimate on {} yet.".format (b))
                continue

            # from now on we'll assume that we discovered the bullet delta
            # seconds before

            bv = (ps [-2] - ps [-1]) / delta
            bd = tank.position - ps [-1]
            if abs (bv.angle - bd.angle) < math.tan (width / bd.length):
                # bullet will miss us
                dealtwith.add (b)
                L.info ("{} will miss us.".format (b))
                continue

            # TODO: sophisticate
            gun.rotation = bd.angle + math.pi
            gun.shoot ()

            dealtwith.add (b)
            L.info ("Shot at {}.".format (b))
            break

        yield (lambda: gun.till_reloaded == 0)
