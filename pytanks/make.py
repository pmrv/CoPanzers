# Copyright (C) 2014 Marvin Poul <ponder@creshal.de>
import pygame
from ecs.exceptions import NonexistentComponentTypeForEntity

from pytanks.scripts import RWInterface
from pytanks.components import *
from pytanks.util import make_color_surface

## defaults for components
def healthbar (pos, size):
    """
    return a default health bar component
    pos, size -- 2 tuple of int, pertaining to the entity the health bar
                 is created for and _not_ the dimension of the resulting health bar
    """
    return HealthBar ( (0, -0.8 * size [1]), (0.7 * size [0], 6) )


## defaults for entities
def bullet (eman, properties, pos, rot, ignore = tuple ()):
    """
    eman       -- ecs.managers.EntityManager, where to add the bullet to
    properties -- 5 tuple of  
                    0: int, damage,
                    1: int, speed,
                    2: int, hit points,
                    3: pygame.Surface, texture
                    4: 2 tuple of int, hitbox
    pos        -- 2 tuple of int, position of the new bullet
    rot        -- float, in which direction the bullet should be fired
    """

    e = eman.create_entity ()
    eman.add_component (e, Position (*pos))
    eman.add_component (e, Projectile (properties [0], ignore))
    eman.add_component (e, Movement (rot, properties [1]))
    eman.add_component (e, Health (properties [2]))
    eman.add_component (e, Renderable (properties [3], 2))
    eman.add_component (e, Hitbox (properties [4]))
    eman.add_component (e, Tags (Class = "Bullet"))

    return e

def barrier (eman, hp, texture, size, pos):
    """
    eman    -- ecs.managers.EntityManager, where to add the bullet to
    hp      -- int, maximum hitpoints of the barrier
    texture -- pygame.Surface
    size    -- 2 tuple of int, how big the barrier should be
    pos     -- 2 tuple of int, position of the new bullet
    """

    e = eman.create_entity ()
    eman.add_component (e, Position (*pos))
    eman.add_component (e, Hitbox (size))
    eman.add_component (e, Health (hp))
    eman.add_component (e, healthbar (pos, size))
    eman.add_component (e, Renderable (texture))
    eman.add_component (e, Tags (Class = "Barrier"))

    return e

def example_barrier (eman, hp, size, pos):
    return barrier (eman, hp, make_color_surface (size, (0, 155, 0)), size, pos)

def weapon (eman, texture, reload_time, bullet_properties, root, slot):
    """
    Create an entity with Weapon/Position/Renderable/Mountable component.

    eman        -- ecs.managers.EntityManager, where to add the bullet to
    texture     -- pygame.Surface, what the weapon looks like
    reload_time -- int, in seconds
    root        -- ecs.models.Entity, on which other entity this weapon is
                   mounted on, usually a turret or tanks or whatever
    slot        -- int, into which mountpoint of root this weapon should be put into
    """

    # Not catching the NonexistentComponentTypeForEntity exception here 
    # because we cannot do anything reasonable with it here. 
    # If we catch it and fail silently the caller can assume the weapon
    # was successfully created, if we catch it and return some error indication
    # they will have to check for that, in which case it is cleaner for them
    # to just catch the exception themselves.
    m = eman.component_for_entity (root, Mount)
    if slot >= m.amount or m.mounts [slot] != None:
        raise ValueError ("Mount point {} already taken or not existent.".format (slot))

    e = eman.create_entity ()
    m.mounts [slot] = e

    eman.add_component (e, Position (0, 0)) # Position is later set by the MountSystem
    eman.add_component (e, Movement (0, 0, 0))
    eman.add_component (e, Renderable (texture, 1))
    eman.add_component (e, Mountable (root))
    eman.add_component (e, Weapon (reload_time, bullet_properties))
    eman.add_component (e, Tags (Class = "Weapon"))

    return e

def example_weapon (eman, root, slot):
    """
    Creates a default turret with some placeholder values for the bullet and
    a blue triangle as texture.
    """

    h, w = 20, 20
    s = pygame.Surface ((h, w))
    s.set_colorkey ((255, 255, 255))
    s.fill ((255, 255, 255))
    pygame.draw.polygon (s, (150, 0, 0), ((w/2, 0), (w, h/2), (w/2, h)))
    pygame.draw.polygon (s, (  0, 0, 0), ((w/2, 0), (w, h/2), (w/2, h)), 1)

    return weapon (eman, s, .8, (5, 80, 2, make_color_surface ( (5, 5), (255, 255, 0) ), (5, 5)), root, slot)

def scripted_turret (eman, routine, pos):

    h, w = 30, 30
    s = pygame.Surface ((h, w))
    s.set_colorkey ((255, 255, 255))
    s.fill ((255, 255, 255))
    pygame.draw.polygon (s, (0, 155, 0), ((0, h/2), (w/2, 0), (w, h/2), (w/2, h)))
    pygame.draw.polygon (s, (0, 0, 0), ((0, h/2), (w/2, 0), (w, h/2), (w/2, h)), 1)

    e = barrier (eman, 80, s, (h, w), pos)

    eman.add_component (e, Mount (((0,0),)))
    example_weapon (eman, e, 0)
    eman.add_component (e, 
            Script (routine (RWInterface (e, eman), eman)))
    eman.add_component (e, Tags (Class = "Turret"))

    return e

def scripted_tank (eman, routine, pos):

    e = example_barrier (eman, 100, (60, 20), pos)
    pos = eman.database [Position] [e]
    mov = Movement (0, 0, 70)
    tag = eman.database [Tags] [e]
    tag ["Class"] = "Tank"

    eman.add_component (e, mov)
    eman.add_component (e, Mount ( ((0, 0),) ))
    example_weapon (eman, e, 0)
    eman.add_component (e, 
        Script (routine (RWInterface (e, eman), eman))
    )
