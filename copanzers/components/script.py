from ecs.models import Component

from copanzers.util import Vec2d

class Script (Component):

    @classmethod
    def file (cls, path, script_args):
        """
        creates a new script component from a file
        path -- to script file
        script_args -- tuple, arguments to the scripts routines, see copanzers.make
        """
        return cls (load_routine (path) (*script_args))

    def __init__ (self, routine):
        """
        routine -- python generator
        """
        self.routine   = routine
        self.predicate = lambda: True

def load_routine (script):

    with open (script) as f:
        l = {"Vec2d": Vec2d}
        routine = exec (f.read (), l)
        return l ["main"]
