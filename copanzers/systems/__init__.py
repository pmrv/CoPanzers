# Copyright (C) 2014 Marvin Poul <ponder@creshal.de>
import logging
from ecs.models import System

class LogSystem (System):

    def __init__ (self):
        self.log = logging.getLogger (__name__ + "." + type (self).__name__)
        super ().__init__ ()

from .movementsystem      import MovementSystem
from .healthsystem        import HealthSystem
from .rendersystem        import RenderSystem
from .healthrendersystem  import HealthRenderSystem
from .mountsystem         import MountSystem
from .weaponsystem        import WeaponSystem
from .collisionsystem     import CollisionSystem
from .scriptsystem        import ScriptSystem
