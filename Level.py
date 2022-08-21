import  pygame

from Tile import Tile
from Player import Player
from settings import tile_size

class Level:

    def __init__(self,layout):

        # map
        self.tiles = pygame.sprite.Group()
        self.layout = layout

        # player
        self.player = pygame.sprite.GroupSingle()

        # reading layout and player starting position from settings
        self.read_layout()

    def read_layout(self):

        for y,row in enumerate(self.layout):
            for x,type in enumerate(row):
                if type == 'X':
                    self.tiles.add(Tile((x * tile_size, y * tile_size),tile_size))
                elif type == 'P':
                    self.player.add(Player((x * tile_size, y * tile_size)))

    def draw(self,screen):

        self.tiles.draw(screen)
        self.player.draw(screen)