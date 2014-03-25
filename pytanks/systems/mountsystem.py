# Copyright (C) 2014 Marvin Poul <ponder@creshal.de>
from ecs.exceptions import NonexistentComponentTypeForEntity

from pytanks.systems import LogSystem
from pytanks.components import *

class MountSystem (LogSystem):

    def update (self, dt):

        eman = self.entity_manager
        for e, m in eman.pairs_for_type (Mount):

            try: 
                pos = eman.component_for_entity (e, Position)
            except NonexistentComponentTypeForEntity:
                self.log.warn ("%s has a Mount but no Position component, \
                        cannot adjust the position of the mounted entities.", e)
                continue

            for i in range (m.amount):
                im = m.mounts [i]
                if im is None: continue

                try: 
                    ipos = eman.component_for_entity (im, Position)
                    ipos.x = pos.x + m.points [i] [0]
                    ipos.y = pos.y + m.points [i] [1]

                except NonexistentComponentTypeForEntity:
                    self.log.warn ("%s is mounted on %s, but has no Position \
                            component, cannot adjust it.")
                    continue
