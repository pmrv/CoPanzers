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

from .movementsystem     import MovementSystem
from .healthsystem       import HealthSystem
from .rendersystem       import RenderSystem
from .healthrendersystem import HealthRenderSystem
from .mountsystem        import MountSystem
from .weaponsystem       import WeaponSystem
from .collisionsystem    import CollisionSystem
from .scriptsystem       import ScriptSystem
from .visionsystem       import VisionSystem
from .killsystem         import KillSystem
