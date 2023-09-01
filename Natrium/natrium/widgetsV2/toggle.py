from natrium import widgetsV2, common
from natrium.graphics import multiline_text
import pygame

default_style = {
    'cornerradius': 0,
    'borderwidth': 1,

    'inactive':
        {
            'body':
                {
                    'color': '#DADADA',
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
                    'blur': 0,
                    'offsetx': 0,
                    'offsety': 0,
                    'gradient_orient': 'vertical',
                    'gradient_blend': 10
                },

            'text':
                {
                    'color': 'black',
                    'gradient_orient': 'vertical',
                    'gradient_blend': 10
                }

        },

    'hover':
        {
            'body':
                {
                    'color': '#EFEFFF',
                    'gradient_orient': 'vertical',
                    'gradient_blend': 10
                },

            'border':
                {
                    'color': 'dodgerblue',
                    'gradient_orient': 'vertical',
                    'gradient_blend': 10
                },

            'shadow':
                {
                    'color': (0, 0, 0, 0),
                    'blur': 0,
                    'offsetx': 0,
                    'offsety': 0,
                    'gradient_orient': 'vertical',
                    'gradient_blend': 10
                },

            'text':
                {
                    'color': 'black',
                    'gradient_orient': 'vertical',
                    'gradient_blend': 10
                }

        },

    'active':
        {
            'body':
                {
                    'color': '#CFCFEF',
                    'gradient_orient': 'vertical',
                    'gradient_blend': 10
                },

            'border':
                {
                    'color': 'dodgerblue2',
                    'gradient_orient': 'vertical',
                    'gradient_blend': 10
                },

            'shadow':
                {
                    'color': (0, 0, 0, 0),
                    'blur': 0,
                    'offsetx': 0,
                    'offsety': 0,
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

class ToggleButton(widgetsV2.Label):
    @property
    def state(self):
        return self._event_mode == 2

    @state.setter
    def state(self, val):
        boolean = not not val
        self._event_mode = 2 if boolean else 0

    @property
    def string(self):
        return self._text

    @string.setter
    def string(self, val):
        self._text = val
        self._base_text_rendering = multiline_text.render_multiline(pygame.font.SysFont(*self._font_data),
                                                                    self._text,
                                                                    True,
                                                                    self.style['inactive']['text']['color'],
                                                                    self.style['inactive']['text']['gradient_blend'],
                                                                    self.style['inactive']['text']['gradient_orient']
                                                                    )

        self._base_secondary_text = multiline_text.render_multiline(pygame.font.SysFont(*self._font_data),
                                                                    self._text,
                                                                    True,
                                                                    self.style['hover']['text']['color'],
                                                                    self.style['hover']['text']['gradient_blend'],
                                                                    self.style['hover']['text']['gradient_orient']
                                                                    )

        self._base_tertiary_text = multiline_text.render_multiline(pygame.font.SysFont(*self._font_data),
                                                                   self._text,
                                                                   True,
                                                                   self.style['active']['text']['color'],
                                                                   self.style['active']['text']['gradient_blend'],
                                                                   self.style['active']['text']['gradient_orient']
                                                                   )

        if len(self.style['inactive']['text']['color']) == 4 and not isinstance(self.style['inactive']['text']['color'], str):
            self._base_text_rendering.set_alpha(self.style['inactive']['text']['color'][3])

        if len(self.style['hover']['text']['color']) == 4 and not isinstance(self.style['hover']['text']['color'], str):
            self._base_secondary_text.set_alpha(self.style['hover']['text']['color'][3])

        if len(self.style['active']['text']['color']) == 4 and not isinstance(self.style['active']['text']['color'], str):
            self._base_tertiary_text.set_alpha(self.style['active']['text']['color'][3])

    def __init__(self, container, text="", style=None, font=('gadugi', 12), anchor='topleft', size=None, padding=(10, 10),
                 image_path=None, image_anchor='midleft', image_margin=(5, 5)):

        style = style if style else default_style

        super().__init__(container, style, text, font, anchor, size, padding, image_path, image_anchor, image_margin)
        self._base_secondary_rendering = self.render_custom_hierarchy(self.style['hover'])

        self._base_tertiary_rendering = self.render_custom_hierarchy(self.style['active'])

        self._base_secondary_text = multiline_text.render_multiline(pygame.font.SysFont(*self._font_data),
                                                                    self._text,
                                                                    True,
                                                                    self.style['hover']['text']['color'],
                                                                    self.style['hover']['text']['gradient_blend'],
                                                                    self.style['hover']['text']['gradient_orient']
                                                                    )

        self._base_tertiary_text = multiline_text.render_multiline(pygame.font.SysFont(*self._font_data),
                                                                   self._text,
                                                                   True,
                                                                   self.style['active']['text']['color'],
                                                                   self.style['active']['text']['gradient_blend'],
                                                                   self.style['active']['text']['gradient_orient']
                                                                   )

        self._event_mode = 0
        self._pre_event_mode = 0

        self._is_hover = False
        self._is_click = False
        self._is_disabled = False

        if len(self.style['inactive']['text']['color']) == 4 and not isinstance(self.style['inactive']['text']['color'], str):
            self._base_text_rendering.set_alpha(self.style['inactive']['text']['color'][3])

        if len(self.style['hover']['text']['color']) == 4 and not isinstance(self.style['hover']['text']['color'], str):
            self._base_secondary_text.set_alpha(self.style['hover']['text']['color'][3])

        if len(self.style['active']['text']['color']) == 4 and not isinstance(self.style['active']['text']['color'], str):
            self._base_tertiary_text.set_alpha(self.style['active']['text']['color'][3])

    def disable(self):
        self._is_disabled = 1

    def enable(self):
        self._is_disabled = 0

    def trigger(self, events, mpos):
        if isinstance(self.container, widgetsV2.Panel):
            if not self.container._isplaced:
                return

        if self._is_disabled:
            self._event_mode = 2

            if self._pre_event_mode != self._event_mode:
                self.place_hierarchy()

            if self.rect.collidepoint(*mpos):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_NO)

            elif not any([x._is_hover for x in widgetsV2.Widget.interactives]):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

            return

        self._is_hover = False
        self._pre_event_mode = self._event_mode

        if self.rect.collidepoint(*mpos):
            self._is_hover = True
            self._event_mode = 1 if self._event_mode != 2 else self._event_mode
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

        elif not any([x._is_hover for x in widgetsV2.Widget.interactives]):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        if not self.rect.collidepoint(*mpos) and self._event_mode != 2:
            self._event_mode = 0

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(*event.pos) and event.button == 1:
                    self._is_click = True
                    self._event_mode = [2, 0][self._event_mode-1]

        if self._pre_event_mode != self._event_mode:
            widgetsV2.Widget.triggered_widgets.append(self)
            self.place_hierarchy()

    def place_hierarchy(self):
        pos = [self.style['borderwidth']]*2
        self.fill((0, 0, 0, 0))

        select_render_list = [self._base_hierarchy_rendering, self._base_secondary_rendering, self._base_tertiary_rendering]
        select_render = select_render_list[self._event_mode]

        select_text_list = [self._base_text_rendering, self._base_secondary_text, self._base_tertiary_text]
        select_text = select_text_list[self._event_mode]

        select_offset_list = [[self.style['inactive']['shadow']['offsetx'], self.style['inactive']['shadow']['offsety']],
                              [self.style['hover']['shadow']['offsetx'], self.style['hover']['shadow']['offsety']],
                              [self.style['active']['shadow']['offsetx'], self.style['active']['shadow']['offsety']]]
        select_offset = select_offset_list[self._event_mode]

        self._hierarchy_rendering = [select_render[0].copy(),
                                     select_render[1].copy(),
                                     select_render[2].copy(),
                                     select_render[3].copy()]
        self._text_rendering = select_text.copy()

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
                image_position[0] += tw//2
                image_position[1] += th//2
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

        self.blit(self._hierarchy_rendering[3], select_offset)
        self.blit(self._hierarchy_rendering[1], (0, 0))
        self.blit(self._hierarchy_rendering[0], pos)

default_style2 = {
    'cornerradius': 0,
    'borderwidth': 1,

    'inactive':
        {
            'body':
                {
                    'color': 'white',
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
                    'blur': 0,
                    'offsetx': 0,
                    'offsety': 0,
                    'gradient_orient': 'vertical',
                    'gradient_blend': 10
                },

            'checkmark':
                {
                    'color': (0, 0, 0, 0),
                    'gradient_orient': 'vertical',
                    'gradient_blend': 10
                }

        },

    'active':
        {

            'checkmark':
                {
                    'color': 'black',
                    'gradient_orient': 'vertical',
                    'gradient_blend': 10
                }
        }
}

class Checkbox(ToggleButton):
    def __init__(self, container, style=None, length=15, padding=(10, 10)):
        style = style if style else default_style2
        style2 = {
            'cornerradius': style['cornerradius'],
            'borderwidth': style['borderwidth'],

            'inactive':
                {
                    'body': style['inactive']['body'],

                    'border': style['inactive']['border'],

                    'shadow': style['inactive']['shadow'],

                    'text': style['inactive']['checkmark']

                },

            'hover':
                {
                    'body': style['inactive']['body'],

                    'border': style['inactive']['border'],

                    'shadow': style['inactive']['shadow'],

                    'text':
                        {
                            'color': (0, 0, 0, 0),
                            'gradient_orient': 'vertical',
                            'gradient_blend': 10
                        }

                },

            'active':
                {
                    'body': style['inactive']['body'],

                    'border': style['inactive']['border'],

                    'shadow': style['inactive']['shadow'],

                    'text': style['active']['checkmark']
                }
        }
        super().__init__(container, style=style2, text='✓', font=('segoeuisymbol', int(length/1.1)), anchor='center', size=[length]*2, padding=padding)
