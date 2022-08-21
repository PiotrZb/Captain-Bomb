import pygame

class Player(pygame.sprite.Sprite):

    def __init__(self,pos):

        super().__init__()

        self.image = pygame.surface.Surface((32,64))
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.image.fill('red')