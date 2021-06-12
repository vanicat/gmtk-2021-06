from ursina import *
from ursina.prefabs.sprite import Sprite

app = Ursina()

SCALE = 1/20

camera.orthographic = True
camera.fov = 1
scene.set_scale(SCALE)
window.borderless = False
window.exit_button = True

cote_bleu = load_texture('cote-bleu', path='assets')
cote_rouge = load_texture('cote-rouge', path='assets')

blue_sprite = Sprite(texture=cote_bleu, scale = (.03, .03), position = (.5, .45), rotation_z = 90)
red_sprite = Sprite(texture=cote_rouge, scale = (.03, .03), position = (-.5, -.45), rotation_z = 90)

if __name__ == '__main__':
    app.run()