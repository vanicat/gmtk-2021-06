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
cookies = load_texture('cookies', path='assets')

class Game():
    def __init__(self, level_name) -> None:
        self.level = Level(level_name, SCALE)
        camera.position = self.level.object_position('objects', 'camera')

        self.red_sprite = Player(texture=cote_rouge, position=self.level.object_position('objects', 'red-start'))
        self.blue_sprite = Player(texture=cote_bleu, position=self.level.object_position('objects', 'blue-start'), control=False)

        self.red_sprite.other = self.blue_sprite
        self.blue_sprite.other = self.red_sprite

        def build_terrain_sprite(x, y, tile):
            return Sprite(tile['texture'], position=(x, y), scale = SCALE*3.2, collider='box')

        self.terrain = [build_terrain_sprite(x, y, tile) for x, y, tile in self.level.iter_layer('terrain')]  

        def build_cookies(x, y, tile):
            return Sprite(cookies, position=(x, y), scale = SCALE*3.2, collider='box', tile = tile)

        self.cookies = [build_cookies(x, y, tile) for x, y, tile in self.level.iter_object_by_type('objects', 'cookie')]
        print(self.cookies[0].x, self.cookies[0].y)

    def update(self):
        camera.position = (self.red_sprite.position + self.blue_sprite.position) / 2
        camera.z = -20

    def clear(self):
        scene.clear()

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

        new_dist = distance2d(self, self.other)
        if too_long and new_dist > self.length * 1.03:
            self.position += -self.velocity * time.dt
            self.velocity = Vec2(0, 0)  


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


game = None


def do_unpause():
    resume()
    unpause.disable()
    restart.disable()


def do_restart():
    global game
    if game: game.clear()
    game = Game('level1')
    do_unpause()


def do_button(title, do_it, pos):
    button = Button(title, scale = (.05, .01), position = pos)
    button.text_entity.scale = (1/5,1)
    button.always_on_top = True
    button.on_click = do_it
    button.ignore_paused = True
    button.eternal = True
    return button

unpause = do_button('start/continue', do_unpause, (0, 0.01))
restart = do_button('restart level', do_restart, (0, -0.01))
restart.disable()

def update():
    global game

    if game: game.update()
    else: game = Game('level1')

def input(key):
    if key == 'escape':
        unpause.enable()
        restart.enable()
        pause()

pause()


if __name__ == '__main__':
    app.run()
