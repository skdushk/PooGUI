from natrium import widgetsV2, common
from natrium.graphics import multiline_text
import pygame

# box_label = {
#     'cornerradius':0,
#     'borderwidth':0,
#
#     'background':(0, 0, 0, 0),
#     'foreground':'black',
#     'bordercolor':(0, 0, 0, 0),
#
#     'shadow_color':(0, 0, 0, 0),
#     'shadow_blur':0,
#     'shadow_offsetx':0,
#     'shadow_offsety':0,
#
#     'gradient_orient':'horizontal',
#     'gradient_blend': 10
# }

default_style = {
    'cornerradius': 0,
    'borderwidth': 0,

    'inactive':
        {
            'body':
                {
                    'color': (0, 0, 0, 0),
                    'gradient_orient': 'vertical',
                    'gradient_blend': 10
                },

            'border':
                {
                    'color': (0, 0, 0, 0),
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
                },

            'text':
                {
                    'color': 'black',
                    'gradient_orient': 'vertical',
                    'gradient_blend': 10
                }

        }
}

class Label(widgetsV2.Widget):
    @property
    def string(self):
        return self._text

    @string.setter
    def string(self, val):
        self._text = val

        # self._base_text_rendering = pygame.font.SysFont(*self._font_data).render(self._text, 1, self._style['foreground'])
        self._base_text_rendering = multiline_text.render_multiline(pygame.font.SysFont(*self._font_data),
                                                                    self._text,
                                                                    True,
                                                                    self.style['inactive']['text']['color'],
                                                                    self.style['inactive']['text']['gradient_blend'],
                                                                    self.style['inactive']['text']['gradient_orient']
                                                                    )
        if len(self.style['inactive']['text']['color']) == 4 and not isinstance(self.style['inactive']['text']['color'], str):
            self._base_text_rendering.set_alpha(self.style['inactive']['text']['color'][3])

        self.place_hierarchy()
        # pygame.event.post(pygame.event.Event(widgetsV2.Widget.EVENT_TRIGGER))

    @property
    def text_anchor(self):
        return self._text_anchor
    @text_anchor.setter
    def text_anchor(self, value):
        self._text_anchor = value
        self.place_hierarchy()

    @property
    def image(self):
        return self._image
    @image.setter
    def image(self, path):
        self._image = pygame.image.load(path) if path else pygame.Surface((1, 1), pygame.SRCALPHA, 32)
        self.place_hierarchy()

    @property
    def image_anchor(self):
        return self._image_anchor
    @image_anchor.setter
    def image_anchor(self, value):
        self._image_anchor = value
        self.place_hierarchy()

    @property
    def image_margin(self):
        return self._image_margin
    @image_margin.setter
    def image_margin(self, value):
        self._image_margin = value
        self.place_hierarchy()

    def __init__(self, container, style=None, text="", font=('gadugi', 12), anchor='center', size=None, padding=(0, 0),
                 image_path=None, image_anchor='midtop', image_margin=(5, 5)):

        style = style if style else default_style
        self._style = style

        self._text = text
        self._text_anchor = anchor

        self._font_data = font
        self._base_text_rendering = multiline_text.render_multiline(pygame.font.SysFont(*self._font_data),
                                                                    self._text,
                                                                    True,
                                                                    self.style['inactive']['text']['color'],
                                                                    self.style['inactive']['text']['gradient_blend'],
                                                                    self.style['inactive']['text']['gradient_orient']
                                                                    )
        if len(self.style['inactive']['text']['color']) == 4 and not isinstance(self.style['inactive']['text']['color'], str):
            self._base_text_rendering.set_alpha(self.style['inactive']['text']['color'][3])

        self._font_object = pygame.font.SysFont(*self._font_data)
        self._text_size = self._font_object.size(self._text)

        self._text_rendering = None
        size = size if size else [self._text_size[0], self._text_size[1]]

        self._image = pygame.Surface((1, 1), pygame.SRCALPHA, 32) if not image_path else pygame.image.load(image_path).convert_alpha()
        self._image_anchor = image_anchor
        self._image_margin = image_margin

        super().__init__(container, style, size, padding)

    def place_hierarchy(self):
        pos = [self.style['borderwidth']]*2
        self.fill((0, 0, 0, 0))

        self._hierarchy_rendering = [self._base_hierarchy_rendering[0].copy(),
                                     self._base_hierarchy_rendering[1].copy(),
                                     self._base_hierarchy_rendering[2].copy(),
                                     self._base_hierarchy_rendering[3].copy()]
        self._text_rendering = self._base_text_rendering.copy()
        iw, ih = self._image.get_size()
        tw, th = self._text_rendering.get_size()

        text_position = common.anchor_calculation(
            self._hierarchy_rendering[2],
            self._text_rendering,
            self._text_anchor,
            1, 0)

        image_position = text_position.copy()
        match self._image_anchor:
            case 'topleft':
                image_position[0] -= iw+self._image_margin[0]
                image_position[1] -= ih+self._image_margin[1]
            case 'topright':
                image_position[0] += tw+self._image_margin[0]
                image_position[1] -= ih+self._image_margin[1]
            case 'bottomright':
                image_position[0] += tw+self._image_margin[0]
                image_position[1] += th+self._image_margin[1]
            case 'bottomleft':
                image_position[0] -= iw+self._image_margin[0]
                image_position[1] += th+self._image_margin[1]
            case 'center':
                image_position[0] += tw//2-iw//2
                image_position[1] += th//2-iw//2
            case 'midtop':
                image_position[0] += tw//2-iw//2
                image_position[1] -= ih+self._image_margin[1]
            case 'midbottom':
                image_position[0] += tw//2-iw//2
                image_position[1] += th+self._image_margin[1]
            case 'midleft':
                image_position[0] -= iw+self._image_margin[0]
                image_position[1] += th//2-ih//2
            case 'midright':
                image_position[0] += tw+self._image_margin[0]
                image_position[1] += th//2-ih//2

        self._hierarchy_rendering[2].blit(self._text_rendering, text_position)
        self._hierarchy_rendering[0].blit(self._hierarchy_rendering[2], [x//2-y//2 for x, y in zip(self.rect.size, self._base_size)])

        self.blit(self._hierarchy_rendering[3], [self.style['inactive']['shadow']['offsetx'], self.style['inactive']['shadow']['offsety']])
        self.blit(self._hierarchy_rendering[1], (0, 0))
        self.blit(self._hierarchy_rendering[0], pos)
