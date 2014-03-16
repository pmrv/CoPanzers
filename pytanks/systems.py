import logging

from ecs.models import System
from ecs.exceptions import NonexistentComponentTypeForEntity

from pytanks.components import *
from pytanks.util import components_for_entity
from pytanks import make

class LogSystem (System):

    def __init__ (self):
        self.log = logging.getLogger (__name__ + type (self).__name__)
        System.__init__ (self)

class ExampleTurretSystem (LogSystem):

    def update (self, dt):

        eman = self.entity_manager
        for e, turret in eman.pairs_for_type (ExampleTurret):

            if turret.target == None:
                # shot at the first barrier we find
                for c, tags in eman.pairs_for_type (Tags):
                    if tags ["Class"] == "Barrier":
                        turret.target = c
                        self.log.info ("Turret %s found new target %s.", e, c)
                        break
                else:
                    continue # can't find new targets

            try:
                target_pos = eman.component_for_entity (turret.target, Position)
            except NonexistentComponentTypeForEntity:
                # target has no position, assume it no longer exists
                self.log.info ("Turret %s lost target %s.", e, turret.target) 
                turret.target = None
                continue

            mount  = eman.component_for_entity (e, Mount)
            weapon = eman.component_for_entity (mount.mounts [0], Weapon) 
            if weapon.till_reloaded > 0:
                continue

            turret_pos = eman.component_for_entity (e, Position)
            weapon_mov = eman.component_for_entity (mount.mounts [0], Movement)

            diff = target_pos.x - turret_pos.x, target_pos.y - turret_pos.y

            weapon_mov.rotation = math.acos (
                diff [0] / math.sqrt (diff [0] ** 2 + diff [1] ** 2)
            ) 
            
            weapon.triggered = True


class RenderSystem (LogSystem):

    def __init__ (self, surface, *args, **kw):
        """
        surface -- pygame.Surface, surface to draw to
        """
        self.surface = surface
        LogSystem.__init__ (self, *args, **kw)

    def update (self, _):

        surf = self.surface
        surf.fill ( (255, 255, 255) )

        eman = self.entity_manager
        renders = list (eman.pairs_for_type (Renderable))
        renders.sort (key = lambda x: x [1].layer)
        for e, renderable in renders:

            pos = eman.component_for_entity (e, Position)
            try:
                rot = eman.component_for_entity (e, Movement).rotation
                if rot != 0:
                    texture = pygame.transform.rotate (
                        renderable.texture, math.degrees (rot)
                    )
                else:
                    texture = renderable.texture
            except NonexistentComponentTypeForEntity:
                texture = renderable.texture

            text_rect = texture.get_rect ()
            text_rect.center = pos.x, pos.y
            surf.blit (texture, text_rect)


class HealthRenderSystem (RenderSystem):

    def update (self, _):

        eman = self.entity_manager

        for e, bar in eman.pairs_for_type (HealthBar):
            try: 
                health = eman.component_for_entity (e, Health)
                pos    = eman.component_for_entity (e, Position)
            except NonexistentComponentTypeForEntity as err:
                if   err.component_type == Health:
                    self.log.warn ("%s has a HealthBar but no Health component.", e)
                elif err.component_type == Position:
                    self.log.warn ("%s has no Position component, can't draw its \
                            health bar.", e)
                continue 

            # TODO: make this cooler

            border = pygame.Rect ( (pos.x + bar.topleft [0], pos.y + bar.topleft [1],
                                    bar.size [0], bar.size [1]) )

            pygame.draw.rect (self.surface, (0, 0, 0), border, 1)

            remaining = health.hp / health.max_hp * (bar.width - 2)
            # super efficient, I know but I'm too lazy to type it out…
            topleft_green = list (map (lambda x: x + 1, bar.topleft))
            size_green    = remaining, bar.height - 2
            topleft_green [0] += pos.x
            topleft_green [1] += pos.y

            pygame.draw.rect (self.surface, (0, 255, 0), (topleft_green, size_green))

            if health.hp == health.max_hp:
                continue

            topleft_red = [topleft_green [0] + remaining, topleft_green [1]]
            size_red    = (bar.width - 2) - remaining, bar.height - 2

            pygame.draw.rect (self.surface, (255, 0, 0), (topleft_red, size_red))


class HealthSystem (LogSystem):

    def update (self, _):

        destroyed = []
        for e, health in self.entity_manager.pairs_for_type (Health):
            if health.hp <= 0:
                self.log.info ("%s was destroyed.", e)
                destroyed.append (e)

        for e in destroyed:
            self.entity_manager.remove_entity (e)


class MountSystem (LogSystem):

    def update (self, dt):

        eman = self.entity_manager
        for e, m in eman.pairs_for_type (Mount):

            try: 
                pos = eman.component_for_entity (e, Position)
            except NonexistentComponentTypeForEntity:
                self.log.warn ("%s has a Mount but no Position component, \
                        cannot adjust the position of the mounted entities.", e)
                continue

            for i in range (m.amount):
                im = m.mounts [i]
                if im is None: continue

                try: 
                    ipos = eman.component_for_entity (im, Position)
                    ipos.x = pos.x + m.points [i] [0]
                    ipos.y = pos.y + m.points [i] [1]

                except NonexistentComponentTypeForEntity:
                    self.log.warn ("%s is mounted on %s, but has no Position \
                            component, cannot adjust it.")
                    continue


class MovementSystem (LogSystem):

    def __init__ (self, width, height):
        """
        width, height -- int, specify size of the visible screen
        """
        self.screen = pygame.Rect ( (0, 0, width, height) )
        LogSystem.__init__ (self)

    def update (self, dt):
        remove = []
        for e, vel in self.entity_manager.pairs_for_type (Movement):
            try:
                pos = self.entity_manager.component_for_entity (e, Position)
            except NonexistentComponentTypeForEntity:
                self.log.warn ("%s has a Movement but no Position component, \
                        cannot move it.", e)
                continue 

            pos.x += vel.dx
            pos.y += vel.dy

            if not self.screen.collidepoint (pos):
                self.log.debug ("%s left the visible screen at %s, removing it.",
                        e, pos)
                remove.append (e) # remove all entities which disappear from the game screen

            try:
                hitbox = self.entity_manager.component_for_entity (e, Hitbox)
                hitbox.center = pos.x, pos.y
            except NonexistentComponentTypeForEntity:
                continue

        for e in remove:
            self.entity_manager.remove_entity (e)


class CollisionSystem (LogSystem):

    def update (self, dt):
        # for now just do collision detection for Projectiles

        eman = self.entity_manager
        destroyed = [] # projectiles which hit a target
        for e, proj in eman.pairs_for_type (Projectile):
            
            try:
                ehit, epos = components_for_entity (eman, e, (Hitbox, Position))
                ehit.center = epos.x, epos.y
            except NonexistentComponentTypeForEntity:
                self.log.warn ("Skipping projectile %s for collision detection as \
                        it has either no Position or Hitbox component.", e)
                continue

            for o, ohit in eman.pairs_for_type (Hitbox):
                if e == o or o in proj.ignore: continue

                try:
                    opos = eman.component_for_entity (o, Position)
                except:
                    self.log.debug ("Skipping %s for collision dectection as it \
                            has no Hitbox component.", o)
                    continue

                ohit.center = opos.x, opos.y

                # TODO: we should use pygame.Rect.collidelistall for this one
                if ehit.colliderect (ohit):

                    self.log.debug ("Projectile %s hit %s.", e, o)
                    destroyed.append (e)

                    try:
                        ohealth = eman.component_for_entity (o, Health)
                        ohealth.hp -= proj.damage
                    except NonexistentComponentTypeForEntity:
                        self.log.info ("%s was hit but has no Health component, \
                                so it took no damage.", o)

                    break

        for e in destroyed:
            eman.remove_entity (e)


class WeaponSystem (LogSystem):

    def update (self, dt):

        eman = self.entity_manager
        for e, weapon in eman.pairs_for_type (Weapon):

            if weapon.triggered:
                weapon.triggered = False
                weapon.till_reloaded = weapon.reload_time

                rot = eman.component_for_entity (e, Movement).rotation
                pos = eman.component_for_entity (e, Position)
                ign = (eman.component_for_entity (e, Mountable).root,)

                self.log.debug ("Weapon %s fired bullet from %s with angle %i°.",
                        e, pos, math.degrees (-rot))
                make.bullet (eman, weapon.bullet_properties, pos, -rot, ign)
            
            weapon.till_reloaded = max (0, weapon.till_reloaded - dt)


