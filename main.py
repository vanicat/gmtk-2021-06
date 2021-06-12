from math import hypot
from ursina import *
from ursina.application import pause
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

    def input(self, key):
        if self.control:
            if key == 'space' and self.touching :
                self.velocity += SAUT[self.touching]
        if key == 'tab':
            self.control = not self.control
        
    def update(self):
        self.velocity += GRAVITY * time.dt
        if self.control:
            self.velocity.x += (held_keys['right arrow'] - held_keys['left arrow']) * time.dt

        touching = None

        direction = self.down
        hits_info = self.cast(direction)
        if hits_info.hit:
            self.velocity.y = max(self.velocity.y, 0)
            touching = 'down'

        direction = self.up
        hits_info = self.cast(direction)
        if hits_info.hit:
            self.velocity.y = min(self.velocity.y, 0)
            touching = 'up'

        direction = self.left
        hits_info = self.cast(direction)
        if hits_info.hit:
            self.velocity.x = max(self.velocity.x, 0)
            touching = 'left'

        direction = self.right
        hits_info = self.cast(direction)
        if hits_info.hit:
            self.velocity.x = min(self.velocity.x, 0)
            touching = 'right'
        
        self.touching = touching
        
        self.position += self.velocity * time.dt

    def cast(self, direction:Vec2):
        direction = direction.normalized()
        hits_info = boxcast(self.position + direction * self.width / 2, 
            direction = direction,
            distance = length(self.velocity) * time.dt,
            thickness = self.width/2,
            ignore = (self,),
            debug = True
        )
        
        return hits_info
        

red_sprite = Player(texture=cote_rouge, position=level1.object_position('objects', 'red-start'))
blue_sprite = Player(texture=cote_bleu, position=level1.object_position('objects', 'blue-start'), control=False)


red_sprite.other = blue_sprite
blue_sprite.other = red_sprite

def build_terrain_sprite(x, y, tile):
    return Sprite(tile['texture'], position=(x, y), scale = SCALE*3.2, collider='box')

terrain = [build_terrain_sprite(x, y, tile) for x, y, tile in level1.iter_layer('terrain')]  

if __name__ == '__main__':
    app.run()
