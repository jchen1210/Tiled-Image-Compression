from collections import defaultdict

class Polyomino:
    '''
    A Polyomino shape, equipped with the ability to rotate and rescale
    '''
    def __init__(self, name: str, footprint: list):
        self.name = name
        self.footprint = footprint
        self.height = max(r for r,c in footprint) + 1
        self.width  = max(c for r,c in footprint) + 1

    def rotate(self) -> 'Polyomino':
        rotated = [(c, -r) for r,c in self.footprint]
        min_r = min(r for r,c in rotated)
        min_c = min(c for r,c in rotated)
        rotated = [(r-min_r, c-min_c) for r,c in rotated]
        return Polyomino(self.name, rotated)

    def get_rotations(self) -> list['Polyomino']:
        rots = []
        s = self
        for _ in range(4):
            if not any(set(s.footprint) == set(r.footprint) for r in rots):
                rots.append(s)
            s = s.rotate()
        return rots
    
    def get_scaled(self, scale: int) -> 'Polyomino':
        scaled_footprint = []
        for dr, dc in self.footprint:
            for u in range(scale):
                for v in range(scale):
                    i = dr*scale + u
                    j = dc*scale + v
                    scaled_footprint.append((i,j))
        scaled = Polyomino(self.name + "_x" + scale, scaled_footprint)
        return scaled
    
class Tile:
    '''
    A Polyomino tile with a colour
    '''
    def __init__(self, shape: Polyomino, colour: tuple):
        self.shape = shape
        self.colour = colour

    def anchor_footprint(self, anchor: tuple) -> list:
        anchored_footprint = []
        for block in self.shape.footprint:
            anchored_footprint.append((block[0] + anchor[0], block[1] + anchor[1]))
        return anchored_footprint

    
    def get_rotations(self) -> list[Polyomino]:
        return self.shape.get_rotations()

    def get_scaled(self, scale: int) -> 'Tile':
        return Tile(self.shape.get_scaled(scale), self.colour)
    


class TileSet:
    '''
    A set of Polyomino tiles used to tile a rectangular plane
    '''
    def __init__(self, base_tiles: list[Tile], scales: list[int]):
        self.tiles = []
        self.placements = []
        self.width = None
        self.height = None

        copy_scales = list(scales)
        if 1 not in scales:
            copy_scales.insert(0, 1)
        self.scales = copy_scales

        for tile in base_tiles:
            for scale in self.scales:
                for rotation in tile.get_rotations:
                    self.tiles.append(rotation.get_scaled(rotation))

    def set_placements(self, width: int, height: int) -> list:
        self.width = width
        self.height = height
        placements = []
        for tile in self.tiles:
            for i in range(height - tile.height):
                for j in range(width - tile.width):
                    placements.append((tile, (i, j)))

        self.placements = placements
        return self.placements
    
    def block_to_placements(self) -> dict:
        block_to_placements = defaultdict()
        for i, placement in enumerate(self.placements):
            tile = placement[0]
            anchor = placement[1]
            for block in tile.anchor_footprint(anchor):
                block_to_placements[block].append(i)
    
