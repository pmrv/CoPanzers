from ecs.models import Component

class Script (Component):

    def __init__ (self, routine, interface):
        """
        routine   -- generator function taking one argument
        interface -- some object instance used to pass values
                     between the routine and the script system
        """
        self.interface = interface
        self.routine   = routine (interface)
        self.predicate = lambda: True
        
