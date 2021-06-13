#%%
from collections import OrderedDict
import json
from typing import Union
from ursina import *


def load_json(filename: Union[str, Path]):
    with open(filename) as level_file:
        return json.load(level_file)

#%%
class Level():
    """load level from a json (made with tiled)
Severall helper method are available"""
    def __init__(self, name: str, scale:float):
        filename = Path('assets', name + '.json')
        level = load_json(filename)
        self.level = level
        self.scale = scale

        # Assume tilewidth is the same than tileheight
        self.tile_size = level['tilewidth']
        tileset_final = {}
        for tileset in level['tilesets']:
            firstgit = tileset['firstgid']
            if 'source' not in tileset:
                raise NotImplementedError
            tileset = load_json(Path('assets', tileset['source']))
            for tile in tileset['tiles']:
                texture = load_texture(tile['image'])
                tile['texture'] = texture
                tileset_final[firstgit + tile['id']] = tile
        self.tileset = tileset_final

        self.layers = OrderedDict()
        self.objects_groups = OrderedDict()
        for layer in level['layers']:
            self.layers[layer['name']] = layer
            if layer['type'] == 'objectgroup':
                objects = OrderedDict()
                for o in layer['objects']:
                    objects[o['name']] = o
                self.objects_groups[layer['name']] = objects


    def object_position(self, layer, name):
        """search in the object layer for an """
        obj = self.objects_groups[layer][name]
        return (self.coc(obj['x']), -self.coc(obj['y']))


    def iter_layer(self, name):
        layer = self.layers[name]
        for chunk in layer['chunks']:
            data = iter(chunk['data'])
            height = chunk['height']
            width = chunk['width']
            start_x = chunk['x']
            start_y = chunk['y']
            for y in range(start_y, start_y + height):
                for x in range(start_x, start_x + width):
                    tile_id = next(data)
                    if tile_id != 0:
                        tile = self.tileset[tile_id]
                        yield (x * self.scale, -y * self.scale, tile)
        
    def iter_object_by_type(self, layer, type):
        for obj in self.objects_groups[layer].values():
            if obj['type'] == type:
                
                yield  (self.coc(obj['x']), -self.coc(obj['y']), obj)

    def coc(self, x):
        """convert object coordinate to game coordinate"""
        return x/self.tile_size * self.scale

# %%
if __name__ == '__main__':
    app = Ursina()
    level = Level('level1', 1/20)
