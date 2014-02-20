import pygame, math

from .util import Rect, make_color_surface

class GameObject:

    def __init__ (self, texture, position):
        """
        texture  -- pygame Surface or pygame Color
        position -- 2 tuple of int, initial position (centered) on the screen
        """

        if not isinstance (texture, pygame.Surface):
            raise TypeError ("Parameter $texture must be a pygame Surface.")

        self.texture = texture
        self.position = list (position)
        # holds misc data about the object
        # class -- what class of objects does it belongs to? Turret/Bullet/Whatever
        # kind  -- what kind of Turret/Bullet/Whatever is it?
        # team  -- objects with the same self.tags["team"] e.g. should normally 
        #          not attack each other, but compliance is not mandatory
        # name  -- name for display, should be unique but does not have to be, 
        #          use id(obj) if you need a unique identifier
        self.tags = {"class": None, "kind": None, "team": None, "name": None} 

    def step (self, game_objects, relative_time):
        """
        game_objects  -- list, well, duh, a list of all
                               game objects currently in the game
        relative_time -- float, modifier to influence to overall 
                                pace of the game and to accommodate 
                                between different fps
        """
        pass

    def draw (self, surface):
        """
        surface -- pygame.Surface, surface we draw ourselves to
        """
        surface.blit (self.texture, (self.position [0] - self.texture.get_width () / 2,
                                    self.position [1] - self.texture.get_height () / 2))
