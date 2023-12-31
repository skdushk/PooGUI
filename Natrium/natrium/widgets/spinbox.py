from natrium import widgets
import pygame
from math import ceil

default_style = {
    'cornerradius':[4, 0, 0, 4],
    'borderwidth':1,

    'background':'#FAFAFA',
    'active_bg':'#FAFAFA',

    'foreground':'black',
    'active_fg':'black',

    'bordercolor':'grey55',
    'active_bc':'dodgerblue',

    'gradial_orient':'horizontal',
    'gradient_blend': 10,

    'btn1': {
        'cornerradius':[0, 4, 0, 0],
        'borderwidth':1,

        'background':'dodgerblue4',
        'hover_bg':'dodgerblue3',
        'active_bg':'dodgerblue2',

        'foreground':'white',
        'hover_fg':'white',
        'active_fg':'white',

        'bordercolor':'navy',
        'hover_bc': 'dodgerblue4',
        'active_bc': 'dodgerblue3',

        'gradial_orient':'horizontal',
        'gradient_blend': 10,
    },

    'btn2': {
        'cornerradius':[0, 0, 4, 0],
        'borderwidth':1,

        'background':'dodgerblue4',
        'hover_bg':'dodgerblue3',
        'active_bg':'dodgerblue2',

        'foreground':'white',
        'hover_fg':'white',
        'active_fg':'white',

        'bordercolor':'navy',
        'hover_bc': 'dodgerblue4',
        'active_bc': 'dodgerblue3',

        'gradial_orient':'horizontal',
        'gradient_blend': 10,
    }

}

class Spinbox(widgets.InputBox):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        if self.min_val <= val <= self.max_val:
            self._value = val
            self.string = str(self._value)

    def __init__(self, container, style=None, default_val=0, font=('gadugi', 15), anchor='topleft', size=(300, 20),
                 padding=(10, 10), min_val=-1000, max_val=10000000000):

        style = style if style else default_style

        btn1_style = style['btn1']
        btn2_style = style['btn2']

        button_height = ceil((size[1]+padding[1])/2)
        size = size[0]-30, size[1]

        super().__init__(container, style, str(default_val), font, anchor, size, padding)

        self._value = default_val
        self.min_val = min_val
        self.max_val = max_val
        self._seperator = widgets.Seperator(container, 29, 'horizontal', style['bordercolor'])

        self._incr_btn = widgets.Button(container=container, style=btn1_style, text='5', font=('webdings', 15),
                                        anchor='center', size=(30, button_height), padding=(0, 0), command=self.incr_val)

        self._decr_btn = widgets.Button(container=container, style=btn2_style, text='6', font=('webdings', 15),
                                        anchor='center', size=(30, button_height), padding=(0, 0), command=self.decr_val)

    def incr_val(self):
        if self._value+1 <= self.max_val:
            self._value += 1
            self.string = str(self._value)

    def decr_val(self):
        if self.min_val <= self.value-1:
            self._value -= 1
            self.string = str(self._value)

    def trigger(self, events, mpos, mprd):
        if isinstance(self.container, widgets.Panel):
            if not self.container._isplaced:
                return

        self._pre_event_mode = self._event_mode

        self._is_hover = False
        self._is_click = False
        text_len = pygame.font.SysFont(*self._font_data).size(self._text)[0]

        if self._event_mode:
            self._active_blink_timer += 1
        else:
            self._active_blink_timer = 0

        if self.rect.collidepoint(*mpos):
            self._is_hover = True
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)

        elif not any([x._is_hover for x in widgets.Widget.interactives]):
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
                    if event.unicode.isdigit() or event.unicode == '-':
                        if event.unicode != '-':
                            self.string += event.unicode if self.min_val < int(self.string+event.unicode) < self.max_val else ''
                        else:
                            self.string += '-'

                    if event.key == pygame.K_BACKSPACE:
                        if text_len > self.rect.width:
                            self._scroll_offset = -text_len+self.rect.width-10
                        else:
                            self._scroll_offset = 0

                        self.string = self.string[0:-1]

                    elif event.key == pygame.K_DELETE:
                        self.string = ''
                        self._scroll_offset = 0

                    elif event.key in [pygame.K_RETURN, pygame.K_KP_ENTER] and self.multiline:
                        self.string += '\n'

                    elif event.key == pygame.K_RIGHT:
                        if text_len > self.rect.width:
                            self._scroll_offset = -text_len+self.rect.width-10

                        self._scroll_offset = self._scroll_offset - 10 if not text_len < self.rect.width else self._scroll_offset

                    elif event.key == pygame.K_LEFT:
                        self._scroll_offset = min(0, self._scroll_offset+10)

                    elif text_len > self.rect.width:
                        self._scroll_offset = -text_len+self.rect.width-10

        if self._event_mode != self._pre_event_mode or self._event_mode:
            self.place_hierarchy()


    def absolute_placement(self, x, y):
        self._seperator.absolute_placement(x+self.rect.width, y+self.rect.height//2)
        super().absolute_placement(x, y)
        self._incr_btn.absolute_placement(x+self.rect.width-1, y)
        self._decr_btn.absolute_placement(x+self.rect.width-1, y+self.rect.height//2)

