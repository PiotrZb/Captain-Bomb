import pygame

from Tile import Tile
from Player import Player
from settings import tile_size, screen_width, player_speed, bomb_radius, bomb_dmg


class Level:

    def __init__(self, layout):

        # map
        self.tiles = pygame.sprite.Group()
        self.layout = layout
        self.tiles_shift_vector = pygame.math.Vector2(0, 0)

        # Alive creatures
        self.alive = []

        # player
        self.player = pygame.sprite.GroupSingle()
        self.alive.append(self.player)

        # bombs
        self.bombs = pygame.sprite.Group()

        # reading layout and player starting position from settings
        self.read_layout()

    def read_layout(self):

        for y, row in enumerate(self.layout):
            for x, type in enumerate(row):

                if type == 'X':
                    self.tiles.add(Tile((x * tile_size, y * tile_size), tile_size))

                # reading player starting position
                elif type == 'P':
                    self.player.add(Player((x * tile_size, y * tile_size)))

    def update(self):

        # map
        self.shift_tiles()
        self.tiles.update(self.tiles_shift_vector)

        # player
        self.player.update(self.tiles, self.bombs)

        # bombs
        self.bombs.update(self.tiles, self.tiles_shift_vector)
        for bomb in self.bombs.sprites():

            # removal of used bombs
            if not bomb.exist:
                self.bombs.remove(bomb)

            # checking if bomb should give dmg to alive creatures in neighborhood
            elif bomb.give_dmg:

                # checking creatures in range
                for group in self.alive:
                    for creature in group.sprites():
                        creature_vec = pygame.math.Vector2(creature.rect.center)
                        if creature_vec.distance_to(bomb.rect.center) <= bomb_radius:
                            creature.dmg = bomb_dmg

                bomb.give_dmg = False

    def draw(self, screen):

        self.tiles.draw(screen)
        self.player.draw(screen)
        self.bombs.draw(screen)

    def shift_tiles(self):

        player = self.player.sprite
        player_vert_pos = player.rect.x

        if player_vert_pos > screen_width - screen_width / 3 and player.shift_vector.x > 0:
            self.tiles_shift_vector.x = -player_speed
            player.speed = 0

        elif player_vert_pos < screen_width / 3 and player.shift_vector.x < 0:
            self.tiles_shift_vector.x = player_speed
            player.speed = 0

        else:
            self.tiles_shift_vector.x = 0
            player.speed = player_speed
