from ecs.models import System

from pytanks.components.renderable import Renderable
from pytanks.components.position   import Position

class RenderSystem (System):

    def __init__ (self, surface, *args, **kw):
        """
        surface -- pygame.Surface, surface to draw to
        """
        self.surface = surface
        System.__init__ (*args, **kw)

    def update (self, _):

        surf = self.surface
        surf.fill ( (255, 255, 255) )

        eman = self.entity_manager
        for e, renderable in eman.pairs_for_type (Renderable):

            pos = eman.component_for_entity (e, Position)
            surf.blit (renderable.texture, (pos.x, pos.y, 0, 0))
