from os import listdir
import pygame


def import_animation(path):
    animation_images = []

    for image_path in sorted(listdir(path),key=lambda x : int(x.removesuffix('.png')),reverse=False):
        image = pygame.image.load(path + '/' + image_path).convert_alpha()
        animation_images.append(image)

    return animation_images
