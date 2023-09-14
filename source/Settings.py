import pygame
import os
from Functions import import_layout

current_dir = os.path.dirname(os.path.abspath(__file__))
print(current_dir)

layouts1 = {
    'terrain': import_layout(current_dir + '/../layouts/test/test_terrain.csv'),
    'creatures': import_layout(current_dir + '/../layouts/test/test_creatures.csv'),
    'background terrain': import_layout(current_dir + '/../layouts/test/test_background terrain.csv'),
    'shelves': import_layout(current_dir + '/../layouts/test/test_shelves.csv'),
    'background objects': import_layout(current_dir + '/../layouts/test/test_background objects.csv')
}

level_textures = {}


def load_textures():
    level_textures['terrain'] = pygame.image.load(current_dir + '/../textures/map/Tiles.png').convert_alpha()


tile_size = 64
screen_width = 1280
screen_height = len(layouts1['terrain']) * tile_size

animation_rate = 0.2

hp = 100
player_speed = 4
jump_speed = -12
gravity = 0.51
bomb_delay = 3000
bomb_rate = 1000
bomb_radius = 150
