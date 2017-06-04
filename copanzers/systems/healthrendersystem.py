# Copyright (C) 2014 Marvin Poul <ponder@creshal.de>
from ctypes import byref

from copanzers.util import gfx, Rect
from ecs.exceptions import NonexistentComponentTypeForEntity

from copanzers.systems import LogSystem, RenderSystem
from copanzers.components import *

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

            border = Rect (int(pos.x + bar.topleft [0]),
                           int(pos.y + bar.topleft [1]),
                           bar.size [0], bar.size [1])

            gfx.sdl.SDL_SetRenderDrawColor(gfx.renderer, 0, 0, 0, 0)
            gfx.sdl.SDL_RenderDrawRect(gfx.renderer, byref(border))

            remaining = int(health.hp / health.max_hp * (bar.w - 2))
            green_rect = Rect(int(1 + bar.x + pos.x), int(1 + bar.y + pos.y),
                              remaining, bar.h - 2)

            gfx.sdl.SDL_SetRenderDrawColor(gfx.renderer, 0, 255, 0, 0)
            gfx.sdl.SDL_RenderFillRect(gfx.renderer, byref(green_rect))

            if health.hp == health.max_hp:
                continue

            red_rect = Rect(green_rect.x + remaining, green_rect.y,
                            bar.w - remaining - 2, bar.h - 2)

            gfx.sdl.SDL_SetRenderDrawColor(gfx.renderer, 255, 0, 0, 0)
            gfx.sdl.SDL_RenderFillRect(gfx.renderer, byref(red_rect))
