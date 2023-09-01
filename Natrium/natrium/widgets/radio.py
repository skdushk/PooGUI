import pprint

import pygame
from natrium import widgets, graphics, common

default_style = {
    'cornerradius':[4, 4, 4, 4],
    'borderwidth':1,

    'background':'#DADADA',
    'hover_bg': '#EFEFFF',
    'active_bg':'#CFCFEF',

    'foreground':'black',
    'hover_fg': 'black',
    'active_fg':'black',

    'bordercolor':'grey55',
    'hover_bc': 'dodgerblue',
    'active_bc':'dodgerblue2',

    'gradial_orient':'horizontal',
    'gradient_blend': 10
}

class RadioButton(widgets.Label):
    @property
    def active(self):
        return self._event_mode == 2

    @active.setter
    def active(self, val):
        boolean = not not val
        self._event_mode = 2 if boolean else 0

    @property
    def string(self):
        return self._text

    @string.setter
    def string(self, val):
        self._text = val
        self._base_text_rendering = pygame.font.SysFont(*self._font_data).render(self._text, 1, self.style['foreground'])
        self._base_secondary_text = pygame.font.SysFont(*self._font_data).render(self._text, 1, self.style['hover_fg'])
        self._base_tertiary_text = pygame.font.SysFont(*self._font_data).render(self._text, 1, self.style['active_fg'])

        if len(self.style['foreground']) == 4 and not isinstance(self.style['foreground'], str):
            self._base_text_rendering.set_alpha(self.style['foreground'][3])
        if len(self.style['hover_fg']) == 4 and not isinstance(self.style['hover_fg'], str):
            self._base_secondary_text.set_alpha(self.style['hover_fg'][3])
        if len(self.style['active_fg']) == 4 and not isinstance(self.style['active_fg'], str):
            self._base_tertiary_text.set_alpha(self.style['active_fg'][3])

        self.place_hierarchy()

    def __init__(self, container, style=None, text="", font=('gadugi', 15), anchor='topleft', size=None, padding=(10, 10),
                 associate_with=None):

        style = style if style else default_style

        super().__init__(container, style, text, font, anchor, size, padding)
        self._base_secondary_rendering = self.render_secondary_hierarchy()
        self._base_secondary_text = pygame.font.SysFont(*font).render(self._text, 1, self.style['hover_fg'])

        self._base_tertiary_rendering = self.render_tertiary_hierarchy()
        self._base_tertiary_text = pygame.font.SysFont(*font).render(self._text, 1, self.style['active_fg'])
        self._event_mode = 0
        self._pre_event_mode = 0

        self._is_hover = False
        self._is_click = False

        self.associate_with = associate_with if associate_with else []

        if len(self.style['foreground']) == 4 and not isinstance(self.style['foreground'], str):
            self._base_text_rendering.set_alpha(self.style['foreground'][3])
        if len(self.style['hover_fg']) == 4 and not isinstance(self.style['hover_fg'], str):
            self._base_secondary_text.set_alpha(self.style['hover_fg'][3])
        if len(self.style['active_fg']) == 4 and not isinstance(self.style['active_fg'], str):
            self._base_tertiary_text.set_alpha(self.style['active_fg'][3])

    def render_secondary_hierarchy(self):
        pos = [self.style['borderwidth']]*2
        size = [x-self.style['borderwidth']*2 for x in self.rect.size]

        padding = graphics.draw.render_dynamic_rect(pygame.Rect(pos, size), self.style['hover_bg'], self.style['cornerradius'],
                                                    orient=self.style['gradial_orient'],
                                                    gradient_blend=self.style['gradient_blend'])
        content = pygame.Surface(self._base_size, pygame.SRCALPHA, 32)
        padding.blit(content, [x//2-y//2 for x, y in zip(self.rect.size, self._base_size)])

        bordercolor = (0, 0, 0, 0) if not self.style['borderwidth'] else self.style['hover_bc']

        border = graphics.draw.render_dynamic_rect(pygame.Rect(0, 0, *self.rect.size), bordercolor,
                                                   self.style['cornerradius'], orient=self.style['gradial_orient'],
                                                   gradient_blend=self.style['gradient_blend'])

        return [padding, border, content]

    def render_tertiary_hierarchy(self):
        pos = [self.style['borderwidth']]*2
        size = [x-self.style['borderwidth']*2 for x in self.rect.size]

        padding = graphics.draw.render_dynamic_rect(pygame.Rect(pos, size), self.style['active_bg'], self.style['cornerradius'],
                                                    orient=self.style['gradial_orient'],
                                                    gradient_blend=self.style['gradient_blend'])
        content = pygame.Surface(self._base_size, pygame.SRCALPHA, 32)
        padding.blit(content, [x//2-y//2 for x, y in zip(self.rect.size, self._base_size)])

        bordercolor = (0, 0, 0, 0) if not self.style['borderwidth'] else self.style['active_bc']

        border = graphics.draw.render_dynamic_rect(pygame.Rect(0, 0, *self.rect.size), bordercolor,
                                                   self.style['cornerradius'], orient=self.style['gradial_orient'],
                                                   gradient_blend=self.style['gradient_blend'])

        return [padding, border, content]

    def trigger(self, events, mpos):
        if isinstance(self.container, widgets.Panel):
            if not self.container._isplaced:
                return

        self._pre_event_mode = self._event_mode
        self._is_hover = False
        self._is_click = False

        if self.rect.collidepoint(*mpos):
            self._is_hover = True
            self._event_mode = 1 if self._event_mode != 2 else self._event_mode
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

        elif not any([x._is_hover for x in widgets.Widget.interactives]):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        if not self.rect.collidepoint(*mpos) and self._event_mode != 2:
            self._event_mode = 0

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(*event.pos) and event.button == 1:
                    self._is_click = True
                    self._event_mode = 2

        for widget in self.associate_with:
            if widget._is_click:
                self._event_mode = 0

        if self._pre_event_mode != self._event_mode:
            self.place_hierarchy()

    def place_hierarchy(self):
        pos = [self.style['borderwidth']]*2
        self.fill((0, 0, 0, 0))

        select_render_list = [self._base_hierarchy_rendering, self._base_secondary_rendering, self._base_tertiary_rendering]
        select_render = select_render_list[self._event_mode]

        select_text_list = [self._base_text_rendering, self._base_secondary_text, self._base_tertiary_text]
        select_text = select_text_list[self._event_mode]

        self._hierarchy_rendering = [select_render[0].copy(),
                                     select_render[1].copy(),
                                     select_render[2].copy()]
        self._text_rendering = select_text.copy()

        text_position = common.anchor_calculation(self._hierarchy_rendering[2], self._text_rendering, self.text_anchor,
                                                  0, -1)

        self._hierarchy_rendering[2].blit(self._text_rendering, text_position)
        self._hierarchy_rendering[0].blit(self._hierarchy_rendering[2], [x//2-y//2 for x, y in zip(self.rect.size, self._base_size)])

        self.blit(self._hierarchy_rendering[1], (0, 0))

        self.blit(self._hierarchy_rendering[0], pos)