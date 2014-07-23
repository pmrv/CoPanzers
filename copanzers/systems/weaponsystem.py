# Copyright (C) 2014 Marvin Poul <ponder@creshal.de>
import math

from copanzers.systems import LogSystem
from copanzers.components import *
from copanzers import make

class WeaponSystem (LogSystem):

    def update (self, dt):

        eman = self.entity_manager
        for e, weapon in eman.pairs_for_type (Weapon):

            weapon.till_reloaded = max (0, weapon.till_reloaded - dt)

            if weapon.triggered:

                weapon.triggered = False
                if weapon.till_reloaded > 0:
                    continue

                weapon.till_reloaded = weapon.reload_time

                rot = eman.component_for_entity (e, Movement).angle
                pos = eman.component_for_entity (e, Position)
                ign = (eman.component_for_entity (e, Mountable).root,)
                make.make (eman, None, weapon.bullet_type, rot, ign, pos = pos)

                self.log.debug ("Weapon %s fired bullet from %s with angle %i°.",
                        e, pos, math.degrees (-rot))
