from collections import OrderedDict
import json
from typing import Union
from ursina import *


def load_json(filename: Union[str, Path]):
    with open(filename) as level_file:
        return json.load(level_file)

class Level():
    """load level from a json (made with tiled)
Severall helper method are available"""
    def __init__(self, name: str) -> None:
        filename = Path('assets', name + '.json')
        level = load_json(filename)
        self.level = level

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
        return (obj['x']/self.tile_size, obj['y']/self.tile_size)


    def iter_layer(self, name):
        layer = self.layers[name]
