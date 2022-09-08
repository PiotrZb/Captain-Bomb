import sys

import pygame
from random import randint
import GUI

import Tile
import StaticObjects
from Player import Player
from settings import tile_size, screen_width, player_speed, bomb_radius, screen_height
from Particles import Particles
import Enemies


class Level:

    def __init__(self, layouts):

        # background
        self.background_image = pygame.image.load('textures/backgrounds/background.png').convert_alpha()
        self.background_image = pygame.transform.scale(self.background_image, (screen_width, screen_height))

        # map
        self.colidable_tiles = pygame.sprite.Group()
        self.noncolidable_tiles = pygame.sprite.Group()
        self.layouts = layouts
        self.tiles_shift_vector = pygame.math.Vector2(0, 0)
        self.doors = []

        # lists of moveable objects
        self.alive = []
        self.others = []
        self.enemies = pygame.sprite.Group()
        self.enemies_particles = pygame.sprite.Group()
        self.alive.append(self.enemies)

        # player
        self.player = pygame.sprite.GroupSingle()
        self.alive.append(self.player)
        self.player_particles = pygame.sprite.GroupSingle()
        self.player_particles.add(Particles())

        # bombs
        self.bombs = pygame.sprite.Group()
        self.others.append(self.bombs)

        # hearts
        self.hearts = pygame.sprite.Group()

        # gui
        self.health_bar = GUI.HealthBar((20, 20))

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
                                self.noncolidable_tiles.add(
                                    Tile.BackgroundTerrainTile((x * tile_size, y * tile_size), type))
                            case 'creatures':
                                if type == '18':
                                    self.player.add(Player((x * tile_size, y * tile_size)))
                                elif type == '17':
                                    self.enemies.add(Enemies.BaldPirate((x * tile_size, y * tile_size)))
                                    self.enemies_particles.add(Particles())
                            case 'shelves':
                                self.colidable_tiles.add(Tile.Shelves((x * tile_size, y * tile_size), type))
                            case 'background objects':

                                # windows
                                if type == '13':
                                    self.noncolidable_tiles.add(
                                        StaticObjects.StaticObject('textures/non-animated objects/window.png',
                                                                   (x * tile_size, y * tile_size)))
                                    self.noncolidable_tiles.add(StaticObjects.Sunlight((x * tile_size, y * tile_size)))

                                # candles
                                elif type == '1':
                                    candle = StaticObjects.Candle((x * tile_size, y * tile_size))
                                    self.noncolidable_tiles.add(candle)
                                    self.noncolidable_tiles.add(StaticObjects.CandleLight(candle.rect.topleft))

                                # barrels
                                elif type == '6':
                                    random_number = randint(0, 1)
                                    if random_number == 0:
                                        flipx = False
                                    else:
                                        flipx = True
                                    self.noncolidable_tiles.add(
                                        StaticObjects.StaticObject('textures/non-animated objects/barrel.png',
                                                                   (x * tile_size, y * tile_size),
                                                                   pygame.Vector2(0, 20), flipx=flipx))

                                # bottles
                                elif type == '10' or type == '9':

                                    random_number = randint(0, 1)
                                    if random_number == 0:
                                        flipx = False
                                    else:
                                        flipx = True

                                    random_number = randint(0, 2)
                                    if random_number == 0:
                                        rotation = 0
                                    elif random_number == 1:
                                        rotation = 90
                                    else:
                                        rotation = -90

                                    random_number = randint(0, 2)
                                    if random_number == 0:
                                        path = 'textures/non-animated objects/red bottle.png'
                                    elif random_number == 1:
                                        path = 'textures/non-animated objects/blue bottle.png'
                                    else:
                                        path = 'textures/non-animated objects/green bottle.png'

                                    bottle = StaticObjects.StaticObject(path, (x * tile_size, y * tile_size),
                                                                        rotation=rotation, flipx=flipx)
                                    bottle.rect.topleft += pygame.Vector2(0, tile_size - bottle.rect.height)
                                    self.noncolidable_tiles.add(bottle)

                                # skulls
                                elif type == '11':

                                    random_number = randint(0, 1)
                                    if random_number == 0:
                                        flipx = False
                                    else:
                                        flipx = True

                                    random_number = randint(0, 1)
                                    if random_number == 0:
                                        flipy = False
                                    else:
                                        flipy = True

                                    random_number = randint(0, 4)
                                    if random_number == 0:
                                        rotation = 0
                                    elif random_number == 1:
                                        rotation = 90
                                    elif random_number == 2:
                                        rotation = 180
                                    elif random_number == 3:
                                        rotation = -180
                                    else:
                                        rotation = -90

                                    skull = StaticObjects.StaticObject('textures/non-animated objects/skull.png',
                                                                       (x * tile_size, y * tile_size), flipx=flipx,
                                                                       flipy=flipy, rotation=rotation)
                                    skull.rect.topleft += pygame.Vector2(0, tile_size - skull.rect.height)
                                    self.noncolidable_tiles.add(skull)

                                # tables
                                elif type == '12':
                                    self.noncolidable_tiles.add(
                                        StaticObjects.StaticObject('textures/non-animated objects/table.png',
                                                                   (x * tile_size, y * tile_size),
                                                                   pygame.Vector2(0, tile_size - 32)))

                                # chairs
                                elif type == '8':
                                    self.noncolidable_tiles.add(
                                        StaticObjects.StaticObject('textures/non-animated objects/chair.png',
                                                                   (x * tile_size, y * tile_size),
                                                                   pygame.Vector2(0, tile_size - 56)))

                                # chins
                                elif type == '4' or type == '5':
                                    random_number = randint(0, 1)
                                    if random_number == 0:
                                        type = 'small'
                                    else:
                                        type = 'big'
                                    self.noncolidable_tiles.add(
                                        StaticObjects.Chain((x * tile_size, y * tile_size), type))

                                # doors
                                elif type == '0':
                                    self.doors.append(StaticObjects.Door((x * tile_size, y * tile_size)))

                                # hearts
                                elif type == '16':
                                    self.hearts.add(StaticObjects.Heart((x * tile_size, y * tile_size)))

        self.noncolidable_tiles.add(self.doors)

    def update(self):

        # map
        self.shift_tiles()
        self.colidable_tiles.update(self.tiles_shift_vector)
        self.noncolidable_tiles.update(self.tiles_shift_vector)

        # player
        self.player.update(self.colidable_tiles, self.bombs)
        player = self.player.sprite
        self.player_particles.sprite.update(player.rect.midbottom, player.facing_direction, self.tiles_shift_vector,
                                            player.current_status)

        # enemies
        self.enemies.update(self.colidable_tiles, self.tiles_shift_vector, player, self.bombs.sprites())
        for index, enemy in enumerate(self.enemies):
            self.enemies_particles.sprites()[index].update(enemy.rect.midbottom, enemy.facing_direction,
                                                           self.tiles_shift_vector, enemy.current_status)

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

        # doors
        player_center = player.rect.center
        for door in self.doors:
            if door.rect.collidepoint(player_center) and door.animation_type != 'opening':
                door.change_animation('opening')
            elif door.animation_type != 'closing' and not door.rect.collidepoint(player_center):
                door.change_animation('closing')

        # hearts
        self.hearts.update(self.tiles_shift_vector)
        player_rect = player.rect
        for heart in self.hearts.sprites():
            if player_rect.contains(heart.rect) and heart.animation_type != 'collected':
                heart.change_animation('collected')
                player.dmg = -25

            elif heart.animation_type == 'collected' and not heart.non_looped_animation_in_progress:
                self.hearts.remove(heart)

        # gui update
        self.health_bar.update(player.hp)

    def draw(self, screen):

        screen.blit(self.background_image, (0, 0))

        self.noncolidable_tiles.draw(screen)
        self.colidable_tiles.draw(screen)
        self.player.draw(screen)
        if self.player_particles.sprite.visible and self.player.sprite.is_alive:
            self.player_particles.draw(screen)
        self.enemies.draw(screen)
        for index, particles in enumerate(self.enemies_particles.sprites()):
            if particles.visible and self.enemies.sprites()[index].is_alive:
                sprite = pygame.sprite.GroupSingle()
                sprite.add(particles)
                sprite.draw(screen)

        self.bombs.draw(screen)
        self.hearts.draw(screen)
        self.health_bar.draw(screen)

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
