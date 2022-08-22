layout = [
    '                         ',
    '                         ',
    'P           XX           ',
    'XX           XXXX        ',
    '     XX          X       ',
    'X                XX    XX',
    'X           XX           ',
    'X                        ',
    'X      XXXXX     XX      ',
    'X          X            X',
    'XXXXXXXXXXXX          XXX'
]

tile_size = 64

screen_width = 1280
screen_height = len(layout) * tile_size

hp = 100
player_speed = 4
jump_speed = -12
bomb_delay = 2000
bomb_rate = 1000
gravity = 0.51

animation_rate = 0.2