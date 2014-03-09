from ecs.models import System
from ecs.exceptions import NonexistentComponentTypeForEntity

from pytanks.components import *
from pytanks.util import components_for_entity
from pytanks import make

class ExampleTurretSystem (System):

    def update (self, dt):

        eman = self.entity_manager
        for e, turret in eman.pairs_for_type (ExampleTurret):

            if turret.target == None:
                # shot at the first barrier we find
                for c, tags in eman.pairs_for_type (Tags):
                    if tags ["Class"] == "Barrier":
                        turret.target = c
                        break

            weapon = eman.component_for_entity (e, Weapon)
            if weapon.till_reloaded:
                continue

            target_pos = eman.component_for_entity (turret.target, Position)
            turret_pos = eman.component_for_entity (e, Position)
            turret_mov = eman.component_for_entity (e, Movement)

            diff = target_pos [0] - turret_pos [0], target_pos [1] - turret_pos [1]

            turret_mov.rotation = math.cos (
                diff [0] / math.sqrt (diff [0] ** 2 + diff [1] ** 2)
            )
            
            weapon.triggered = True


class RenderSystem (System):

    def __init__ (self, surface, *args, **kw):
        """
        surface -- pygame.Surface, surface to draw to
        """
        self.surface = surface
        System.__init__ (self, *args, **kw)

    def update (self, _):

        surf = self.surface
        surf.fill ( (255, 255, 255) )

        eman = self.entity_manager
        for e, renderable in eman.pairs_for_type (Renderable):

            pos = eman.component_for_entity (e, Position)
            text_rect = renderable.texture.get_rect ()
            text_rect.center = pos.x, pos.y
            surf.blit (renderable.texture, text_rect)


class HealthRenderSystem (RenderSystem):

    def update (self, _):

        eman = self.entity_manager

        for e, bar in eman.pairs_for_type (HealthBar):
            try: 
                health = eman.component_for_entity (e, Health)
                pos    = eman.component_for_entity (e, Position)
            except NonexistentComponentTypeForEntity as err:
                if   err.component_type == Health:
                    print ("Weird, this entity has a HealthBar but \
                            no Health: {}".format (e))
                elif err.component_type == Position:
                    print ("Weird, this entity has no Position: {}".format (e))
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


class HealthSystem (System):

    def update (self, _):

        destroyed = []
        for e, health in self.entity_manager.pairs_for_type (Health):
            if health.hp <= 0:
                print ("Entity {} was destroyed.".format (e))
                destroyed.append (e)

        for e in destroyed:
            self.entity_manager.remove_entity (e)


class MountSystem (System):

    def update (self, dt):

        eman = self.entity_manager
        for e, m in eman.pairs_for_type (Mount):

            try: 
                pos = eman.compononent_for_enitity (e, Position)
            except NonexistentComponentTypeForEntity:
                print ("Weird, entity {} has no Position.".format (e))
                continue

            for i in range (m.amount):
                im = m.mounts [i]
                if im is None: continue

                try: 
                    ipos = eman.compononent_for_enitity (im, Position)
                    ipos.x += pos.x + m.points [i] [0]
                    ipos.y += pos.y + m.points [i] [1]

                except NonexistentComponentTypeForEntity:
                    print ("Weird, entity {} has no Position.".format (im))
                    continue


class MovementSystem (System):

    def update (self, dt):
        for e, vel in self.entity_manager.pairs_for_type (Movement):
            try:
                pos = self.entity_manager.component_for_entity (e, Position)
            except NonexistentComponentTypeForEntity:
                print ("No position component found for moving.")
                continue # shouldn't be happening, but just to be sure

            pos.x += vel.dx
            pos.y += vel.dy

            try:
                hitbox = self.entity_manager.component_for_entity (e, Hitbox)
                hitbox.center = pos.x, pos.y
            except NonexistentComponentTypeForEntity:
                print ("Entity has no hitbox, don't try to move it.")
                continue


class CollisionSystem (System):

    def update (self, dt):
        # for now just do collision detection for Projectiles

        eman = self.entity_manager
        destroyed = [] # projectiles which hit a target
        for e, proj in eman.pairs_for_type (Projectile):
            
            try:
                ehit, epos = components_for_entity (eman, e, (Hitbox, Position))
                ehit.center = epos.x, epos.y
            except NonexistentComponentTypeForEntity:
                print ("Entity {} has either no Hitbox or no Position \
                        but Projectile, can't do collision detection  \
                        with it.".format (e))
                continue

            for o, ohit in eman.pairs_for_type (Hitbox):
                if e == o or o in proj.ignore: continue

                try:
                    opos = eman.component_for_entity (o, Position)
                except:
                    print ("Entity {} has no Position but Hitbox, \
                            can't to collision detection with it.".format (o))
                    continue

                ohit.center = opos.x, opos.y

                # TODO: we should use pygame.Rect.collidelistall for this one
                if not ehit.colliderect (ohit):
                    continue

                destroyed.append (e)

                try:
                    ohealth = eman.component_for_entity (o, Health)
                    ohealth.hp -= proj.damage
                except NonexistentComponentTypeForEntity:
                    print ("Entity {} was hit but has no Health.".format (o))
                    continue

        for e in destroyed:
            eman.remove_entity (e)


class WeaponSystem (System):

    def update (self, dt):

        eman = self.entity_manager
        for e, weapon in eman.pairs_for_type (Weapon):

            if weapon.triggered:
                weapon.triggered = False
                weapon.till_reloaded = weapon.reload_time

                mov = eman.component_for_entity (e, Movement)
                pos = eman.component_for_entity (e, Position)

                rot = mov.rotation
                make.bullet (eman, weapon, pos, rot)
            
            weapon.till_reloaded = max (0, weapon.till_reloaded - dt)


