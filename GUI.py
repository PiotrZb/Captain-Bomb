import pygame

from settings import hp, screen_height, screen_width


class Button(pygame.sprite.Sprite):

    def __init__(self, center_pos, txt=''):

        super().__init__()

        # attributes
        self.clicked = False

        # text
        self.font = pygame.font.SysFont("Arial", 18, bold=True)
        self.font_color = 'black'
        self.text = txt
        self.txt = self.font.render(self.text, 1, pygame.Color(self.font_color))
        self.offset_y = -5

        # sprite attributes
        self.textures = []
        image = pygame.image.load('textures/gui/menu/button/basic.png').convert_alpha()
        self.textures.append(pygame.transform.scale(image,(image.get_rect().width * 4, image.get_rect().height * 4)))
        image = pygame.image.load('textures/gui/menu/button/clicked.png').convert_alpha()
        self.textures.append(pygame.transform.scale(image,(image.get_rect().width * 4, image.get_rect().height * 4)))
        self.image = self.textures[0]
        self.rect = self.image.get_rect()
        self.rect.center = center_pos

        txt_rect = self.txt.get_rect()
        self.image.blit(self.txt,(self.rect.width/2 - txt_rect.width/2, self.rect.height/2 - txt_rect.height/2  + self.offset_y))

    def update(self):

        self.txt = self.font.render(self.text, 1, pygame.Color(self.font_color))
        txt_rect = self.txt.get_rect()
        self.image.blit(self.txt, (self.rect.width / 2 - txt_rect.width / 2, self.rect.height / 2 - txt_rect.height / 2  + self.offset_y))


class Menu(pygame.sprite.Group):

    def __init__(self, screen_center):

        super().__init__()

        self.active = True

        # background
        background = pygame.image.load('textures/backgrounds/gaus_background.png').convert_alpha()
        self.background = pygame.sprite.Sprite()
        self.background.image = pygame.transform.scale(background,(screen_width, screen_height))
        self.background.rect = self.background.image.get_rect()
        self.add(self.background)

        # baner
        self.baner = pygame.sprite.Sprite()
        texture = pygame.image.load('textures/gui/menu/baner/baner.png').convert_alpha()
        self.baner.image = pygame.transform.scale(texture, (texture.get_rect().width * 3, texture.get_rect().height * 3))
        self.baner.rect = self.baner.image.get_rect()
        self.baner.rect.center = (screen_width/2, 100)
        self.add(self.baner)

        # buttons
        self.new_game_button = Button((640, 360),'New Game')
        self.add(self.new_game_button)

    def switch_visibility(self):
        self.active = not self.active

    def menu_events(self):

        mouse_pos = pygame.mouse.get_pos()

        # new game
        if self.new_game_button.rect.collidepoint(mouse_pos):
            self.new_game_button.font_color = 'red'
            if pygame.mouse.get_pressed()[0] and not self.new_game_button.clicked:
                self.new_game_button.clicked = True
                self.new_game_button.image = self.new_game_button.textures[1]
                self.new_game_button.offset_y = 0
            elif not pygame.mouse.get_pressed()[0] and self.new_game_button.clicked:
                self.active = False
                self.new_game_button.clicked = False
                self.new_game_button.image = self.new_game_button.textures[0]
                self.new_game_button.font_color = 'black'
                self.new_game_button.offset_y = -5
        else:
            self.new_game_button.font_color = 'black'




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
