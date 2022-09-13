from os import listdir
from csv import reader
import pygame


def import_animation(path, scale=1):
    animation_images = []

    for image_path in sorted(listdir(path), key=lambda x: int(x.removesuffix('.png')), reverse=False):
        image = pygame.image.load(path + '/' + image_path).convert_alpha()
        image = pygame.transform.scale(image,(image.get_rect().width * scale, image.get_rect().height * scale))
        animation_images.append(image)

    return animation_images

def import_layout(path):

    with open(path,'r',newline='') as file:

        layout = reader(file, delimiter=',')
        return list(layout)
