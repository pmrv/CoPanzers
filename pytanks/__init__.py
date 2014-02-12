import pygame, math

from .util import Destroyed, Rect
import pytanks.target as target

class GameObject:

    def __init__ (self, texture, position, hitbox):
        """
        texture   -- pygame Surface or pygame Color
        position  -- 2 tuple of int, initial position on the screen
        hitbox    -- 2 tuple of int, size of the hitbox of the object
        hitpoints -- int
        """

        self.hitbox = Rect ( position, hitbox )

        if isinstance (texture, pygame.Surface):
            self.texture = texture
        elif isinstance (texture, (pygame.Color, tuple)):
            self.texture = pygame.Surface (self.hitbox.size)
            self.texture.fill (texture)
            pygame.draw.rect (self.texture, (0, 0, 0), self.texture.get_rect (), 1)
        else:
            raise TypeError ("Parameter $texture must be a pygame Surface or Color.")
        
        self.position  = list (position)

    def step (self, other_game_objects, relative_time):
        """
        other_game_objects -- list, well, duh, a list of all other 
                                    game objects currently in the game
        relative_time      -- float, modifier to influence to overall 
                                     pace of the game and to accomodate 
                                     between different fps
        """
        self.hitbox.center = self.position

    def draw (self, surface):
        surface.blit (self.texture, (self.position [0] - self.texture.get_width () / 2,
                                    self.position [1] - self.texture.get_height () / 2))


class Barrier (GameObject):

    def __init__ (self, hp, *args, **kw):
        GameObject.__init__ (self, *args, **kw)
        target.init (self, hp)

    hit = target.hit

    def step (self, o, t):
        target.step (self, o, t)
        GameObject.step (self, o, t)

    def draw (self, surface):
        GameObject.draw (self, surface)
        target.draw (self, surface)

class Bullet (GameObject):

    def __init__ (self, speed, direction, damage, *args, **kw):
        """
        speed     -- int, how fast is the bullet moving
        direction -- float, in radians
        damage    -- int
        """

        self.damage    = damage
        self.dx = math.cos (direction) * speed
        self.dy = math.sin (direction) * speed

        GameObject.__init__ (self, *args, **kw)

    def step (self, others, dt):

        for o in others:
            if self.hitbox.colliderect (o.hitbox) and hasattr (o, "hit"):
                o.hit (self.damage, self)
                raise Destroyed ("Bullet hit something.")
        self.position [0] += self.dx * dt
        self.position [1] += self.dy * dt

        GameObject.step (self, others, dt)

