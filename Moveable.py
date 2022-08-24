import pygame

from settings import gravity, jump_speed, animation_rate, hp
from functions import import_animation

class Moveable(pygame.sprite.Sprite):

    def __init__(self):

        super().__init__()

        # sprite attributes
        self.rect = pygame.rect.Rect(0,0,0,0)

        # basic attributes
        self.shift_vector = pygame.math.Vector2(0, 0)
        self.speed = 0
        self.gravity = gravity

        # additional attributes
        self.jump_speed = jump_speed
        self.fall_dmg = 0

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

                    # fall dmg
                    if self.shift_vector.y > 17:
                        self.fall_dmg = (self.shift_vector.y - 17) * 10

                    self.rect.bottom = tile.rect.top
                    self.gravity = 0
                    self.shift_vector.y = 0
            else:
                self.gravity = 0.51

class Animated(pygame.sprite.Sprite):

    def __init__(self):

        super().__init__()

        self.animations = {}
        self.looped_animations = []
        self.animation_type = 'idle'
        self.animation_index = 0
        self.animation_rate = animation_rate
        self.non_looped_animation_in_progress = False
        self.facing_direction = 'right'

    def change_animation(self, type):

        self.animation_type = type
        self.animation_index = 0

        # checking if animation is looped
        if self.animation_type not in self.looped_animations: self.non_looped_animation_in_progress = True

    def load_textures(self, textures_path):

        for animation_type in self.animations.keys():
            self.animations[animation_type] = import_animation(textures_path + '/' + animation_type)

    def animate(self,flip = False):

        # setting image
        self.image = self.animations[self.animation_type][int(self.animation_index)]

        # checking if image should be flipped
        if flip: self.image = pygame.transform.flip(self.image, True, False)

        # incrementing index
        self.animation_index += self.animation_rate

        # checking if index is out of range
        if self.animation_index >= len(self.animations[self.animation_type]):
            if self.animation_type in self.looped_animations: self.animation_index = 0
            else:
                self.animation_index = len(self.animations[self.animation_type]) - 1
                self.non_looped_animation_in_progress = False

        # updating size
        self.rect.size = self.image.get_size()

class Alive(Moveable,Animated):

    def __init__(self):

        super().__init__()

        self.hp = hp
        self.is_alive = True
        self.dmg = 0
        self.current_status = 'idle'

    def set_status(self):

        if self.shift_vector == (0, 0) and self.current_status != 'falling':
            self.current_status = 'idle'
        elif self.shift_vector == (0, 0) and self.current_status == 'falling':
            self.current_status = 'landing'
        elif self.shift_vector.x != 0 and self.shift_vector.y == 0:
            self.current_status = 'running'
        elif self.shift_vector.y > self.gravity:
            self.current_status = 'falling'
        elif self.shift_vector.y < 0:
            self.current_status = 'jumping'

    def apply_dmg(self):

        # applying dmg and fall dmg
        self.hp -= (self.dmg + self.fall_dmg)

        # checking if creature is dead
        if self.hp <= 0: self.is_alive = False
        else:
            self.dmg = 0
            self.fall_dmg = 0


