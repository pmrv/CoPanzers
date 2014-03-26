# Copyright (C) 2014 Marvin Poul <ponder@creshal.de>
import pygame
from ecs.exceptions import NonexistentComponentTypeForEntity

from copanzers.systems import LogSystem
from copanzers.components import *
from copanzers.util import destroy_entity

class MovementSystem (LogSystem):

    def __init__ (self, width, height):
        """
        width, height -- int, specify size of the visible screen
        """
        self.screen = pygame.Rect ( (0, 0, width, height) )
        super ().__init__ ()

    def update (self, dt):
        remove = []
        for e, vel in self.entity_manager.pairs_for_type (Movement):
            try:
                pos = self.entity_manager.component_for_entity (e, Position)
            except NonexistentComponentTypeForEntity:
                self.log.warn ("%s has a Movement but no Position component, \
                        cannot move it.", e)
                continue 

            pos.x += vel.dx * dt
            pos.y += vel.dy * dt

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
            destroy_entity (self.entity_manager,e)
