from ecs.models import System
from ecs.exceptions import NonexistentComponentTypeForEntity

from pytanks.components.movement import Position

class MountSystem (System):

    def update (self, dt):

        eman = self.entity_manager
        for e, m in eman.pairs_for_type (Mount):

            try: 
                pos = eman.compononent_for_enitity (e, Position)
            except NonexistentComponentTypeForEntity:
                print ("Weird, entity {} has no Position.".format (e))
                continue

            for i in range (m.amount):
                im = m.mounts [i]
                if im is None: continue

                try: 
                    ipos = eman.compononent_for_enitity (im, Position)
                    ipos.x += pos.x + m.points [i] [0]
                    ipos.y += pos.y + m.points [i] [1]

                except NonexistentComponentTypeForEntity:
                    print ("Weird, entity {} has no Position.".format (im))
                    continue
