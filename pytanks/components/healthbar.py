# Copyright (C) 2014 Marvin Poul <ponder@creshal.de>
import pygame
from ecs.models import Component

class HealthBar (Component, pygame.Rect):
    """
    Describes the position and size of the health bar relative to
    the center of the entity.
    """

    def __init__ (self, center, size):
        pygame.Rect.__init__ (self, center [0] - size [0] / 2,
                                    center [1] - size [1] / 2,
                                    *size)
