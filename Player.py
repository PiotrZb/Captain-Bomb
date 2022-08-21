import pygame

from functions import import_animation
from settings import player_speed,jump_speed,animation_rate


class Player(pygame.sprite.Sprite):

    def __init__(self, pos):

        super().__init__()

        # animations
        self.animations = {'idle': [], 'run': [], 'jump': [], 'fall': [], 'jump anticipation': [], 'ground': [],
                           'hit': [], 'dead hit': [], 'dead ground': [], 'door in': [], 'door out': []}
        self.animation_index = 0
        self.animation_rate = animation_rate
        self.animation_type = 'idle'
        self.load_textures('textures/player')

        self.image = self.animations['idle'][0]
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

        # movement
        self.speed = player_speed
        self.shift_vector = pygame.math.Vector2(0, 0)
        self.gravity = 0.51
        self.jump_speed = jump_speed
        self.facing_direction = 'right'

    def change_animations(self, type):
        self.animation_type = type
        self.animation_index = 0

    def animate(self):
        self.image = self.animations[self.animation_type][int(self.animation_index)]
        if self.facing_direction == 'left':
            self.image = pygame.transform.flip(self.image,True,False)
        self.animation_index += self.animation_rate
        if self.animation_index >= len(self.animations[self.animation_type]):
            self.animation_index = 0

    def load_textures(self, textures_path):

        for animation_type in self.animations.keys():
            self.animations[animation_type] = import_animation(textures_path + '/' + animation_type)

    def control(self):

        pressed_keys = pygame.key.get_pressed()

        # move right
        if pressed_keys[pygame.K_d]:
            self.shift_vector.x = 1
            self.facing_direction = 'right'
            if self.animation_type != 'run':
                self.change_animations('run')

        # move left
        if pressed_keys[pygame.K_a]:
            self.shift_vector.x = -1
            self.facing_direction = 'left'
            if self.animation_type != 'run':
                self.change_animations('run')

        # stop
        if not (pressed_keys[pygame.K_d] or pressed_keys[pygame.K_a]):
            self.shift_vector.x = 0

        # jump
        if pressed_keys[pygame.K_SPACE] and self.shift_vector.y == 0:
            self.shift_vector.y = self.jump_speed

        # setting other animations
        if self.shift_vector == (0,0):
            self.change_animations('idle')
        elif self.shift_vector.y < 0:
            self.change_animations('jump')
        elif self.shift_vector.y > self.gravity:
            self.change_animations('fall')

    def collisions(self, tiles):

        # horizontal movement
        self.rect.x += self.shift_vector.x * self.speed

        for tile in tiles.sprites():

            if tile.rect.colliderect(self.rect):
                if self.shift_vector.x < 0:
                    self.rect.left = tile.rect.right
                    self.shift_vector.x = 0
                elif self.shift_vector.x > 0:
                    self.rect.right = tile.rect.left
                    self.shift_vector.x = 0

        # vertical movement
        self.shift_vector.y += self.gravity
        self.rect.y += self.shift_vector.y

        for tile in tiles.sprites():

            if tile.rect.colliderect(self.rect):
                if self.shift_vector.y < 0:
                    self.rect.top = tile.rect.bottom
                    self.shift_vector.y = 0.0001
                elif self.shift_vector.y > 0:
                    self.rect.bottom = tile.rect.top
                    self.gravity = 0
                    self.shift_vector.y = 0
            else:
                self.gravity = 0.51

    def update(self, tiles):

        self.control()
        self.collisions(tiles)
        self.animate()
