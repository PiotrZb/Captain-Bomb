import pygame

from settings import gravity, jump_speed

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

        self.facing_direction = 'right'

class Alive(Moveable,Animated):

    def __init__(self):

        super().__init__()

