# Copyright (C) 2014 Marvin Poul <ponder@creshal.de>
import math
from functools import partial

def destroy_target (w, target):
    if w.till_reloaded <= 0:
        w.shoot ()
    return target.destroyed

def main (turret, time):

    x, y = turret.position
    cannon = turret.mounts [0]
    
    for b in filter (lambda x: x ["Class"] == "Barrier", turret.visible):
        bx, by = b.position
        dx, dy = bx - x, by - y
        if dy == 0:
            cannon.rotation = 0 + math.pi * (dx < 0)
        else:
            cannon.rotation = math.acos (dx / math.sqrt (dx**2 + dy**2)) * dy / abs (dy)
        
        yield partial (destroy_target, cannon, b)
