from pytanks.systems import LogSystem
from pytanks.components import Script

class ScriptSystem (LogSystem):

    def update (self, dt):

        eman = self.entity_manager
        finished = []
        for e, s in eman.pairs_for_type (Script):

            if s.predicate ():
                try:
                    self.log.debug ("Running script routine for %s.", e)
                    s.predicate = next (s.routine)
                except StopIteration: # routine finished
                    self.log.info ("Script routine for %s finished.", e)
                    finished.append (e)
                except Exception as err:
                    self.log.warning ("Script routine for %s failed with \"%s\".",
                                      e, err)
                    finished.append (e)

        for e in finished:
            eman.remove_component (e, Script)
