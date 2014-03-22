
import pygame
from ecs.exceptions import NonexistentComponentTypeForEntity

from pytanks.systems import LogSystem
from pytanks.components import *

class MovementSystem (LogSystem):

    def __init__ (self, width, height):
        """
        width, height -- int, specify size of the visible screen
        """
        self.screen = pygame.Rect ( (0, 0, width, height) )
        LogSystem.__init__ (self)

    def update (self, dt):
        remove = []
        for e, vel in self.entity_manager.pairs_for_type (Movement):
            try:
                pos = self.entity_manager.component_for_entity (e, Position)
            except NonexistentComponentTypeForEntity:
                self.log.warn ("%s has a Movement but no Position component, \
                        cannot move it.", e)
                continue 

            pos.x += vel.dx
            pos.y += vel.dy

            if not self.screen.collidepoint (pos):
                self.log.debug ("%s left the visible screen at %s, removing it.",
                        e, pos)
                remove.append (e) # remove all entities which disappear from the game screen

            try:
                hitbox = self.entity_manager.component_for_entity (e, Hitbox)
                hitbox.center = pos.x, pos.y
            except NonexistentComponentTypeForEntity:
                continue

        for e in remove:
            self.entity_manager.remove_entity (e)
