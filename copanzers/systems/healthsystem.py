# Copyright (C) 2014 Marvin Poul <ponder@creshal.de>
from ecs.exceptions import NonexistentComponentTypeForEntity

from copanzers.systems import LogSystem
from copanzers.components import Health, Destroyed

class HealthSystem (LogSystem):

    def update (self, _):

        for e, health in self.entity_manager.pairs_for_type (Health):
            if health.hp <= 0:
                self.log.info ("%s was destroyed.", e)
                self.entity_manager.add_component (e, Destroyed ())
