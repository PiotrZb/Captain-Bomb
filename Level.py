import  pygame

from Tile import Tile
from settings import tile_size

class Level:
    def __init__(self,layout):
        self.tiles = pygame.sprite.Group()
        self.layout = layout

        self.read_layout()

    def read_layout(self):

        for y,row in enumerate(self.layout):
            for x,type in enumerate(row):
                if type == 'X':
                    self.tiles.add(Tile((x * tile_size, y * tile_size),tile_size))

    def draw(self,screen):

        self.tiles.draw(screen)