import sys

import pygame

import Tile
import SimpleObjects
from Player import Player
from settings import tile_size, screen_width, player_speed, bomb_radius, level_textures
from Particles import Particles
import Enemies


class Level:

    def __init__(self, layouts):

        # map
        self.colidable_tiles = pygame.sprite.Group()
        self.noncolidable_tiles = pygame.sprite.Group()
        self.layouts = layouts
        self.tiles_shift_vector = pygame.math.Vector2(0, 0)

        # lists of moveable objects
        self.alive = []
        self.others = []
        self.enemies = pygame.sprite.Group()
        self.alive.append(self.enemies)

        # player
        self.player = pygame.sprite.GroupSingle()
        self.alive.append(self.player)
        self.player_particles = pygame.sprite.GroupSingle()
        self.player_particles.add(Particles())

        # bombs
        self.bombs = pygame.sprite.Group()
        self.others.append(self.bombs)

        self.load_level()

    def load_level(self):

        for key in self.layouts.keys():

            layout = self.layouts[key]

            for y, row in enumerate(layout):
                for x, type in enumerate(row):

                    if type != '-1':
                        match key:
                            case 'terrain':
                                self.colidable_tiles.add(Tile.TerrainTile((x * tile_size, y * tile_size), type))
                            case 'background terrain':
                                self.noncolidable_tiles.add(Tile.BackgroundTerrainTile((x * tile_size, y * tile_size), type))
                            case 'creatures':
                                if type == '18':
                                    self.player.add(Player((x * tile_size, y * tile_size)))
                                elif type == '17':
                                    self.enemies.add(Enemies.BaldPirate((x * tile_size, y * tile_size)))
                            case 'shelves':
                                self.colidable_tiles.add(Tile.Shelves((x * tile_size, y * tile_size), type))
                            case 'background objects':

                                if type == '13':
                                    self.noncolidable_tiles.add(SimpleObjects.Window((x * tile_size, y * tile_size)))

    def update(self):

        # map
        self.shift_tiles()
        self.colidable_tiles.update(self.tiles_shift_vector)
        self.noncolidable_tiles.update(self.tiles_shift_vector)

        # player
        self.player.update(self.colidable_tiles, self.bombs)
        player = self.player.sprite
        self.player_particles.sprite.update(player.rect.midbottom, player.facing_direction, self.tiles_shift_vector, player.current_status)

        # enemies
        self.enemies.update(self.colidable_tiles, self.tiles_shift_vector, player)

        # bombs
        self.bombs.update(self.colidable_tiles, self.tiles_shift_vector)
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
                        distance = creature_vec.distance_to(bomb.rect.midbottom)
                        if distance <= bomb_radius:
                            creature.hit_by_bomb(bomb.rect.midbottom)
                            creature.dmg = (bomb_radius - distance) / 3

                for group in self.others:
                    for object in group.sprites():
                        if object != bomb:
                            object_vec = pygame.math.Vector2(object.rect.center)
                            distance = object_vec.distance_to(bomb.rect.midbottom)
                            if distance <= bomb_radius:
                                object.hit_by_bomb(bomb.rect.midbottom)

                bomb.give_dmg = False

    def draw(self, screen):

        self.noncolidable_tiles.draw(screen)
        self.colidable_tiles.draw(screen)
        self.player.draw(screen)
        if self.player_particles.sprite.visible and self.player.sprite.is_alive:
            self.player_particles.draw(screen)
        self.enemies.draw(screen)
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
