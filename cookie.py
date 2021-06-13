from constant import *
from libs import *
from ursina import *

class Cookie(Sprite):
    def __init__(self, texture, position, scale, tile):
        super().__init__(texture=texture, position=position, scale = scale*3.2, collider='box', tile = tile)

    def collide(self):
        self.disable()