import pygame

from Settings import *
from Level import Level
from GUI import MainMenu, PauseMenu


class Game:

    def __init__(self):

        self.status = 'on'

        # window
        self.screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE | pygame.SCALED)
        pygame.display.set_caption('King and Pigs')

        # main clock
        self.main_clock = pygame.time.Clock()

        # fps font
        pygame.font.init()
        self.font = pygame.font.SysFont("Arial", 18, bold=True)

        # menu
        self.main_menu = MainMenu()
        self.pause_menu = PauseMenu()

        # Levels
        load_textures()

    def check_events(self):

        for event in pygame.event.get():

            if self.main_menu.active:
                x = self.main_menu.menu_events()

                # exit
                if x == 0:
                    self.status = 'off'

                # new game
                elif x == 2:
                    self.Level1 = Level(layouts1)

            if self.pause_menu.active and not self.main_menu.active:
                if not self.pause_menu.menu_events():
                    self.main_menu.switch_visibility()
                    self.pause_menu.active = False

            # game exit
            if event.type == pygame.QUIT:
                self.status = 'off'

            elif event.type == pygame.KEYDOWN:

                # fullscreen mode
                if event.key == pygame.K_j:
                    pygame.display.toggle_fullscreen()

                # exit menu
                elif event.key == pygame.K_ESCAPE and not self.main_menu.active:
                    self.pause_menu.switch_visibility()

    def show_fps(self):

        fps_str = str(int(self.main_clock.get_fps())) + ' fps'
        fps = self.font.render(fps_str, 1, pygame.Color('white'))
        self.screen.blit(fps, (10, 10))

    # game loop
    def run(self):

        while self.status == 'on':

            self.check_events()
            self.screen.fill((0, 0, 0))

            if self.main_menu.active:
                self.main_menu.update()
                self.main_menu.update_animations()
                self.main_menu.draw(self.screen)

            elif self.pause_menu.active:
                self.pause_menu.update()
                self.pause_menu.draw(self.screen)

            else:
                # updates
                self.Level1.update()

                # draw elements here
                self.Level1.draw(self.screen)

            self.show_fps()
            pygame.display.update()
            self.main_clock.tick(60)
