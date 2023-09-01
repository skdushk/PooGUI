from natrium import widgets, common
import pygame

default_style = {
    'cornerradius':0,
    'borderwidth':0,

    'background':(0, 0, 0, 0),
    'foreground':'black',
    'bordercolor':(0, 0, 0, 0),

    'gradial_orient':'horizontal',
    'gradient_blend': 10
}

class Label(widgets.Widget):
    @property
    def string(self):
        return self._text

    @string.setter
    def string(self, val):
        self._pre_text = self._text
        self._text = val

        self._base_text_rendering = pygame.font.SysFont(*self._font_data).render(self._text, 1, self.style['foreground'])
        if len(self.style['foreground']) == 4: self._base_text_rendering.set_alpha(self.style['foreground'][3])

        self.place_hierarchy()

    def __init__(self, container, style=None, text="", font=('gadugi', 15), anchor='topleft', size=None, padding=(0, 0)):

        style = style if style else default_style
        self.style = style

        self._text = text
        self._pre_text = self._text
        self.text_anchor = anchor

        self._font_data = font
        self._base_text_rendering = pygame.font.SysFont(*font).render(self._text, 1, self.style['foreground'])
        if len(self.style['foreground']) == 4: self._base_text_rendering.set_alpha(self.style['foreground'][3])

        self._font_object = pygame.font.SysFont(*self._font_data)
        self._text_size = self._font_object.size(self._text)

        self._text_rendering = None
        size = size if size else [self._text_size[0], self._text_size[1]]

        super().__init__(container, style, size, padding)

    def _trigger(self):
        super()._trigger()
        self._pre_text = self._text

    def place_hierarchy(self):
        pos = [self.style['borderwidth']]*2
        self.fill((0, 0, 0, 0))

        self._hierarchy_rendering = [self._base_hierarchy_rendering[0].copy(),
                                     self._base_hierarchy_rendering[1].copy(),
                                     self._base_hierarchy_rendering[2].copy()]
        self._text_rendering = self._base_text_rendering.copy()

        text_position = common.anchor_calculation(
            self._hierarchy_rendering[2],
            self._text_rendering,
            self.text_anchor,
            0, -1)

        self._hierarchy_rendering[2].blit(self._text_rendering, text_position)
        self._hierarchy_rendering[0].blit(self._hierarchy_rendering[2], [x//2-y//2 for x, y in zip(self.rect.size, self._base_size)])

        self.blit(self._hierarchy_rendering[1], (0, 0))
        self.blit(self._hierarchy_rendering[0], pos)
