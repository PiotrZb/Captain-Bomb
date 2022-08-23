import pygame

from functions import import_animation
from settings import player_speed, jump_speed, animation_rate, hp, bomb_rate, gravity
from Bomb import Bomb
from Moveable import Alive


class Player(Alive):

    def __init__(self, pos):

        super().__init__()

        # animations
        self.animations = {'idle': [], 'run': [], 'jump': [], 'fall': [], 'jump anticipation': [], 'ground': [],
                           'hit': [], 'dead hit': [], 'dead ground': [], 'door in': [], 'door out': []}
        self.looped_animations = ['idle', 'run', 'jump anticipation']
        self.animation_index = 0
        self.animation_rate = animation_rate
        self.animation_type = 'idle'
        self.load_textures('textures/player')
        self.non_looped_animation_in_progress = False

        # sprite traits
        self.image = self.animations['idle'][0]
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

        # movement
        self.facing_direction = 'right'
        self.previous_status = 'idle'
        self.current_status = 'idle'

        # player traits
        self.hp = hp
        self.is_alive = True
        self.dmg = 0
        self.bombs = pygame.sprite.Group()
        self.bomb_timer = pygame.time.get_ticks()

    def change_animation(self, type):
        self.animation_type = type
        self.animation_index = 0

    def animate(self):

        # checking if animation is looped
        if self.animation_type in self.looped_animations:
            self.non_looped_animation_in_progress = False
        else:
            self.non_looped_animation_in_progress = True

        # setting image
        self.image = self.animations[self.animation_type][int(self.animation_index)]

        # checking if image should be flipped
        if self.facing_direction == 'left':
            self.image = pygame.transform.flip(self.image, True, False)

        # incrementing index
        self.animation_index += self.animation_rate

        # checking if index is out of range
        if self.animation_index >= len(self.animations[self.animation_type]):
            if self.animation_type in self.looped_animations:
                self.animation_index = 0
            else:
                self.animation_index = len(self.animations[self.animation_type]) - 1
                self.non_looped_animation_in_progress = False

        # updating rect
        self.rect.size = self.image.get_size()

    def load_textures(self, textures_path):

        for animation_type in self.animations.keys():
            self.animations[animation_type] = import_animation(textures_path + '/' + animation_type)

    def set_status(self):
        self.previous_status = self.current_status

        if self.shift_vector == (0, 0) and self.previous_status != 'falling':
            self.current_status = 'idle'
        elif self.shift_vector == (0, 0) and self.previous_status == 'falling':
            self.current_status = 'landing'
        elif self.shift_vector.x != 0 and self.shift_vector.y == 0:
            self.current_status = 'running'
        elif self.shift_vector.y > self.gravity:
            self.current_status = 'falling'
        elif self.shift_vector.y < 0:
            self.current_status = 'jumping'

    def set_animation(self):

        if not self.non_looped_animation_in_progress and self.hp > 0:
            if (self.fall_dmg > 0 or self.dmg > 0) and self.animation_type != 'hit':
                self.change_animation('hit')
            elif self.current_status == 'running' and self.animation_type != 'run':
                self.change_animation('run')
            elif self.current_status == 'idle' and self.animation_type != 'idle':
                self.change_animation('idle')
            elif self.current_status == 'falling' and self.animation_type != 'fall':
                self.change_animation('fall')
            elif self.current_status == 'jumping' and self.animation_type != 'jump':
                self.change_animation('jump')
            elif self.current_status == 'landing' and self.animation_type != 'ground':
                self.change_animation('ground')
        elif self.hp <= 0 and self.animation_type not in ['dead ground', 'dead hit']:
            if self.fall_dmg > 0:
                self.change_animation('dead ground')
            elif self.dmg > 0:
                self.change_animation('dead hit')

    def control(self):

        pressed_keys = pygame.key.get_pressed()

        # move right
        if pressed_keys[pygame.K_d] and self.current_status in ['running','idle']:
            self.shift_vector.x = 1
            self.facing_direction = 'right'

        # move left
        if pressed_keys[pygame.K_a] and self.current_status in ['running','idle']:
            self.shift_vector.x = -1
            self.facing_direction = 'left'

        # stop
        if not (pressed_keys[pygame.K_d] or pressed_keys[pygame.K_a])  and self.current_status in ['running','idle']:
            self.shift_vector.x = 0

        # jump
        if pressed_keys[pygame.K_SPACE] and self.shift_vector.y == 0:
            self.shift_vector.y = self.jump_speed

        # setting bomb
        if pressed_keys[pygame.K_f] and pygame.time.get_ticks() - self.bomb_timer > bomb_rate:
            self.bombs.add(Bomb(self.rect,True))
            self.bomb_timer = pygame.time.get_ticks()
        else:
            self.bombs = pygame.sprite.Group()

    def update(self, tiles, bombs_list):

        if self.hp > 0:
            self.control()
            self.collisions(tiles)
            self.set_status()

        self.set_animation()
        self.animate()

        if self.fall_dmg > 0:
            self.hp -= self.fall_dmg
            if self.hp > 0: self.fall_dmg = 0

        if self.dmg > 0:
            self.hp -= self.dmg
            if self.hp > 0: self.dmg = 0

        bombs_list.add(self.bombs)

