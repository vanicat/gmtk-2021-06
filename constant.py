from ursina import Vec2

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