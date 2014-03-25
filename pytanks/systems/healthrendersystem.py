# Copyright (C) 2014 Marvin Poul <ponder@creshal.de>
import pygame
from ecs.exceptions import NonexistentComponentTypeForEntity

from pytanks.systems import LogSystem, RenderSystem
from pytanks.components import *

class HealthRenderSystem (RenderSystem):

    def update (self, _):

        eman = self.entity_manager

        for e, bar in eman.pairs_for_type (HealthBar):
            try: 
                health = eman.component_for_entity (e, Health)
                pos    = eman.component_for_entity (e, Position)
            except NonexistentComponentTypeForEntity as err:
                if   err.component_type == Health:
                    self.log.warn ("%s has a HealthBar but no Health component.", e)
                elif err.component_type == Position:
                    self.log.warn ("%s has no Position component, can't draw its \
                            health bar.", e)
                continue 

            # TODO: make this cooler

            border = pygame.Rect ( (pos.x + bar.topleft [0], pos.y + bar.topleft [1],
                                    bar.size [0], bar.size [1]) )

            pygame.draw.rect (self.surface, (0, 0, 0), border, 1)

            remaining = health.hp / health.max_hp * (bar.width - 2)
            # super efficient, I know but I'm too lazy to type it out…
            topleft_green = list (map (lambda x: x + 1, bar.topleft))
            size_green    = remaining, bar.height - 2
            topleft_green [0] += pos.x
            topleft_green [1] += pos.y

            pygame.draw.rect (self.surface, (0, 255, 0), (topleft_green, size_green))

            if health.hp == health.max_hp:
                continue

            topleft_red = [topleft_green [0] + remaining, topleft_green [1]]
            size_red    = (bar.width - 2) - remaining, bar.height - 2

            pygame.draw.rect (self.surface, (255, 0, 0), (topleft_red, size_red))
