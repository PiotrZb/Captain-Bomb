import pygame

from settings import bomb_rate
from Bomb import Bomb
from Moveable import Alive


class Player(Alive):

    def __init__(self, pos):

        super().__init__()

        # animations
        self.animations = {'idle': [], 'run': [], 'jump': [], 'fall': [], 'jump anticipation': [], 'ground': [],
                           'hit': [], 'dead hit': [], 'dead ground': [], 'door in': [], 'door out': []}
        self.looped_animations = ['idle', 'run', 'jump anticipation']
        self.load_textures('textures/player')

        # sprite attributes update
        self.image = self.animations[self.animation_type][0]
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

        # player attributes
        self.bombs = pygame.sprite.Group()
        self.bomb_timer = pygame.time.get_ticks()

    def update_animation(self):

        if not self.non_looped_animation_in_progress and self.is_alive:

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

        elif not self.is_alive and self.animation_type not in ['dead ground', 'dead hit']:

            if self.fall_dmg > 0:
                self.change_animation('dead ground')

            elif self.dmg > 0:
                self.change_animation('dead hit')

    def control(self):

        # reading pressed keys
        pressed_keys = pygame.key.get_pressed()

        # move right
        if pressed_keys[pygame.K_d] and self.current_status in ['running', 'idle']:
            self.shift_vector.x = 1
            self.facing_direction = 'right'

        # move left
        if pressed_keys[pygame.K_a] and self.current_status in ['running', 'idle']:
            self.shift_vector.x = -1
            self.facing_direction = 'left'

        # stop
        if not (pressed_keys[pygame.K_d] or pressed_keys[pygame.K_a]) and self.current_status in ['running', 'idle'] and not self.hit_by_bomb_status:
            self.shift_vector.x = 0

        # jump
        if pressed_keys[pygame.K_SPACE] and self.shift_vector.y == 0:
            self.shift_vector.y = self.jump_speed

        # drop bomb
        if pressed_keys[pygame.K_f] and pygame.time.get_ticks() - self.bomb_timer > bomb_rate:
            self.bombs.add(Bomb(self.rect, True))
            self.bomb_timer = pygame.time.get_ticks()
        else:
            self.bombs = pygame.sprite.Group()

    def update(self, tiles, bombs_list):

        # movement update
        if self.is_alive:
            self.control()
            self.update_status()
        else:
            self.shift_vector.x = 0
            self.shift_vector.y = 0

        self.collisions(tiles)

        # animation update
        self.update_animation()

        # checking if sprite should be flipped
        if self.facing_direction == 'left':
            self.animate(True)
        else:
            self.animate(False)

        # applying dmg
        if self.is_alive:
            self.apply_dmg()

        # adding new bombs to list
        bombs_list.add(self.bombs)
