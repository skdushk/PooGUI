import pygame
import sys
from natrium import graphics, widgets, styling, widgetsV2
from natrium.typehinting import *

class Window:
    @property
    def size(self):
        return self._disp.get_size()

    @property
    def width(self):
        return self._disp.get_width()

    @property
    def height(self):
        return self._disp.get_height()

    @property
    def style(self):
        return self._style

    @style.setter
    def style(self, val):
        self._style = val


    def __init__(self, size:IsSizeSequence, background:IsColor, gradial_orient:IsOrientLiteral = 'horizontal',
                 gradient_blend:int = 80, title:str = "Window", icon:str = None, resizable:bool = True):
        flags = pygame.SRCALPHA
        if resizable:
            flags |= pygame.RESIZABLE

        self._disp = pygame.display.set_mode(size, flags)
        pygame.display.set_caption(title)
        self.master = None

        if icon:
            pygame.display.set_icon(pygame.image.load(icon))

        self.background = background
        self.gradial_orient = gradial_orient
        self.gradient_blend = gradient_blend

        self._clock = pygame.time.Clock()
        self._events = []
        self._mpos = (0, 0)
        self._mprd = None
        self._rect = None
        self._previous_size = 0
        self._z_event_index = 0

    def trigger(self):
        self._events = pygame.event.get()
        self._mpos = pygame.mouse.get_pos()
        self._mprd = pygame.mouse.get_pressed()

        for event in self._events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit('Natrium GUI 0.6.0\nPygame Engine 2.v')

        if not isinstance(self.background, (list, tuple)):
            self._disp.fill(self.background)

        if isinstance(self.background, (list, tuple)):
            if self._previous_size != self.size:
                self._rect = graphics.draw.render_dynamic_rect(pygame.Rect(0, 0, *self.size),
                                                               self.background,
                                                               radius=1, orient=self.gradial_orient,
                                                               gradient_blend=self.gradient_blend)
            self._disp.blit(self._rect, (0, 0))

        self._previous_size = self.size

        for widget in widgetsV2.Widget.interactives:
                self.listen(widget)

        widgetsV2.Widget.reset()

    def listen(self, widget:widgets.Widget):
        params = []

        if isinstance(widget, (widgetsV2.Button, widgetsV2.Entry, widgetsV2.ToggleButton,
                               widgetsV2.RadioButton, widgets.Spinbox, widgetsV2.Panel)):
            params.append(self._events)

        if not (isinstance(widget, widgets.Panel) and not isinstance(widget, widgets.Listbox)):
            params.append(self._mpos)

        if isinstance(widget, (widgetsV2.Button, widgets.Spinbox)):
            params.append(self._mprd)

        widget.trigger(*params)

    def listen_multiple(self, widgets:clcs.Sequence[widgets.Widget]):
        for widget in widgets:
            self.listen(widget)

    def time_since_process(self):
        return pygame.time.get_ticks() / 1000

    def get_abs_offset(self):
        return self._disp.get_abs_offset()

    def get_offset(self):
        return self._disp.get_offset()

    def blit_wid(self, surf:pygame.Surface, dest:IsPosition):
        self._disp.blit(surf, dest)

    def get_rate(self):
        return self._clock.get_fps()

    def refresh(self):
        pygame.display.flip()
        self._clock.tick(62)
