import pygame

class Window(pygame.sprite.Sprite):

    def __init__(self, pos):

        super().__init__()

        self.image = pygame.image.load('textures/objects/window.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    def shift(self, shift_vector):

        self.rect.x += shift_vector.x
        self.rect.y += shift_vector.y

    def update(self, shift_vector):
        self.shift(shift_vector)