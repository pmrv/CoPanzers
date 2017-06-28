# Copyright (C) 2014 Marvin Poul <ponder@creshal.de>
import math
from ctypes import byref

from ecs.exceptions import NonexistentComponentTypeForEntity
import sdl2 as sdl

from copanzers.systems import LogSystem
from copanzers.components import *

class RenderSystem (LogSystem):

    def __init__(self, gfx, *args, **kw):
        self.gfx = gfx
        LogSystem.__init__(self, *args, **kw)

    def update (self, _):

        # draw white background
        sdl.SDL_SetRenderDrawColor(self.gfx.renderer, 255, 255, 255, 255)
        sdl.SDL_RenderFillRect(self.gfx.renderer, None)

        eman = self.entity_manager
        renders = list (eman.pairs_for_type (Renderable))
        renders.sort (key = lambda x: x [1].layer)
        for e, renderable in renders:

            pos = eman.component_for_entity(e, Position)
            renderable.rect.center = map(int, (pos.x, pos.y))

            try:
                rot = eman.component_for_entity(e, Movement).angle
                sdl.SDL_RenderCopyEx(self.gfx.renderer, renderable.texture, None,
                                     byref(renderable.rect), math.degrees(rot),
                                     None, 0x0)
            except NonexistentComponentTypeForEntity:
                sdl.SDL_RenderCopy(self.gfx.renderer, renderable.texture, None,
                                   byref(renderable.rect))
