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

red_sprite = Sprite(texture=cote_rouge, scale = (1, 1), position = level1.object_position('objects', 'red-start'), rotation_z = 90)
blue_sprite = Sprite(texture=cote_bleu, scale = (1, 1), position = level1.object_position('objects', 'blue-start'), rotation_z = 90)


if __name__ == '__main__':
    app.run()