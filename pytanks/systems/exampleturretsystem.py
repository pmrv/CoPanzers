from ecs.models import System

from pytanks.components.tags import Tags
from pytanks.position import Movement, Position
from pytanks.weapon import Weapon


class ExampleTurretSystem (System):

    def update (self, dt):

        eman = self.entity_manager
        for e, turret in eman.pairs_for_type (ExampleTurret):

            if turret.target == None:
                # shot at the first barrier we find
                for c, tags in eman.pairs_for_type (Tags)
                    if tags ["Class"] == "Barrier":
                        turret.target = c
                        break

            weapon = eman.component_for_entity (e, Weapon)
            if weapon.till_reloaded:
                continue

            target_pos = eman.component_for_entity (turret.target, Position)
            turret_pos = eman.component_for_entity (e, Position)
            turret_mov = eman.component_for_entity (e, Movement)

            diff = target_pos [0] - turret_pos [0], target_pos [1] - turret_pos [1]

            turret_mov.rotation = math.cos (
                diff [0] / math.sqrt (diff [0] ** 2 + diff [1] ** 2)
            )
            
            weapon.triggered = True
