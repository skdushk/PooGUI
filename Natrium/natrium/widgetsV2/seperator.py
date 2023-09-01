from natrium import widgetsV2
import pygame

class Seperator(widgetsV2.Widget):
    def __init__(self, container, length, orient='horizontal', color='grey'):
        size = (length, 1) if orient == 'horizontal' else (1, length)

        default_style = {
            'cornerradius': 0,
            'borderwidth': 1,

            'inactive':
                {
                    'body':
                        {
                            'color': color,
                            'gradient_orient': 'vertical',
                            'gradient_blend': 10
                        },

                    'border':
                        {
                            'color': 'grey55',
                            'gradient_orient': 'vertical',
                            'gradient_blend': 10
                        },

                    'shadow':
                        {
                            'color': (0, 0, 0, 0),
                            'blur': 10,
                            'offsetx': 10,
                            'offsety': 10,
                            'gradient_orient': 'vertical',
                            'gradient_blend': 10
                        }

                }
        }

        super().__init__(container, padding=(0, 0), size=size, style=default_style)

    def render_custom_hierarchy(self, lol):
        line = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32) # ez
        line.fill(self._style['inactive']['body']['color'])

        return line

    def place_hierarchy(self):
        self.blit(self._base_hierarchy_rendering, (0, 0))
