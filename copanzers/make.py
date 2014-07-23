# Copyright (C) 2014 Marvin Poul <ponder@creshal.de>
import pygame, os, logging, collections, json
from copy import deepcopy
from ecs.exceptions import NonexistentComponentTypeForEntity

import copanzers.components
from copanzers.scripts import RWInterface
from copanzers.components import *
from copanzers.util import make_color_surface

log = logging.getLogger (__name__)

_presets = {}
def update_presets (presets):
    for preset in os.listdir ("presets/entities"):
        with open ("presets/entities/" + preset) as pref:
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
        presets [name] = compargs

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
                del presets [name]
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
                    del presets [name]
                    break

                while n >= len (vargs):
                    vargs.append ([])
                vargs [n].append ( (comp, key) )
            else:
                continue

            break

def make (eman, game, name, *vargs, pos = (0, 0)):
    try:
        proto = _presets [name].copy ()
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

    e = eman.create_entity ()
    eman.add_component (e, Position (*pos))

    for c, args in proto.items ():
        # we special case some components here becaues it would be to
        # cumbersome otherwise, we also have to check whether we might have not
        # gotten the class itself but an alternative constructor
        if   c in (Script, getattr (Script, c.__name__, None)):
            args ["script_args"] = RWInterface (e, eman), game
        elif c == Mountable:
            args ["root"] = vargs [0]
        elif c == Mount:
            m = Mount (args ['points'])
            if len (m.mounts) != len (args ['mounts']):
                log.error ("Preset '%s' provides too much or too few mounted \
entities for the specified mount points. If some were left empty on purpose, \
set the respective elements in 'mounts' to null.", name)
                eman.remove_entity (e)
                return

            for i, mounted in enumerate (args ['mounts']):
                if mounted != None:
                    m.mounts [i] = make (eman, game, mounted, e)
            eman.add_component (e, m)
            continue

        eman.add_component (e, c (**args))

    return e

## defaults for components
def healthbar (size):
    """
    return a default health bar component
    size -- 2 tuple of int, pertaining to the entity the health bar
            is created for and _not_ the dimension of the resulting health bar
    """
    return HealthBar ( (0, -0.8 * size [1]), (0.7 * size [0], 6) )

update_presets (_presets)
