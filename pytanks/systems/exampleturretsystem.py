
import math
from ecs.exceptions import NonexistentComponentTypeForEntity

from pytanks.systems import LogSystem
from pytanks.components import *

class ExampleTurretSystem (LogSystem):

    def update (self, dt):

        eman = self.entity_manager
        for e, turret in eman.pairs_for_type (ExampleTurret):

            if turret.target == None:
                # shot at the first barrier we find
                for c, tags in eman.pairs_for_type (Tags):
                    if tags ["Class"] == "Barrier":
                        turret.target = c
                        self.log.info ("Turret %s found new target %s.", e, c)
                        break
                else:
                    continue # can't find new targets

            try:
                target_pos = eman.component_for_entity (turret.target, Position)
            except NonexistentComponentTypeForEntity:
                # target has no position, assume it no longer exists
                self.log.info ("Turret %s lost target %s.", e, turret.target) 
                turret.target = None
                continue

            mount  = eman.component_for_entity (e, Mount)
            weapon = eman.component_for_entity (mount.mounts [0], Weapon) 
            if weapon.till_reloaded > 0:
                continue

            turret_pos = eman.component_for_entity (e, Position)
            weapon_mov = eman.component_for_entity (mount.mounts [0], Movement)

            diff = target_pos.x - turret_pos.x, target_pos.y - turret_pos.y

            weapon_mov.rotation = math.acos (
                diff [0] / math.sqrt (diff [0] ** 2 + diff [1] ** 2)
            ) 
            
            weapon.triggered = True
