from ursina import Vec2
from enum import Enum, auto

SCALE = 1/20
GRAVITY = Vec2(0, -.2)
SAUT = {
    'up': Vec2(0, -.2),
    'down': Vec2(0, .2),
    'left': Vec2(1, 2).normalized() * .2,
    'right': Vec2(-1, 2).normalized() * .2
}
ELAST = 1
COMMAND_SPEED = .1
WALKING_SPEED = .6

class Capacity(Enum):
    def _generate_next_value_(name:str, start, count, last_value):
        return name.lower()
    CLAW = auto()