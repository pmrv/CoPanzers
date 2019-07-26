"""Copyright (C) 2017 Marvin Poul <ponder@creshal.de>"""

from logging import getLogger
import sdl2 as sdl
from ctypes import byref, POINTER

class GfxError(Exception): pass

SDL_INIT_VIDEO = 0x20

class SDLState:

    running = False

    def __init__(self, *, resolution = None):
        """
        Setup SDL libary binding, if resolution is given, call the open()
        method with it. SDLState.running is True if a SDL_QUIT event was
        received at anytime and False otherwise.
        """

        self.window = POINTER(sdl.SDL_Window)()
        self.renderer = POINTER(sdl.SDL_Renderer)()

        self.__logger = getLogger()

        if resolution:
            self.open(resolution = resolution)

    def open(self, resolution):
        """
        Open new window with the given resolution (width, height).
        """

        width, height = resolution

        if sdl.SDL_Init(SDL_INIT_VIDEO) != 0:
            err = "Failed to initialize SDL: " \
                + sdl.SDL_GetError()
            self.__logger(err)
            raise OSError(err)

        sdl.SDL_CreateWindowAndRenderer(width, height, 0,
                                        byref(self.window),
                                        byref(self.renderer))
        if self.window.contents == None or self.renderer.contents == None:
            err = "Failed to create window/renderer: " \
                + sdl.SDL_GetError()
            self.__logger(err)
            raise OSError(err)

        self.running = True

    def close(self):
        """
        Free all SDL objects and call SDL_Quit..
        """

        sdl.SDL_DestroyRenderer(self.renderer)
        sdl.SDL_DestroyWindow(self.window)
        sdl.SDL_Quit()

    def __enter__(self):

        return self

    def __exit__(self, *_):

        self.close()
        return False

    def poll(self):
        """
        CHeck for new SDL event and update properties if necessary.
        """

        event = sdl.SDL_Event()
        while sdl.SDL_PollEvent(byref(event)):
            if event.type == sdl.SDL_QUIT:
                self.running = False
