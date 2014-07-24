# Copyright (C) 2014 Marvin Poul <ponder@creshal.de>
import pygame, os, logging, json
from functools import partial
from copy import deepcopy
from ecs.exceptions import NonexistentComponentTypeForEntity

import copanzers.components
from copanzers.scripts import RWInterface
from copanzers.components import *

log = logging.getLogger (__name__)

class Maker:

    __slots__ = "game", "eman"
    presets = {}

    def __init__ (self, eman, game, entity_path = None):
        """
        entity_path -- str, directory where to find the entity presets
        game -- GameInfo, needed for the script routines, see bin/tanks
        """
        self.eman = eman
        self.game = game
        if entity_path:
            self.update_presets (entity_path)

    def update_presets (self, entity_path):
        for preset in os.listdir (entity_path):
            with open (os.path.join (entity_path, preset)) as pref:
                try:
                    cp_pre = json.load (pref)
                except ValueError:
                    log.error ("Failed to read in preset '%s', is no valid json.", preset)
                    continue

            try:
                name = cp_pre ['Misc']['name']
            except KeyError:
                log.error ("Failed to read in preset '%s', didn't specify a name.",
                        preset)
                continue

            vargs = []
            compargs = {"vargs": vargs}
            self.presets [name] = compargs

            for s in cp_pre:
                if s == 'Misc': continue
                try:
                    if "." in s:
                        # preset has a section of the form Component.factory, so we
                        # have to get the respective function instead of just the class
                        c, fac, *_ = s.split (".")
                        comp = getattr (getattr (copanzers.components, c), fac)
                    else:
                        comp = getattr (copanzers.components, s)
                except AttributeError as err:
                    log.error ("Failed to read in preset '%s', specified component \
or factory '%s' doesn't exist.", preset, err.args [0].split ("'") [-2])
                    del self.presets [name]
                    break

                compargs [comp] = {}

                for key, val in cp_pre [s].items ():
                    if not isinstance (val, str) or val [0] != '$':
                        compargs [comp][key] = val
                        continue

                    try:
                        n = int (val [1:])
                    except ValueError:
                        log.error ("Failed to read in preset '%s', '%s' is not a \
valid argument number.", preset, val [1:])
                        del self.presets [name]
                        break

                    while n >= len (vargs):
                        vargs.append ([])
                    vargs [n].append ( (comp, key) )
                else:
                    continue

                break

    def make (self, name, *vargs, pos = (0, 0)):
        try:
            proto = self.presets [name].copy ()
        except KeyError:
            raise ValueError ("Preset {} doesn't exist.".format (name)) from None

        for i, va in enumerate (proto ["vargs"]):
            try:
                for c, o in va:
                    proto [c][o] = vargs [i]
            except IndexError:
                log.error ("Preset '%s' specified more arguments than were \
provided.", name)
                return
        del proto ["vargs"]

        e = self.eman.create_entity ()
        self.eman.add_component (e, Position (*pos))
        needs_hp_bar = False

        for c, args in proto.items ():
            # we special case some components here becaues it would be to
            # cumbersome otherwise, we also have to check whether we might have not
            # gotten the class itself but an alternative constructor
            if   c in (Script, getattr (Script, c.__name__, None)):
                args ["script_args"] = RWInterface (e, self.eman), self.game
            elif c == Mountable:
                args ["root"] = vargs [0]
            elif c == HealthBar:
                if "size" not in args or "center" not in args:
                    # we defer here, because we don't know whether the hitbox was
                    # already added
                    needs_hp_bar = True
                    continue
            elif c == Mount:
                m = Mount (args ['points'])
                if len (m.mounts) != len (args ['mounts']):
                    log.error ("Preset '%s' provides too much or too few mounted \
entities for the specified mount points. If some were left empty on purpose, set \
the respective elements in 'mounts' to null.", name)
                    self.eman.remove_entity (e)
                    return

                for i, mounted in enumerate (args ['mounts']):
                    if mounted != None:
                        m.mounts [i] = self.make (mounted, e)
                self.eman.add_component (e, m)
                continue

            self.eman.add_component (e, c (**args))

        if needs_hp_bar:
            hp   = self.eman.component_for_entity (e, Health).max_hp
            size = self.eman.component_for_entity (e, Hitbox).size
            self.eman.add_component (e,
                HealthBar ( (0, -0.8 * size [1]), (hp / 2, 6) )
            )
        return e

    def __getitem__ (self, name):
        return partial (self.make, name)
