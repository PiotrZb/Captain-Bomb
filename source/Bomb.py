import pygame

from Moveable_Animated_Alive import Moveable, Animated
from Settings import bomb_delay, current_dir


class Bomb(Moveable, Animated):

    def __init__(self, player_rect, player_shift, bomb_on=False):

        super().__init__()

        # animations
        self.animations = {'bomb off': [], 'bomb on': [], 'explosion': []}
        self.looped_animations = ['bomb off', 'bomb on']
        self.load_textures(current_dir + '/../textures/bomb')
        if bomb_on: self.animation_type = 'bomb on'
        else: self.animation_type = 'bomb off'

        # setting position
        self.image = self.animations[self.animation_type][self.animation_index]
        self.rect = self.image.get_rect()
        self.rect.center = player_rect.center
        self.rect.bottom = player_rect.bottom
        self.old_rect_center = self.rect.copy().center

        # bomb attributes
        self.exist = True
        self.on_timer = pygame.time.get_ticks()
        if bomb_on: self.status = 'bomb on'
        else: self.status = 'bomb off'
        self.give_dmg = False

        # setting starting velocity
        self.additional_xvel = player_shift.x * 6
        self.additional_yvel = player_shift.y * 1.5

    def update_status(self):

        # checking if the bomb should explode
        if self.status == 'bomb on' and pygame.time.get_ticks() - self.on_timer > bomb_delay:
            self.status = 'explosion'
            self.give_dmg = True

        # checking if object should be removed
        elif self.status == 'explosion' and not self.non_looped_animation_in_progress:
            self.exist = False

    def update_animation(self):

        if self.status == 'bomb off' and self.animation_type != 'bomb off':
            self.change_animation('bomb off')

        elif self.status == 'bomb on' and self.animation_type != 'bomb on':
            self.change_animation('bomb on')

        elif self.status == 'explosion' and self.animation_type != 'explosion':
            self.change_animation('explosion')

    def update(self, tiles, tiles_shift_vector):

        if self.status != 'explosion': self.collisions(tiles)

        if self.exist:

            self.update_status()
            self.update_animation()
            self.animate()

            # updating position
            self.rect.size = self.image.get_size()
            if self.status == 'explosion': self.rect.center = self.old_rect_center
            self.rect.x += tiles_shift_vector.x
            self.rect.y += tiles_shift_vector.y
            self.old_rect_center = self.rect.center
