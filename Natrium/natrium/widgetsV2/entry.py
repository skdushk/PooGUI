import pygame
from natrium import widgetsV2, widgets, common
from natrium.graphics import multiline_text

default_style = {
    'cornerradius': 0,
    'borderwidth': 1,

    'inactive':
        {
            'body':
                {
                    'color': '#FAFAFA',
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

    'active':
        {
            'body':
                {
                    'color': '#FAFAFA',
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
        }
}

class Entry(widgetsV2.Label):
    @property
    def string(self):
        return self._text

    @string.setter
    def string(self, val):
        self._text = val
        self._show_string = self.show_characters * len(self.string) if self.show_characters not in [None, 0] else self.string

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
                                                                    self.style['active']['text']['color'],
                                                                    self.style['active']['text']['gradient_blend'],
                                                                    self.style['active']['text']['gradient_orient']
                                                                    )

        if len(self.style['inactive']['text']['color']) == 4 and not isinstance(self.style['inactive']['text']['color'], str):
            self._base_text_rendering.set_alpha(self.style['inactive']['text']['color'][3])

        if len(self.style['active']['text']['color']) == 4 and not isinstance(self.style['active']['text']['color'], str):
            self._base_secondary_text.set_alpha(self.style['active']['text']['color'][3])

        self._text_size = pygame.font.SysFont(*self._font_data).size(self._show_string)
        self.place_hierarchy()

    def __init__(self, container, style=None, placeholder_text="", font=('gadugi', 12), anchor='topleft', size=(300, 15), padding=(10, 10),
                 multiline=False, show_characters:str=None, image_path=None, image_anchor='midtop', image_margin=(5, 5)):
        style = style if style else default_style

        super().__init__(container, style, placeholder_text, font, anchor, size, padding, image_path, image_anchor, image_margin)
        self._base_secondary_rendering = self.render_custom_hierarchy(self.style['active'])

        self._base_secondary_text = multiline_text.render_multiline(pygame.font.SysFont(*self._font_data),
                                                                   self._text,
                                                                   True,
                                                                   self.style['active']['text']['color'],
                                                                   self.style['active']['text']['gradient_blend'],
                                                                   self.style['active']['text']['gradient_orient']
                                                                   )
        self._event_mode = 0
        self._pre_event_mode = 0

        self.multiline = multiline
        self.show_characters = show_characters
        self._scroll_offset = 0
        self._is_hover = False
        self._is_click = False
        self._font_object = pygame.font.SysFont(*self._font_data)
        self._text_size = self._font_object.size(self._text)
        self._is_disabled = False

        self._active_seperator = pygame.Surface([1, self._text_size[1]])
        self._active_blink_timer = 0

        self._key_hold_timer = 0
        self._prev_key_hold_timer= 0

        self._seperator_index = len(self.string)

        self._show_string = self.show_characters * len(self.string) if self.show_characters not in [None, 0] else self.string
        self.string = self.string

        if len(self.style['inactive']['text']['color']) == 4 and not isinstance(self.style['inactive']['text']['color'], str):
            self._base_text_rendering.set_alpha(self.style['inactive']['text']['color'][3])

        if len(self.style['active']['text']['color']) == 4 and not isinstance(self.style['active']['text']['color'], str):
            self._base_secondary_text.set_alpha(self.style['active']['text']['color'][3])

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


        self._pre_event_mode = self._event_mode
        self._is_hover = False
        self._is_click = False

        if self._event_mode:
            self._active_blink_timer += 1
        else:
            self._active_blink_timer = 0

        if self.rect.collidepoint(*mpos):
            self._is_hover = True
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)

        elif not any([x._is_hover for x in widgetsV2.Widget.interactives]):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(*event.pos) and event.button == 1:
                    self._is_click = True
                    self._event_mode = not self._event_mode
                else:
                    self._event_mode = False

            if self._event_mode:
                if event.type == pygame.KEYDOWN:
                    list_str = list(self.string)
                    list_str.insert(self._seperator_index, event.unicode)

                    self.string = "".join(list_str)\
                        if common.ascii(event.unicode) > 31 else self.string

                    self._seperator_index = len(self.string) \
                        if (len(self.string)-1)-self._seperator_index == 0 and event.key not in [pygame.K_LEFT, pygame.K_RIGHT] \
                        else self._seperator_index

                    print((len(self.string))-self._seperator_index == 0)

                    text_len = pygame.font.SysFont(*self._font_data).size(self._text)[0]

                    if event.key == pygame.K_BACKSPACE:
                        self.string = self.string[0:self._seperator_index-1] + self.string[self._seperator_index:]
                        self._seperator_index -= 1

                        if text_len > self.rect.width:
                            self._scroll_offset = text_len-self.rect.width-12
                        else:
                            self._scroll_offset = 0

                    elif event.key == pygame.K_DELETE:
                        self.string = ''
                        self._scroll_offset = 0

                    elif event.key in [pygame.K_RETURN, pygame.K_KP_ENTER] and self.multiline:
                        self.string += '\n'

                    elif event.key == pygame.K_RIGHT:
                        if text_len > self.rect.width:
                            self._scroll_offset = -text_len+self.rect.width-10

                        self._scroll_offset = self._scroll_offset - 10 if not text_len < self.rect.width else self._scroll_offset
                        self._seperator_index = min(self._seperator_index+1, len(self.string))
                        print(self._seperator_index)

                    elif event.key == pygame.K_LEFT:
                        self._scroll_offset = min(0, self._scroll_offset+10)
                        self._seperator_index = max(self._seperator_index-1, 0)
                        print(self._seperator_index)

                    elif text_len > self.rect.width and \
                            ((len(self.string))-self._seperator_index == 0):
                        self._scroll_offset = -text_len+self.rect.width-12

        if self._event_mode != self._pre_event_mode or self._event_mode:
            widgetsV2.Widget.triggered_widgets.append(self)
            self.place_hierarchy()

    def place_hierarchy(self):
        pos = [self.style['borderwidth']]*2
        self.fill((0, 0, 0, 0))

        select_render_list = [self._base_hierarchy_rendering, self._base_secondary_rendering]
        select_render = select_render_list[self._event_mode]

        select_text_list = [self._base_text_rendering, self._base_secondary_text]
        select_text = select_text_list[self._event_mode]

        select_offset_list = [[self.style['inactive']['shadow']['offsetx'], self.style['inactive']['shadow']['offsety']],
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

        seperator_offset = pygame.font.SysFont(*self._font_data).size(self._text[:self._seperator_index])[0]
        if self._event_mode and self._active_blink_timer//30 % 2 == 0:
            self._hierarchy_rendering[2].blit(self._active_seperator,
                                              [text_position[0] + self._scroll_offset + seperator_offset, 0])

        self._hierarchy_rendering[2].blit(self._text_rendering, [text_position[0]+self._scroll_offset, text_position[1]])
        self._hierarchy_rendering[0].blit(self._hierarchy_rendering[2], [x//2-y//2 for x, y in zip(self.rect.size, self._base_size)])

        self.blit(self._hierarchy_rendering[3], select_offset)
        self.blit(self._hierarchy_rendering[1], (0, 0))
        self.blit(self._hierarchy_rendering[0], pos)


