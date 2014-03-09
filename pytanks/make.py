from pytanks.components import *
from pytanks.util import make_color_surface

## defaults for components
def healthbar (pos, size):
    """
    return a default health bar component
    pos, size -- 2 tuple of int, pertaining to the entity the health bar
                 is created and _not_ the dimension of the resulting health bar
    """
    return HealthBar ( (0, -0.8 * size [1]), (0.7 * size [0], 6) )


## defaults for entities
def bullet (eman, weapon, pos, rot):
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
    eman.add_component (e, Projectile (weapon.bullet_damage, tuple ()))

def barrier (eman, hp, color, size, pos):
    """
    eman  -- ecs.managers.EntityManager, where to add the bullet to
    hp    -- int, maximum hitpoints of the barrier
    color -- 3 tuple of int, the color the barrier should have
    size  -- 2 tuple of int, how big the barrier should be
    pos   -- 2 tuple of int, position of the new bullet
    """

    e = eman.create_entity ()
    eman.add_component (e, Position (*pos))
    eman.add_component (e, Hitbox (size))
    eman.add_component (e, Health (hp))
    eman.add_component (e, healthbar (pos, size))
    eman.add_component (e, Renderable (make_color_surface (size, color)))
