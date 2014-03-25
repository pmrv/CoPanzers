# Copyright (C) 2014 Marvin Poul <ponder@creshal.de>
import math
from functools import partial

def destroy_target (w, target):
    if w.till_reloaded <= 0:
        w.shoot ()
    return target.destroyed

def main (turret, view):

    x, y = turret.position
    cannon = turret.mounts [0]

    
    for b in list (filter (lambda x: x ["Class"] == "Barrier", view)):
        bx, by = b.position
        dx = bx - x
        dy = by - y
        if dy == 0:
            cannon.rotation = 0
        else:
            cannon.rotation = -math.acos (dx / math.sqrt (dx**2 + dy**2))
        
        yield partial (destroy_target, cannon, b)
