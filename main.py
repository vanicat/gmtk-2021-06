from constant import *
from libs import *
from player import Player
from cookie import Cookie

from math import hypot
from ursina import *
from ursina.application import pause, resume
from ursina.prefabs.sprite import Sprite
from level_loader import Level

app = Ursina()

camera.orthographic = True
camera.fov = 1
window.borderless = False
window.exit_button = True


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
            return Sprite(tile['texture'], position=(x, y), scale = SCALE*3.2, collider='box', tile = tile)

        self.terrain = [build_terrain_sprite(x, y, tile) for x, y, tile in self.level.iter_layer('terrain')]  

        def build_cookies(x, y, tile):
            return Cookie(cookies, position=(x, y), scale = SCALE, tile = tile)

        self.cookies = [build_cookies(x, y, tile) for x, y, tile in self.level.iter_object_by_type('objects', 'cookie')]
        print(self.cookies[0].x, self.cookies[0].y)

    def update(self):
        camera.position = (self.red_sprite.position + self.blue_sprite.position) / 2
        camera.z = -20

    def clear(self):
        scene.clear()


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

def input(key):
    if key == 'escape':
        unpause.enable()
        restart.enable()
        pause()

game = Game('level1')
pause()


if __name__ == '__main__':
    app.run()
