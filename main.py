from math import hypot
from ursina import *
from ursina.application import pause, resume
from ursina.prefabs.sprite import Sprite
from level_loader import Level

def length(vec):
    return hypot(*vec)

app = Ursina()

SCALE = 1/20

camera.orthographic = True
camera.fov = 1
window.borderless = False
window.exit_button = True

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


cote_bleu = load_texture('cote-bleu', path='assets')
cote_rouge = load_texture('cote-rouge', path='assets')


level1 = Level('level1', SCALE)
camera.position = level1.object_position('objects', 'camera')

class Player(Sprite):
    def __init__(self, texture, position, control = True):
        super().__init__(texture=texture, position = position, scale=(SCALE, SCALE), collider = 'box')
        self.velocity = Vec2(0, 0)
        self.width = texture.width * SCALE / 100
        self.height = texture.height * SCALE / 64
        #self.collider.visible = True
        self.control = control
        self.other = None
        self.length = .5


    def input(self, key):
        if self.control:
            if key == 'space' and self.touching :
                for direction in self.touching:
                    self.velocity += SAUT[direction]
        if key == 'tab':
            self.control = not self.control
        
    def update(self):
        touching = set()

        direction = self.down
        hits_info = self.cast(direction)
        if hits_info.hit:
            touching.add('down')

        direction = self.up
        hits_info = self.cast(direction)
        if hits_info.hit:
            touching.add('up')

        direction = self.left
        hits_info = self.cast(direction)
        if hits_info.hit:
            touching.add('left')

        direction = self.right
        hits_info = self.cast(direction)
        if hits_info.hit:
            touching.add('right')

        self.touching = touching

        # update velocity
        self.velocity *= .9 ** time.dt
        self.velocity += GRAVITY * time.dt
        if self.control:
            if touching:
                speed = WALKING_SPEED
            else:
                speed = COMMAND_SPEED
            self.velocity.x += (held_keys['right arrow'] - held_keys['left arrow']) * time.dt * speed

        too_long = False

        dist = distance2d(self, self.other)
        if dist >= self.length:
            too_long = True
            vec = self.other.position - self.position
            vec = vec.normalized()
            k = sum(vec * self.velocity)
            if dist > self.length:
                k = k*1.10
            vec *= max(-k, 0)
            self.velocity += (vec.x, vec.y)

        if 'down' in touching:
            self.velocity.y = max(self.velocity.y, 0)
        if 'up' in touching:
            self.velocity.y = min(self.velocity.y, 0)
        if 'left' in touching:
            self.velocity.x = max(self.velocity.x, 0)
        if 'right' in touching:
            self.velocity.x = min(self.velocity.x, 0)
        
        self.position += self.velocity * time.dt

        #if too_long and distance2d(self, self.other) 



    def cast(self, direction:Vec2):
        direction = direction.normalized()
        self.position += direction * (max(length(self.velocity), 0.05) * time.dt)
        hits_info = self.intersects()
        self.position -= direction * (max(length(self.velocity), 0.05) * time.dt)
        
        """ raycast(self.position + direction * self.width / 2, 
            direction = direction,
            distance = ,
            #thickness = self.width/2,
            ignore = (self,),
            debug = True
        ) """
        
        return hits_info
        

red_sprite = Player(texture=cote_rouge, position=level1.object_position('objects', 'red-start'))
blue_sprite = Player(texture=cote_bleu, position=level1.object_position('objects', 'blue-start'), control=False)


red_sprite.other = blue_sprite
blue_sprite.other = red_sprite

def build_terrain_sprite(x, y, tile):
    return Sprite(tile['texture'], position=(x, y), scale = SCALE*3.2, collider='box')

terrain = [build_terrain_sprite(x, y, tile) for x, y, tile in level1.iter_layer('terrain')]  


def update():
    camera.position = (red_sprite.position + blue_sprite.position) / 2
    camera.z = -20


def do_unpause():
    print('unpause clicked')
    resume()
    unpause.disable()

unpause = Button('start/continue', scale = SCALE)
unpause.always_on_top = True
unpause.on_click = do_unpause
unpause.ignore_paused = True


def input(key):
    if key == 'escape':
        unpause.enable()
        pause()

pause()


if __name__ == '__main__':
    app.run()
