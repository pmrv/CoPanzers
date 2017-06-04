# Copyright (C) 2014 Marvin Poul <ponder@creshal.de>
import math
from ctypes import byref, c_double

from ecs.exceptions import NonexistentComponentTypeForEntity

from copanzers.systems import LogSystem
from copanzers.components import *
from copanzers.util import gfx

class RenderSystem (LogSystem):

    def __init__(self, *args, **kw):
        LogSystem.__init__(self, *args, **kw)

    def update (self, _):

        # draw white background
        gfx.sdl.SDL_SetRenderDrawColor(gfx.renderer,
                                       255, 255, 255)
        gfx.sdl.SDL_RenderFillRect(gfx.renderer, None)

        eman = self.entity_manager
        renders = list (eman.pairs_for_type (Renderable))
        renders.sort (key = lambda x: x [1].layer)
        for e, renderable in renders:

            pos = eman.component_for_entity(e, Position)
            renderable.rect.center = map(int, (pos.x, pos.y))

            try:
                rot = eman.component_for_entity(e, Movement).angle
                gfx.sdl.SDL_RenderCopyEx(gfx.renderer, renderable.texture, None,
                                         byref(renderable.rect),
                                         c_double(math.degrees(rot)),
                                         None, 0x0)
            except NonexistentComponentTypeForEntity:
                gfx.sdl.SDL_RenderCopy(gfx.renderer, renderable.texture, None,
                                       byref(renderable.rect))
