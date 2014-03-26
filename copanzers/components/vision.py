# Copyright (C) 2014 Marvin Poul <ponder@creshal.de>

from ecs.models import Component

class Vision (Component):

    def __init__ (self, kind, reach):
        """
        kind  -- str, one of ["plain", "radar"], defines how much detail the
                      vision reveals, e.g. "plain" gives more details than
                      "radar"
        reach -- int, in pixel, how far the vision can see
        """

        self.kind  = kind
        self.reach = reach
        # list of entities visible wrapped in interfaces
        self.visible = [] 
