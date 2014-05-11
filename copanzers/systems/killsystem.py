# Copyright (C) 2014 Marvin Poul <ponder@creshal.de>

from ecs.exceptions import NonexistentComponentTypeForEntity

from copanzers.systems import LogSystem
from copanzers.components import Destroyed, Mount, Tags

def strip_entity (eman, e):
    """
    strip all components except Destroyed from an entity and all mounted
    entities
    """
    try:
        for m in eman.component_for_entity (e, Mount).mounts:
            strip_entity (eman, m)
    except NonexistentComponentTypeForEntity:
        pass
    finally:
        eman.remove_entity (e)
        eman.add_component (e, Destroyed ())

class KillSystem (LogSystem):

    def update (self, _):

        eman = self.entity_manager
        # pairs_for_type returns an iterator, so we make a copy of it to avoid
        # changing it while looping over it
        for e, _ in tuple (eman.pairs_for_type (Destroyed)):
            strip_entity (eman, e)
