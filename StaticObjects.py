import pygame

from Moveable_Animated_Alive import Animated
from settings import tile_size


class StaticObject(pygame.sprite.Sprite):

    def __init__(self, path, pos, offset=pygame.Vector2(0, 0), rotation=0, flipx=False, flipy=False):
        super().__init__()

        self.image = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.rotate(self.image, rotation)
        self.image = pygame.transform.flip(self.image,flipx,flipy)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.rect.topleft += offset

    def shift(self, shift_vector):
        self.rect.x += shift_vector.x
        self.rect.y += shift_vector.y

    def update(self, shift_vector):
        self.shift(shift_vector)


class Door(Animated):

    def __init__(self, pos):

        super().__init__()

        self.animations = {'closed': [], 'opening': [], 'closing': []}
        self.load_textures('textures/door')
        self.looped_animations = ['closed']
        self.animation_type = 'closing'
        self.image = self.animations[self.animation_type][0]
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.offset = pygame.Vector2(0, -32)
        self.rect.topleft += self.offset

    def shift(self, shift_vector):

        self.rect.x += shift_vector.x
        self.rect.y += shift_vector.y

    def update(self, shift_vector):

        self.animate()
        self.shift(shift_vector)

class Chain(Animated):

    def __init__(self, pos, type = 'small'):

        super().__init__()

        self.animations = {'basic': []}
        if type == 'small':
            self.load_textures('textures/chains/small chain')
        else:
            self.load_textures('textures/chains/big chain')
        self.offset = pygame.Vector2(0, tile_size - 52)
        self.looped_animations = ['basic']
        self.animation_type = 'basic'
        self.image = self.animations[self.animation_type][0]
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.rect.topleft += self.offset

    def shift(self, shift_vector):

        self.rect.x += shift_vector.x
        self.rect.y += shift_vector.y

    def update(self, shift_vector):

        self.animate()
        self.shift(shift_vector)


class CandleLight(Animated):

    def __init__(self, pos):
        super().__init__()

        self.animations = {'basic': []}
        self.load_textures('textures/candle light')
        self.looped_animations = ['basic']
        self.animation_type = 'basic'
        self.image = self.animations[self.animation_type][0]
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.offset = pygame.Vector2(-24, -45)
        self.rect.topleft += self.offset

    def shift(self, shift_vector):
        self.rect.x += shift_vector.x
        self.rect.y += shift_vector.y

    def update(self, shift_vector):
        self.animate()
        self.shift(shift_vector)


class Candle(Animated):

    def __init__(self, pos):
        super().__init__()

        self.animations = {'basic': []}
        self.load_textures('textures/candle')
        self.looped_animations = ['basic']
        self.animation_type = 'basic'
        self.image = self.animations[self.animation_type][0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos[0] + tile_size / 2 - self.rect.width / 2, pos[1] + self.rect.height)

    def shift(self, shift_vector):
        self.rect.x += shift_vector.x
        self.rect.y += shift_vector.y

    def update(self, shift_vector):
        self.animate()
        self.shift(shift_vector)


class Sunlight(Animated):

    def __init__(self, pos):
        super().__init__()

        self.animations = {'basic': []}
        self.load_textures('textures/sunlight')
        self.looped_animations = ['basic']
        self.animation_type = 'basic'
        self.image = self.animations[self.animation_type][0]
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.offset = pygame.Vector2(9, 9)
        self.rect.topleft += self.offset

    def shift(self, shift_vector):
        self.rect.x += shift_vector.x
        self.rect.y += shift_vector.y

    def update(self, shift_vector):
        self.animate()
        self.shift(shift_vector)
