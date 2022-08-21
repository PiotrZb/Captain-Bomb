import pygame

class Player(pygame.sprite.Sprite):

    def __init__(self,pos):

        super().__init__()

        self.image = pygame.surface.Surface((32,64))
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.image.fill('red')

        # movement
        self.speed = 8
        self.shift_vector = pygame.math.Vector2(0,0)
        self.gravity = 0.5
        self.jump_speed = -16

    def controll(self):

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[pygame.K_d]:
            self.shift_vector.x = 1
        if pressed_keys[pygame.K_a]:
            self.shift_vector.x = -1
        if not (pressed_keys[pygame.K_d] or pressed_keys[pygame.K_a]):
            self.shift_vector.x = 0
        if pressed_keys[pygame.K_SPACE] and not self.shift_vector.y < 0:
            self.shift_vector.y = self.jump_speed

    def collisions(self,tiles):

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
                    self.shift_vector.y = 0
                elif self.shift_vector.y > 0:
                    self.rect.bottom = tile.rect.top
                    self.gravity = 0
                    self.shift_vector.y = 0
            else:
                self.gravity = 0.5

        print(self.gravity)

    def update(self,tiles):

        self.controll()
        self.collisions(tiles)
