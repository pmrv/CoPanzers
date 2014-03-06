from ecs.models import System

from pytanks.components.health import Health

class HealthSystem (System):

    def update (self, _):

        for e, health in self.entity_manager.pairs_for_type (Health):
            if health.hp <= 0:
                print ("Entity {} was destroyed.".format (e))
                self.entity_manager.remove_entity (e)
