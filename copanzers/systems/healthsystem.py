# Copyright (C) 2014 Marvin Poul <ponder@creshal.de>
from ecs.exceptions import NonexistentComponentTypeForEntity

from copanzers.systems import LogSystem
from copanzers.components import *

from copanzers.util import destroy_entity

class HealthSystem (LogSystem):

    def update (self, _):

        destroyed = []
        for e, health in self.entity_manager.pairs_for_type (Health):
            if health.hp <= 0:
                self.log.info ("%s was destroyed.", e)
                destroyed.append (e)

        for e in destroyed:
            destroy_entity (self.entity_manager, e)
