import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,size):

        super().__init__()

        self.image = pygame.surface.Surface((size,size))
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.image.fill('grey')