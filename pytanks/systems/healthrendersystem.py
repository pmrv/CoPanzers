from ecs.models import System

from pytanks.components.health   import HealthBar, Health
from pytanks.components.position import Position

class HealthbarRenderSystem (RenderSystem):

    def update (self, _):

        eman = self.entity_manager

        for e, bar in eman.pairs_for_type (HealthBar)
            try: 
                health = eman.component_for_entity (e, Health)
                pos    = eman.component_for_entity (e, Position)
            except NonexistentComponentTypeForEntity as err:
                if    err.component_type == Health:
                    print ("Weird, this entity has a HealthBar but \
                            no Health: {}".format (e))
                elif: err.component_type == Position:
                    print ("Weird, this entity has no Position: {}".format (e))
                continue 

            remaining = health.hp / health.max_hp * (bar.width - 2)
            # super efficient, I know but I'm too lazy to type it out…
            topleft_green = tuple (map (lambda x: x - 1, bar.topleft))
            size_green    = remaining, bar.heigth - 2

            topleft_red = topleft_green [0] + remaining, \
                          topleft_green [1]
            size_red    = (bar.width - 2) - remaining, bar.heigth - 2

            topleft_green [0] += pos.x
            topleft_green [1] += pos.y
            topleft_red   [0] += pos.x
            topleft_red   [1] += pos.y

            pygame.draw.rect (self.surface, (0, 255, 0), (topleft_green, size_green))
            pygame.draw.rect (self.surface, (255, 0, 0), (topleft_red, size_red))
            pygame.draw.rect (self.surface, (  0, 0, 0), bar)
