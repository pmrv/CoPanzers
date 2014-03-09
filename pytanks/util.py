import pygame

def make_color_surface (size, color, colorkey = (255, 255, 255)):
    surface = pygame.Surface (size)
    surface.set_colorkey (colorkey)
    surface.fill (color)
    pygame.draw.rect (surface, (0, 0, 0), surface.get_rect (), 1)
    return surface

def Rect (center, size):
    return pygame.Rect (center [0] - size [0] / 2, center [1] - size [1] / 2, *size)

def components_for_entity (eman, entity, components):
    """
    Return a tuple of component instances for a given entity.
    Will not catch any NonexistentComponentTypeForEntity Errors.
    """

    return tuple (eman.component_for_entity (entity, c) for c in components)
