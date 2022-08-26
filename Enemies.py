import pygame

from Moveable_Animated_Alive import Alive

class BaldPirate(Alive):

    def __init__(self, pos):

        super().__init__()

        # animations
        self.animations = {'idle': [], 'run': [], 'jump': [], 'fall': [], 'jump anticipation': [], 'ground': [],
                           'hit': [], 'dead hit': [], 'dead ground': [], 'attack':[]}
        self.looped_animations = ['idle', 'run', 'jump anticipation']
        self.load_textures('textures/enemies/bald pirate')

        # sprite attributes update
        self.image = self.animations[self.animation_type][0]
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    def control(self, player_rect):

        # calculating distance to player
        player_vec = pygame.math.Vector2(player_rect.center)
        distance_to_player = player_vec.distance_to(self.rect.center)

        # logic

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

    def update(self, tiles, tiles_shift_vector, player_rect):

        # movement update
        if self.is_alive:
            self.update_status()
            self.control(player_rect)

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