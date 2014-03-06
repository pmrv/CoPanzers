from ecs.models import System

from pytanks.components.position import Position, Movement
from pytanks import make

class WeaponSystem (System):

    def update (self, dt):

        eman = self.entity_manager
        for e, weapon in eman.pairs_for_type (Weapon):

            if weapon.triggered:
                weapon.triggered = False
                weapon.till_reloaded = weapon.reload_time

                mov = eman.component_for_entity (e, Movement)
                pos = eman.component_for_entity (e, Position)

                rot = mov.rotation
                make.bullet (eman, weapon, pos, rot)
            
            weapon.till_reloaded = max (0, weapon.till_reloaded - dt)


