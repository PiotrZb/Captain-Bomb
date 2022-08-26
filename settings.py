layout = [
    '                         ',
    '                         ',
    'P                        ',
    'XX                       ',
    '     XXX              B  ',
    'X            B       XXXX',
    'X           XXX          ',
    'X                        ',
    'XXX             XXX      ',
    'X      B              B  ',
    'XXXXXXXXXXXX         XXXX'
]

tile_size = 64

screen_width = 1280
screen_height = len(layout) * tile_size

animation_rate = 0.2

hp = 100
player_speed = 4
jump_speed = -12
gravity = 0.51
bomb_delay = 3000
bomb_rate = 1000
bomb_radius = 200
