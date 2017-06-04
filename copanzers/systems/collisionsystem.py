# Copyright (C) 2014 Marvin Poul <ponder@creshal.de>
from ecs.exceptions import NonexistentComponentTypeForEntity

from copanzers.systems import (LogSystem, 
                               components_for_entity)

from copanzers.components import *


class CollisionSystem (LogSystem):

    def update (self, dt):
        # for now just do collision detection for Projectiles

        eman = self.entity_manager
        for e, proj in eman.pairs_for_type (Projectile):

            try:
                ehit, epos = components_for_entity (eman, e, (Hitbox, Position))
                ehit.center = epos.x, epos.y
            except NonexistentComponentTypeForEntity:
                self.log.warn ("Skipping projectile %s for collision detection as \
                        it has either no Position or Hitbox component.", e)
                continue

            for o, ohit in eman.pairs_for_type (Hitbox):
                if e == o or o in proj.ignore: continue

                try:
                    opos = eman.component_for_entity (o, Position)
                except:
                    self.log.debug ("Skipping %s for collision dectection as it \
                            has no Position component.", o)
                    continue

                ohit.center = opos.x, opos.y

                if ehit.colliderect (ohit):

                    self.log.debug ("Projectile %s (at %s) hit %s (at %s).",
                                    e, epos, o, opos)
                    eman.add_component (e, Destroyed ())

                    try:
                        ohealth = eman.component_for_entity (o, Health)
                        ohealth.hp -= proj.damage
                    except NonexistentComponentTypeForEntity:
                        self.log.info ("%s was hit but has no Health component, \
                                so it took no damage.", o)

                    break

