import pygame


class Tile(pygame.sprite.Sprite):

    def __init__(self, pos, size):

        super().__init__()

        # setting image and position
        self.image = pygame.surface.Surface((size, size))
        self.image.fill('grey')
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    def update(self, shift_vector):

        # shifting tile
        self.rect.x += shift_vector.x
        self.rect.y += shift_vector.y
