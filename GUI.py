import pygame

from settings import hp


class HealthBar(pygame.sprite.Group):

    def __init__(self, pos):

        super().__init__()

        self.bar_texture = pygame.image.load('textures/gui/health bar/Health Bar.png').convert_alpha()
        self.heart_texture = pygame.image.load('textures/gui/health bar/Heart.png').convert_alpha()

        # sprites
        self.bar_sprite = pygame.sprite.Sprite()
        self.bar_sprite.image = self.bar_texture
        self.bar_sprite.rect = self.bar_sprite.image.get_rect()
        self.bar_sprite.rect.topleft += pygame.Vector2(pos)

        self.heart1 = pygame.sprite.Sprite()
        self.heart1.image = self.heart_texture
        self.heart1.rect = self.heart1.image.get_rect()
        self.heart1.rect.topleft = self.bar_sprite.rect.topleft + pygame.Vector2(40,22)

        self.heart2 = pygame.sprite.Sprite()
        self.heart2.image = self.heart_texture
        self.heart2.rect = self.heart2.image.get_rect()
        self.heart2.rect.topleft = self.bar_sprite.rect.topleft + pygame.Vector2(66, 22)
        self.heart3 = pygame.sprite.Sprite()
        self.heart3.image = self.heart_texture
        self.heart3.rect = self.heart2.image.get_rect()
        self.heart3.rect.topleft = self.bar_sprite.rect.topleft + pygame.Vector2(92, 22)

        self.add(self.bar_sprite)
        self.add(self.heart1)
        self.add(self.heart2)
        self.add(self.heart3)

    def update(self, player_hp):

        x = int(hp/3)

        if player_hp > 2 * x:
            if self.heart1 not in self.sprites():
                self.add(self.heart1)

            if self.heart2 not in self.sprites():
                self.add(self.heart2)

            if self.heart3 not in self.sprites():
                self.add(self.heart3)

        elif player_hp > x:
            if self.heart1 not in self.sprites():
                self.add(self.heart1)

            if self.heart2 not in self.sprites():
                self.add(self.heart2)

            if self.heart3 in self.sprites():
                self.remove(self.heart3)

        elif player_hp > 0:
            if self.heart1 not in self.sprites():
                self.add(self.heart1)

            if self.heart2 in self.sprites():
                self.remove(self.heart2)

            if self.heart3 in self.sprites():
                self.remove(self.heart3)

        else:
            self.remove(self.heart1)
            self.remove(self.heart2)
            self.remove(self.heart3)
