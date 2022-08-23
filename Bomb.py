import pygame

from Moveable import Moveable
from functions import import_animation
from settings import animation_rate, bomb_delay


class Bomb(Moveable):

    def __init__(self, player_rect, bomb_on=False):

        super().__init__()

        self.animations = {'bomb off': [], 'bomb on': [], 'explosion': []}
        self.load_textures('textures/bomb')
        if bomb_on:
            self.animation_type = 'bomb on'
        else:
            self.animation_type = 'bomb off'
        self.animation_index = 0

        self.image = self.animations[self.animation_type][self.animation_index]
        self.rect = self.image.get_rect()
        self.rect.center = player_rect.center
        self.rect.bottom = player_rect.bottom
        self.old_rect = self.rect.copy()

        self.exist = True
        self.on_timer = pygame.time.get_ticks()

        # self.impact_area =

    def load_textures(self, textures_path):

        for animation_type in self.animations:
            self.animations[animation_type] = import_animation(textures_path + '/' + animation_type)

    def animate(self):

        self.image = self.animations[self.animation_type][int(self.animation_index)]

        if self.animation_type == 'explosion' and self.animation_index == 0:
            self.rect = self.image.get_rect()
            self.rect.center = self.old_rect.center

        self.animation_index += animation_rate

        if self.animation_index >= len(self.animations[self.animation_type]):
            if self.animation_type == 'bomb off':
                self.animation_index = 0
            elif self.animation_type == 'bomb on' and pygame.time.get_ticks() - self.on_timer > bomb_delay:
                self.animation_type = 'explosion'
                self.animation_index = 0
                self.old_rect = self.rect.copy()
            elif self.animation_type == 'bomb on':
                self.animation_index = 0
            else:
                self.exist = False

    def update(self, tiles, tiles_shift_vector):

        if self.animation_type != 'explosion':
            self.collisions(tiles)

        if self.exist: self.animate()

        self.rect.x += tiles_shift_vector.x
        self.rect.y += tiles_shift_vector.y
