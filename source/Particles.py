from Moveable_Animated_Alive import Animated
from Settings import current_dir


class Particles(Animated):

    def __init__(self):

        super().__init__()

        # animations
        self.animations = {'run particles':[],'jump particles':[],'fall particles':[]}
        self.looped_animations = ['run particles']
        self.load_textures(current_dir + '/../textures/particles')
        self.animation_type = 'run particles'
        self.image = self.animations[self.animation_type][0]
        self.rect = self.image.get_rect()
        self.visible = True

    def update(self, creature_midbottom, facing_dir, shift_vector, status):

        # this lines eliminate wrong frame generated during continuous jumping
        if self.animation_type == 'fall particles':
            self.visible = True

        # setting animation type
        match status:
            case 'running':
                self.visible = True
                if self.animation_type != 'run particles' and not self.non_looped_animation_in_progress:
                    self.change_animation('run particles')
            case 'jumping':
                self.visible = True
                if self.animation_type != 'jump particles':
                    self.change_animation('jump particles')
            case 'landing':
                if self.animation_type != 'fall particles':
                    self.change_animation('fall particles')
            case other:
                if not self.non_looped_animation_in_progress:
                    self.visible = False

        # setting position and offset
        if self.animation_index == 0:
            self.rect.midbottom = creature_midbottom
            match self.animation_type:
                case 'run particles':
                    if facing_dir == 'right':
                        self.rect.x -= 10
                    else:
                        self.rect.x += 10
                case 'jump particles':
                    if facing_dir == 'right':
                        self.rect.x -= 10
                    else:
                        self.rect.x -= 20
                case 'fall particles':
                    self.rect.x -= 35

        # map shift
        self.rect.x += shift_vector.x
        self.rect.y += shift_vector.y

        # checking if image should be flipped
        if facing_dir == 'left':
            self.animate(True)
        else:
            self.animate(False)
