# Copyright (C) 2014 Marvin Poul <ponder@creshal.de>

from ecs.models import Component
import sdl2 as sdl
from sdl2 import sdlimage
import ctypes

from copanzers.util import Rect
from copanzers.sdl import GfxError

class Renderable (Component):
    __slots__ = ("texture", "layer", "drect")

    @classmethod
    def file(cls, gfx, path, **kw):
        texture = sdlimage.IMG_LoadTexture(gfx.renderer, path.encode("utf8"))
        if texture == None:
            raise FileNotFound("texture file {} does not exist".format(path))

        return cls(gfx, texture, **kw)

    @classmethod
    def color(cls, gfx, size, color, **kw):
        surface = sdl.SDL_CreateRGBSurface(0, *map(int, size), 32, 0, 0, 0, 0)
        if surface == None:
            raise GfxError("failed to create surface: "
                            + sdl.SDL_GetError().decode("utf8"))

        sdl.SDL_FillRect(surface, None,
                         sum(c << 16 * i for i, c in enumerate(color)))

        try:
            return cls(gfx, sdl.SDL_CreateTextureFromSurface(gfx.renderer, surface), **kw)
        finally:
            sdl.SDL_FreeSurface(surface)

    def __init__ (self, gfx, texture, layer = 0):
        """
        Note that entities that are Renderable also need at least the Position Component.
        texture -- opaque pointer to SDL texture
        layer   -- int, entities with lower layer are drawn first, negative layers are legal
        """

        if texture == None:
            raise GfxError("invalid texture given"
                            + sdl.SDL_GetError().decode("utf8"))
        self.texture = texture

        w, h = ctypes.c_int(), ctypes.c_int()
        ret = sdl.SDL_QueryTexture(texture, None, None,
                                   ctypes.byref(w), ctypes.byref(h))
        if ret != 0:
            raise GfxError("failed to query given texture: "
                            + sdl.SDL_GetError().decode("utf8"))

        self.rect = Rect(0, 0, w, h)

        self.layer = layer
