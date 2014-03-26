from ecs.models import Component

class Script (Component):

    def __init__ (self, routine):
        """
        routine -- python generator
        """
        self.routine   = routine
        self.predicate = lambda: True
        
