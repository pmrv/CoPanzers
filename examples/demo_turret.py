# Copyright (C) 2014 Marvin Poul <ponder@creshal.de>
import math
from functools import partial

def destroy_target (w, target):
    if w.till_reloaded <= 0:
        w.shoot ()
    return target.destroyed

def main (turret, game):

    cannon = turret.mounts [0]

    for b in filter (lambda x: x ["Class"] == "Barrier", turret.visible):
        cannon.rotation = (b.position - turret.position).angle

        yield partial (destroy_target, cannon, b)
