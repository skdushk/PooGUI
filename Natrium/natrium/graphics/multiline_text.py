import pygame
from natrium import common
from natrium.graphics import color

def render_multiline(font, text:str, antialiased:bool, foreground, gradient_blend=0, gradient_orient='vertical'):
    array_text = text.splitlines()
    if array_text:
        max_text = max(*array_text, key=len) if len(array_text) > 1 else array_text[0]
    else:
        max_text = ''

    max_width = font.size(max_text)[0]

    text_surface = pygame.Surface([max_width+1, font.get_height()*len(array_text)+1], pygame.SRCALPHA, 32)

    for i, text in enumerate(array_text):

        text2 = font.render(text, antialiased, 'white')

        if isinstance(foreground[0], int) or common.is_str(foreground) or isinstance(foreground, pygame.Color):
            color_surf = pygame.Surface([text2.get_width()+1, font.get_height()+1])
            color_surf.fill(foreground)

        elif isinstance(foreground[0], (list, tuple, pygame.Color, str)) and len(foreground) == 2:
            color_surf = color.Color2(*foreground).gradient([text2.get_width()+1, font.get_height()], gradient_orient, gradient_blend)

        elif isinstance(foreground[0], (list, tuple, pygame.Color, str)) and len(foreground) == 3:
            color_surf = color.Color3(*foreground).gradient([text2.get_width()+1, font.get_height()], gradient_orient, gradient_blend)

        text_surface.blit(text2, (0, font.get_height()*i))
        text_surface.blit(color_surf, (0, font.get_height()*i), special_flags=pygame.BLEND_RGBA_MIN)

    return text_surface
