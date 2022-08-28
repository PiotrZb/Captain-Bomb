import pygame

from settings import tile_size, level_textures


class Tile(pygame.sprite.Sprite):

    def __init__(self, pos):

        super().__init__()

        # setting image and position
        self.image = pygame.surface.Surface((tile_size, tile_size), pygame.SRCALPHA, 32)
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    def shift(self, shift_vector):

        # shifting tile
        self.rect.x += shift_vector.x
        self.rect.y += shift_vector.y

    def update(self, shift_vector):

        self.shift(shift_vector)

class TerrainTile(Tile):

    def __init__(self, pos, id):

        super().__init__(pos)
        self.id = id

        self.get_tile_texture()

    def get_tile_texture(self):

        rect = pygame.rect.Rect(0,0,0,0)

        match self.id:
            case '0':
                rect = pygame.rect.Rect(0, 0, tile_size, tile_size)
            case '1':
                rect = pygame.rect.Rect(tile_size, 0, tile_size, tile_size)
            case '2':
                rect = pygame.rect.Rect(2 * tile_size, 0, tile_size, tile_size)
            case '6':
                rect = pygame.rect.Rect(0, tile_size, tile_size, tile_size)
            case '8':
                rect = pygame.rect.Rect(2 * tile_size, tile_size, tile_size, tile_size)
            case '12':
                rect = pygame.rect.Rect(0, 2 * tile_size, tile_size, tile_size)
            case '13':
                rect = pygame.rect.Rect(tile_size, 2 * tile_size, tile_size, tile_size)
            case '14':
                rect = pygame.rect.Rect(2 * tile_size, 2 * tile_size, tile_size, tile_size)
            case '18':
                rect = pygame.rect.Rect(0, 3 * tile_size, tile_size, tile_size)
            case '19':
                rect = pygame.rect.Rect(tile_size, 3 * tile_size, tile_size, tile_size)
            case '24':
                rect = pygame.rect.Rect(0, 4 * tile_size, tile_size, tile_size)
            case '25':
                rect = pygame.rect.Rect(tile_size, 4 * tile_size, tile_size, tile_size)
            case other:
                print('Tile texture not found')

        self.image.blit(level_textures['terrain'], (0,0), rect)

class BackgroundTerrainTile(Tile):

    def __init__(self, pos, id):

        super().__init__(pos)

        self.id = id

        self.get_tile_texture()

    def get_tile_texture(self):

        rect = pygame.rect.Rect(0, 0, 0, 0)

        match self.id:
            case '3':
                rect = pygame.rect.Rect(3 * tile_size, 0, tile_size, tile_size)
            case '4':
                rect = pygame.rect.Rect(4 * tile_size, 0, tile_size, tile_size)
            case '5':
                rect = pygame.rect.Rect(5 * tile_size, 0, tile_size, tile_size)
            case '9':
                rect = pygame.rect.Rect(3 * tile_size, tile_size, tile_size, tile_size)
            case '10':
                rect = pygame.rect.Rect(4 * tile_size, tile_size, tile_size, tile_size)
            case '11':
                rect = pygame.rect.Rect(5 * tile_size, tile_size, tile_size, tile_size)
            case '15':
                rect = pygame.rect.Rect(3 * tile_size, 2 * tile_size, tile_size, tile_size)
            case '16':
                rect = pygame.rect.Rect(4 * tile_size, 2 * tile_size, tile_size, tile_size)
            case '17':
                rect = pygame.rect.Rect(5 * tile_size, 2 * tile_size, tile_size, tile_size)
            case '20':
                rect = pygame.rect.Rect(2 * tile_size, 3 * tile_size, tile_size, tile_size)
            case '21':
                rect = pygame.rect.Rect(3 * tile_size, 3 * tile_size, tile_size, tile_size)
            case '26':
                rect = pygame.rect.Rect(2 * tile_size, 4 * tile_size, tile_size, tile_size)
            case '27':
                rect = pygame.rect.Rect(3 * tile_size, 4 * tile_size, tile_size, tile_size)
            case other:
                print('Tile texture not found')

        self.image.blit(level_textures['terrain'], (0, 0), rect)

class Shelves(Tile):

    def __init__(self, pos, id):

        super().__init__(pos)

        self.id = id

        self.rect.size = (tile_size, 9)

        self.get_tile_texture()

    def get_tile_texture(self):

        rect = pygame.rect.Rect(0, 0, 0, 0)

        match self.id:
            case '22':
                rect = pygame.rect.Rect(4 * tile_size, 3 * tile_size, tile_size, tile_size)
            case '23':
                rect = pygame.rect.Rect(5 * tile_size, 3 * tile_size, tile_size, tile_size)
            case '28':
                rect = pygame.rect.Rect(4 * tile_size, 4 * tile_size, tile_size, tile_size)
            case '29':
                rect = pygame.rect.Rect(5 * tile_size, 4 * tile_size, tile_size, tile_size)
            case other:
                print('Tile texture not found')

        self.image.blit(level_textures['terrain'], (0, 0), rect)