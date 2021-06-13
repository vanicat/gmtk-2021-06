from constant import *
from libs import *
from ursina import *

class Cookie(Sprite):
    def __init__(self, game, texture, position, scale, tile):
        super().__init__(texture=texture, position=position, scale = scale*3.2, collider='box', tile = tile)
        self.game = game

    def collide(self):
        self.disable()

        if 'message' in self.tile:
            t = Text(self.tile['message'], scale = .1, position = (-0.02, 0))
            invoke(lambda: t.disable(), delay=2)

        if 'capacity' in self.tile:
            self.game.add_capacity(self.tile['capacity'])
