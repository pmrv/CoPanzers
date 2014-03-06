from pytanks.components.renderable import Renderable
from pytanks.components.position   import Position, Movement
from pytanks.components.health     import Hitbox, Health

from pytanks.util import make_color_surface, Rect

def bullet (eman, weapon, pos, rot):
    # TODO: squeeze in the damage somewhere
    """
    eman   -- ecs.managers.EntityManager, where to add the bullet to
    weapon -- pytanks.components.weapon.Weapon, weapon component where we get 
              our init data from
    pos    -- 2 tuple of int, position of the new bullet
    rot    -- float, in which direction the bullet should be fired
    """

    e = eman.create_entity ()
    eman.add_component (e, Position (*pos))
    eman.add_component (e, Movement (rot, weapon.bullet_speed))
    eman.add_component (e, Hitbox (weapon.bullet_hitbox))
    eman.add_component (e, Health (weapon.bullet_hp))
    eman.add_component (e, Renderable (weapon.bullet_texture))

def barrier (eman, color, size, pos):
    """
    eman  -- ecs.managers.EntityManager, where to add the bullet to
    color -- 3 tuple of int, the color the barrier should have
    size  -- 3 tuple of int, how big the barrier should be
    pos   -- 2 tuple of int, position of the new bullet
    """

    e = eman.create_entity ()
    eman.add_component (e, Position (*pos))
    eman.add_component (e, Hitbox (Rect (pos, size)))
    eman.add_component (e, Renderable (make_color_surface (size, color)))
