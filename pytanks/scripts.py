import math

class ScriptInterface:
    """
    provides the script routines with getter and setters
    to component values of the entity they control
    """

    def __init__ (self, position, movement):
        """
        position -- pytanks.components.Position instance,
                    must be the same one as added to the entity
                    manager
        movement -- pytanks.components.Movement instance,
                    same as above
        """
        self.max_speed  = 5 # hardcode for now just to get us started
        self.__position = position
        self.__movement = movement
        self.__throttle = 0

    @property
    def position (self):
        """
        read-only value for the position of the entity
        """
        return self.__position 

    @property
    def rotation (self):
        return self.__movement.rotation

    @rotation.setter
    def rotation (self, val):
        self.__movement.rotation = val

    @property
    def throttle (self):
        """
        speed of the entity in percent, getter clamps 
        value between 0 and 1
        """
        return self.__throttle

    @throttle.setter
    def throttle (self, val):
        self.__throttle = min (1, max (0, val))
        self.__movement.speed = val * self.max_speed

def example_routine (tank):
    """
    generator function that yields predicates that work on $tank and
    return True if some condition is met, the script system then continues
    execution of the routine
    """

    x, y = tank.position

    tank.throttle = 1
    tank.rotation = - math.pi / 2
    yield (lambda: tank.position.y <= 50)

    tank.rotation = 0
    tank.throttle = .5
    yield (lambda: tank.position.x >= 500)

    tank.rotation = math.pi / 2
    yield (lambda: tank.position.y >= 250)

    tank.rotation = - 5/6 * math.pi
    tank.throttle = 1
    yield (lambda: tank.position.x <= x)

    diff = y - tank.position.y
    tank.rotation = math.pi / 2 * diff / abs (diff)
    yield (lambda: abs (tank.position.y - y) <= 10)

    tank.throttle = 0
    tank.rotation = 0
