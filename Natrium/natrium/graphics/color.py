import pygame
from pygame import gfxdraw
from natrium.typehinting import *
from natrium.graphics import transform

def gradient(size, orient_rotation=0, colors=('red', 'blue'), blend:int = 10, ratio=(50, 50)):
    if sum(ratio) != 100 or len(colors) != len(ratio):
        return

    sizes = [(size[0]*(x/100)*3, size[1]*3) for x in ratio]
    triple_size = [x*3 for x in size]
    # if orient == "horizontal":
    #     gradient_surf = pygame.Surface((2, 1), pygame.SRCALPHA, 32)
    #     gfxdraw.pixel(gradient_surf, 0, 0, self.color1)
    #     gfxdraw.pixel(gradient_surf, 1, 0, self.color2)
    #
    # elif orient == "vertical":
    #     gradient_surf = pygame.Surface((1, 2), pygame.SRCALPHA, 32)
    #     gfxdraw.pixel(gradient_surf, 0, 0, self.color1)
    #     gfxdraw.pixel(gradient_surf, 0, 1, self.color2)
    #
    # else:
    #     return None
    main_surf = pygame.Surface(triple_size, pygame.SRCALPHA, 32)
    gradient_surf = pygame.Surface(triple_size, pygame.SRCALPHA, 32)
    for i, (size, color) in enumerate(zip(sizes, colors)):
        position = size[0]*i+1, 0
        pygame.draw.rect(gradient_surf, color, (position, size))

    center = gradient_surf.get_rect(topleft=(0, 0)).center
    rotated_image = pygame.transform.rotate(gradient_surf, orient_rotation)
    new_rect = rotated_image.get_rect(center=center)

    main_surf.blit(rotated_image, new_rect.topleft)

    gradient_surf = transform.gaussian_blur_surface(gradient_surf, blend)
    return main_surf.subsurface(triple_size[0]//3, triple_size[1]//3, *size)

def color_to_rgb(color:IsColor):
    return color.r, color.g, color.b

def color_to_rgba(color:IsColor):
    return *color_to_rgb(color), color.a

def hsv_to_rgb(h, s, v):
    color = pygame.Color((0, 0, 0, 255))
    color.hsva = (h, s, v, 100)
    return color_to_rgb(color)

def hsva_to_rgba(h, s, v, a):
    color = pygame.Color((0, 0, 0, 0))
    color.hsva = (h, s, v, a)
    return color_to_rgba(color)
