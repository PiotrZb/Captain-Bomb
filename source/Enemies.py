import pygame

from Moveable_Animated_Alive import Alive
from Settings import player_speed, bomb_radius, current_dir
from Functions import import_animation


class Enemy(Alive):

    def __init__(self, pos, type='captain'):

        super().__init__()

        # animations
        self.animations = {'idle': [], 'run': [], 'jump': [], 'fall': [], 'jump anticipation': [], 'ground': [],
                           'hit': [], 'dead hit': [], 'dead ground': [], 'attack': []}
        self.looped_animations = ['idle', 'run', 'jump anticipation']
        self.load_textures(current_dir + '/../textures/enemies/' + type)

        # sprite attributes
        self.image = self.animations[self.animation_type][0]
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

        # movement
        self.speed = player_speed

    def control(self, player, bombs):
        pass

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

    def update(self, tiles, tiles_shift_vector, player, bombs):

        # movement update
        if self.is_alive:
            self.update_status()
            self.control(player, bombs)

        self.collisions(tiles)
        self.rect.x += tiles_shift_vector.x
        self.rect.y += tiles_shift_vector.y

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

        # eliminating some bugs
        self.rect.size = self.image.get_size()
        if not self.is_alive and self.shift_vector.y:
            self.shift_vector.x = 0


class Captain(Enemy):

    def __init__(self, pos):

        super().__init__(pos,'captain')

        # animations
        self.animations['scare run'] = import_animation(current_dir + '/../textures/enemies/captain/scare run')
        self.looped_animations.append('scare run')

        # Captain attributes
        self.attack_ready = True
        self.scared = False
        self.sc_timer = pygame.time.get_ticks()

    def control(self, player, bombs):

        # checking if player was hit
        if self.animation_type == 'attack' and self.attack_ready and int(self.animation_index) == len(
                self.animations[self.animation_type]) - 3:
            self.attack_ready = False

            if self.rect.colliderect(player.rect) and (
                    (player.rect.center[0] > self.rect.center[0] and self.facing_direction == 'right') or (
                    player.rect.center[0] < self.rect.center[0] and self.facing_direction == 'left')):
                player.dmg += 25
                player.hit_by_enemy(self.facing_direction)

        # calculating distance to player
        player_vec = pygame.math.Vector2(player.rect.center)
        distance_to_player = player_vec.distance_to(self.rect.center)

        # logic
        if distance_to_player < 500 and abs(self.rect.y - player.rect.y) < player.rect.height and player.is_alive and not self.scared:

            # player on right
            if player.rect.center[0] > self.rect.center[0]:
                self.facing_direction = 'right'

                if player.rect.center[0] <= self.rect.midright[0]:
                    self.shift_vector.x = 0
                    if self.animation_type != 'attack':
                        self.change_animation('attack')
                        self.attack_ready = True
                elif not self.non_looped_animation_in_progress:
                    self.shift_vector.x = 0.5

            # player on left
            elif player.rect.center[0] < self.rect.center[0]:
                self.facing_direction = 'left'

                if player.rect.center[0] >= self.rect.midleft[0]:
                    self.shift_vector.x = 0
                    if self.animation_type != 'attack':
                        self.change_animation('attack')
                        self.attack_ready = True
                elif not self.non_looped_animation_in_progress:
                    self.shift_vector.x = -0.5

        elif not self.scared:
            self.shift_vector.x = 0

        for bomb in bombs:

            # calculating distance to bomb
            bomb_vec = pygame.math.Vector2(bomb.rect.center)
            distance_to_bomb = bomb_vec.distance_to(self.rect.center)

            if distance_to_bomb < bomb_radius and abs(self.rect.y - bomb.rect.y) < bomb.rect.height or self.scared:

                if bomb.rect.center[0] <= self.rect.center[0]:
                    self.facing_direction = 'right'
                    self.shift_vector.x = 0.5
                    self.current_status = 'scared'
                    self.scared = True
                    self.sc_timer = pygame.time.get_ticks()
                    if self.animation_type != 'scare run':
                        self.change_animation('scare run')

                elif bomb.rect.center[0] > self.rect.center[0]:
                    self.facing_direction = 'left'
                    self.shift_vector.x = -0.5
                    self.current_status = 'scared'
                    self.scared = True
                    self.sc_timer = pygame.time.get_ticks()
                    if self.animation_type != 'scare run':
                        self.change_animation('scare run')

        # update
        current_ticks = pygame.time.get_ticks()
        if not self.scared:
            self.sc_timer = current_ticks
        elif current_ticks - self.sc_timer > 3.0:
            self.scared = False
            self.sc_timer = current_ticks
            if self.animation_type == 'scare run':
                self.change_animation('idle')
                self.current_status = 'idle'
                self.shift_vector.x = 0

        else:
            self.current_status = 'scare run'
            if self.facing_direction == 'left':
                self.shift_vector.x = -0.5
            else:
                self.shift_vector.x = 0.5


class BaldPirate(Enemy):

    def __init__(self, pos):

        super().__init__(pos, 'bald pirate')

        # bald pirate attributes
        self.kick_ready = True

    def control(self, player, bombs):

        # checking if player or bomb was hit
        if self.animation_type == 'attack' and self.kick_ready and int(self.animation_index) == len(
                self.animations[self.animation_type]) - 7:
            self.kick_ready = False

            if self.rect.colliderect(player.rect) and (
                    (player.rect.center[0] > self.rect.center[0] and self.facing_direction == 'right') or (
                    player.rect.center[0] < self.rect.center[0] and self.facing_direction == 'left')):
                player.dmg += 25
                player.hit_by_enemy(self.facing_direction)

            for bomb in bombs:
                if self.rect.colliderect(bomb.rect) and (
                        (bomb.rect.center[0] > self.rect.center[0] and self.facing_direction == 'right') or (
                        bomb.rect.center[0] < self.rect.center[0] and self.facing_direction == 'left')):
                    bomb.hit_by_enemy(self.facing_direction)


        # calculating distance to player
        player_vec = pygame.math.Vector2(player.rect.center)
        distance_to_player = player_vec.distance_to(self.rect.center)

        # logic
        if distance_to_player < 500 and abs(self.rect.y - player.rect.y) < player.rect.height and player.is_alive:

            # player on right
            if player.rect.center[0] > self.rect.center[0]:
                self.facing_direction = 'right'

                if player.rect.center[0] <= self.rect.midright[0]:
                    self.shift_vector.x = 0
                    if self.animation_type != 'attack':
                        self.change_animation('attack')
                        self.kick_ready = True
                elif not self.non_looped_animation_in_progress:
                    self.shift_vector.x = 0.5

            # player on left
            elif player.rect.center[0] < self.rect.center[0]:
                self.facing_direction = 'left'

                if player.rect.center[0] >= self.rect.midleft[0]:
                    self.shift_vector.x = 0
                    if self.animation_type != 'attack':
                        self.change_animation('attack')
                        self.kick_ready = True
                elif not self.non_looped_animation_in_progress:
                    self.shift_vector.x = -0.5

        else:
            self.shift_vector.x = 0

        for bomb in bombs:

            # calculating distance to bomb
            bomb_vec = pygame.math.Vector2(bomb.rect.center)
            distance_to_bomb = bomb_vec.distance_to(self.rect.center)

            if distance_to_bomb < bomb_radius and abs(self.rect.y - bomb.rect.y) < bomb.rect.height:

                if bomb.rect.center[0] < self.rect.center[0]:
                    self.facing_direction = 'left'
                    self.shift_vector.x = -0.5

                elif bomb.rect.center[0] > self.rect.center[0]:
                    self.facing_direction = 'right'
                    self.shift_vector.x = 0.5

                if bomb.rect.colliderect(self.rect) and (
                        (bomb.rect.center[0] <= self.rect.midright[0] and self.facing_direction == 'right') or (
                        bomb.rect.center[0] >= self.rect.midleft[0] and self.facing_direction == 'left')):
                    self.shift_vector.x = 0
                    if self.animation_type != 'attack':
                        self.change_animation('attack')
                        self.kick_ready = True


class BigGuy(Enemy):

    def __init__(self, pos):

        super().__init__(pos,'big guy')

        self.animations['idle bomb'] = []
        self.animations['pick'] = []
        self.animations['run bomb'] = []
        self.animations['throw'] = []

        self.looped_animations.append('idle bomb')
        self.looped_animations.append('run bomb')

    def control(self, player, bombs):
        pass


class Cucumber(Enemy):

    def __init__(self, pos):

        super().__init__(pos,'cucumber')

        self.animations['blow the wick'] = []

    def control(self, player, bombs):
        pass


class Whale(Enemy):

    def __init__(self, pos):

        super().__init__(pos,'whale')

        self.animations['swallow'] = []

    def control(self, player, bombs):
        pass