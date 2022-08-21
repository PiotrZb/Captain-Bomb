import  pygame

from Tile import Tile
from Player import Player
from settings import tile_size, screen_width

class Level:

    def __init__(self,layout):

        # map
        self.tiles = pygame.sprite.Group()
        self.layout = layout
        self.tiles_shift_vector = pygame.math.Vector2(0,0)

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

    def update(self):

        # map
        self.shift_tiles()
        self.tiles.update(self.tiles_shift_vector)

        # player
        self.player.update(self.tiles)

    def draw(self,screen):

        self.tiles.draw(screen)
        self.player.draw(screen)

    def shift_tiles(self):
        player = self.player.sprite
        player_vert_pos = player.rect.x

        if player_vert_pos > screen_width - screen_width/3 and player.shift_vector.x > 0:
            self.tiles_shift_vector.x = -8
            player.speed = 0
        elif player_vert_pos < screen_width/3 and player.shift_vector.x < 0:
            self.tiles_shift_vector.x = 8
            player.speed = 0
        else:
            self.tiles_shift_vector.x = 0
            player.speed = 8





