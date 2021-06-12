from ursina import *
from ursina.prefabs.sprite import Sprite
from level_loader import Level

app = Ursina()

SCALE = 1/20

camera.orthographic = True
camera.fov = 1
scene.set_scale(SCALE)
window.borderless = False
window.exit_button = True

cote_bleu = load_texture('cote-bleu', path='assets')
cote_rouge = load_texture('cote-rouge', path='assets')


level1 = Level('level1')
camera.position = level1.object_position('objects', 'camera')
camera.position *= SCALE

class Player(Sprite):
    def __init__(self, texture, position):
        super().__init__(texture=texture, position = position, scale=(1, 1), rotation_z=90)


red_sprite = Player(texture=cote_rouge, position=level1.object_position('objects', 'red-start'))
blue_sprite = Player(texture=cote_bleu, position=level1.object_position('objects', 'blue-start'))


def build_terrain_sprite(x, y, tile):
    return Sprite(tile['texture'], scale=2 * tile['imageheight'] * SCALE,
                  position=(x, y), collider='box')

terrain = [build_terrain_sprite(x, y, tile) for x, y, tile in level1.iter_layer('terrain')]  

if __name__ == '__main__':
    app.run()
