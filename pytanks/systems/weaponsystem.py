
import math

from pytanks.systems import LogSystem
from pytanks.components import *

from pytanks import make

class WeaponSystem (LogSystem):

    def update (self, dt):

        eman = self.entity_manager
        for e, weapon in eman.pairs_for_type (Weapon):

            if weapon.triggered:
                weapon.triggered = False
                weapon.till_reloaded = weapon.reload_time

                rot = eman.component_for_entity (e, Movement).rotation
                pos = eman.component_for_entity (e, Position)
                ign = (eman.component_for_entity (e, Mountable).root,)

                self.log.debug ("Weapon %s fired bullet from %s with angle %i°.",
                        e, pos, math.degrees (-rot))
                make.bullet (eman, weapon.bullet_properties, pos, -rot, ign)
            
            weapon.till_reloaded = max (0, weapon.till_reloaded - dt)
