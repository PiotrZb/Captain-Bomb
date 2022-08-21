import pygame

from settings import  *
from Level import  Level

class Game:

    def __init__(self):

        self.status = 'on'

        # window
        self.screen = pygame.display.set_mode((screen_width,screen_height),pygame.RESIZABLE | pygame.SCALED)
        pygame.display.set_caption('King and Pigs')

        # main clock
        self.main_clock = pygame.time.Clock()

        # fps font
        pygame.font.init()
        self.font = pygame.font.SysFont("Arial" , 18 , bold = True)

        # Levels
        self.Level1 = Level(layout)

    def check_events(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.status = 'off'

    def show_fps(self):

        fps_str = str(int(self.main_clock.get_fps())) + ' fps'
        fps = self.font.render(fps_str, 1, pygame.Color('white'))
        self.screen.blit(fps, (10, 10))

    # game loop
    def run(self):

        while self.status == 'on':

            self.check_events()
            self.screen.fill((0, 0, 0))

            # updates
            self.Level1.update()

            # draw elements here
            self.Level1.draw(self.screen)

            self.show_fps()
            pygame.display.update()
            self.main_clock.tick(60)
