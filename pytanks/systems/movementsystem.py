from ecs.models import System
from ecs.exceptions import NonexistentComponentTypeForEntity

class MovementSystem (System):

    def update (self, dt):
        for e, vel in self.entity_manager.pairs_for_type (Movement):
            try:
                pos = self.entity_manager.component_for_entity (e, Position)
            except NonexistentComponentTypeForEntity:
                print ("No position component found for moving.")
                continue # shouldn't be happening, but just to be sure

            pos.x += vel.dx
            pos.y += vel.dy

            try:
                hitbox = self.entity_manager.component_for_entity (e, Hitbox)
                hitbox.center = pos.x, pos.y
            except NonexistentComponentTypeForEntity:
                print ("Entity has no hitbox, don't try to move it.")
                continue
