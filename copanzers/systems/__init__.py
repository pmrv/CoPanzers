# Copyright (C) 2014 Marvin Poul <ponder@creshal.de>
import logging
from ecs.models import System
from ecs.exceptions import NonexistentComponentTypeForEntity

from ..components import Destroyed, Mount

class LogSystem (System):

    def __init__ (self):
        self.log = logging.getLogger (__name__ + "." + type (self).__name__)
        super ().__init__ ()


def components_for_entity (eman, entity, components):
    """
    Return a tuple of component instances for a given entity.
    Will not catch any NonexistentComponentTypeForEntity Errors.
    """

    return tuple (eman.component_for_entity (entity, c) for c in components)

def destroy_entity (eman, e):
    """
    remove an entity and all mounted entities from the entity manager
    """
    try:
        for m in eman.component_for_entity (e, Mount).mounts:
            destroy_entity (eman, m)
    except NonexistentComponentTypeForEntity:
        pass
    finally:
        eman.remove_entity (e)
        eman.add_component (e, Destroyed ())

from .movementsystem     import MovementSystem
from .healthsystem       import HealthSystem
from .rendersystem       import RenderSystem
from .healthrendersystem import HealthRenderSystem
from .mountsystem        import MountSystem
from .weaponsystem       import WeaponSystem
from .collisionsystem    import CollisionSystem
from .scriptsystem       import ScriptSystem
from .visionsystem       import VisionSystem
