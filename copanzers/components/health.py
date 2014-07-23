# Copyright (C) 2014 Marvin Poul <ponder@creshal.de>
from ecs.models import Component

class Health (Component):
    __slots__ = "hp", "max_hp"
    def __init__ (self, max_hp):
        """
        max_hp -- int, health points this entity can have at most
        """
        self.hp = max_hp
        self.max_hp = max_hp
