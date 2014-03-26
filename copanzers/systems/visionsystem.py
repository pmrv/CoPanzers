# Copyright (C) 2014 Marvin Poul <ponder@creshal.de>

import math

from copanzers.systems import LogSystem
from copanzers.components import Vision, Position
from copanzers.scripts import ROInterface

class VisionSystem (LogSystem):

    kinds = {
        # don't make the distinction yet
        "plain": ROInterface,
        "radar": ROInterface
    }

    def update (self, _):

        # we're doing the simplest possible thing for now in here
        eman = self.entity_manager
        for e, vis in eman.pairs_for_type (Vision):
            
            epos = eman.component_for_entity (e, Position)
            vis.visible = []
            for o, opos in eman.pairs_for_type (Position):
                dx, dy = epos.x - opos.x, epos.y - opos.y
                if dx ** 2 + dy ** 2 < vis.reach ** 2:
                    vis.visible.append (self.kinds [vis.kind] (o, eman))
