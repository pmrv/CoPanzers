# Copyright (C) 2014 Marvin Poul <ponder@creshal.de>

from ecs.models import Component

# I'm not really content with this, but it seems the easiest solution
class Destroyed (Component):
    """
    We just use this one to tag dead entities
    """
    pass 
