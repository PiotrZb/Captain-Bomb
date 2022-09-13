import pygame

from settings import hp, screen_height, screen_width
from Moveable_Animated_Alive import Animated


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


class PauseMenu(pygame.sprite.Group):

    def __init__(self):

        super().__init__()

        self.active = False

        # background
        background = pygame.image.load('textures/backgrounds/gaus_background.png').convert_alpha()
        self.background = pygame.sprite.Sprite()
        self.background.image = pygame.transform.scale(background,(screen_width, screen_height))
        self.background.rect = self.background.image.get_rect()
        self.add(self.background)

        # baner
        self.baner = pygame.sprite.Sprite()
        texture = pygame.image.load('textures/gui/menu/baner/small baner.png').convert_alpha()
        self.baner.image = pygame.transform.scale(texture, (texture.get_rect().width * 6, texture.get_rect().height * 6))
        self.baner.rect = self.baner.image.get_rect()
        self.baner.rect.center = (screen_width / 2, 100)
        font = pygame.font.SysFont("Arial", 30, bold=True)
        text = font.render('PAUSE', 1, pygame.Color('black'))
        text_rect = text.get_rect()
        baner_rect = self.baner.rect
        self.baner.image.blit(text,(baner_rect.width/2 - text_rect.width/2, baner_rect.height/2 - text_rect.height/2 + 15))
        self.add(self.baner)

        # buttons
        self.buttons = []
        self.resume_button = Button((640, 360),'Resume')
        self.add(self.resume_button)
        self.buttons.append(self.resume_button)
        self.settings_button = Button((640, 436),'Settings') # + 76 y
        self.add(self.settings_button)
        self.buttons.append(self.settings_button)
        self.quit_button = Button((640, 512), 'Quit')  # + 76 y
        self.add(self.quit_button)
        self.buttons.append(self.quit_button)

    def switch_visibility(self):
        self.active = not self.active

    def menu_events(self):

        mouse_pos = pygame.mouse.get_pos()

        for button in self.buttons:
            if button.rect.collidepoint(mouse_pos):
                button.font_color = 'red'
                if pygame.mouse.get_pressed()[0] and not button.clicked:
                    button.clicked = True
                    button.image = button.textures[1]
                    button.offset_y = 0
                elif not pygame.mouse.get_pressed()[0] and button.clicked:
                    button.clicked = False
                    button.image = button.textures[0]
                    button.font_color = 'black'
                    button.offset_y = -5

                    # resume
                    if button == self.resume_button:
                        self.active = False

                    # exit
                    if button == self.quit_button:
                        return 0
            else:
                button.font_color = 'black'

        return 1

class MainMenu(pygame.sprite.Group):

    def __init__(self):

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
        self.buttons = []
        self.new_game_button = Button((640, 360),'New Game')
        self.add(self.new_game_button)
        self.buttons.append(self.new_game_button)
        self.settings_button = Button((640, 436),'Settings') # + 76 y
        self.add(self.settings_button)
        self.buttons.append(self.settings_button)
        self.credits_button = Button((640, 512), 'Credits')  # + 76 y
        self.add(self.credits_button)
        self.buttons.append(self.credits_button)
        self.exit_button = Button((640, 588), 'Exit')  # + 76 y
        self.add(self.exit_button)
        self.buttons.append(self.exit_button)

        # animated sprites
        self.hero_sprite = Animated()
        self.hero_sprite.animations = {'idle':[]}
        self.hero_sprite.looped_animations = ['idle']
        self.hero_sprite.load_textures('textures/player', 4)
        self.hero_sprite.image = self.hero_sprite.animations[self.hero_sprite.animation_type][0]
        self.hero_sprite.rect = self.hero_sprite.image.get_rect()
        self.hero_sprite.rect.center += pygame.Vector2(120, 350)
        self.add(self.hero_sprite)

        self.enemy_sprite = Animated()
        self.enemy_sprite.animations = {'idle': []}
        self.enemy_sprite.looped_animations = ['idle']
        self.enemy_sprite.load_textures('textures/enemies/captain', 4)
        self.enemy_sprite.image = self.enemy_sprite.animations[self.enemy_sprite.animation_type][0]
        self.enemy_sprite.rect = self.enemy_sprite.image.get_rect()
        self.enemy_sprite.rect.center += pygame.Vector2(840, 300)
        self.add(self.enemy_sprite)

    def switch_visibility(self):
        self.active = not self.active

    def menu_events(self):

        mouse_pos = pygame.mouse.get_pos()

        for button in self.buttons:
            if button.rect.collidepoint(mouse_pos):
                button.font_color = 'red'
                if pygame.mouse.get_pressed()[0] and not button.clicked:
                    button.clicked = True
                    button.image = button.textures[1]
                    button.offset_y = 0
                elif not pygame.mouse.get_pressed()[0] and button.clicked:
                    button.clicked = False
                    button.image = button.textures[0]
                    button.font_color = 'black'
                    button.offset_y = -5

                    # new game
                    if button == self.new_game_button:
                        self.active = False
                        return 2

                    # exit
                    if button == self.exit_button:
                        return 0
            else:
                button.font_color = 'black'

        return 1

    def update_animations(self):
        self.hero_sprite.animate()
        self.enemy_sprite.animate(flip=True)


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
