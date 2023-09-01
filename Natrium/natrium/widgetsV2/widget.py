import pygame
from natrium import graphics, display, widgets, widgetsV2

def get_abs_pos(widget, offset=None):
    offset = offset if offset else [0, 0]

    if not isinstance(widget, display.Window) and widget != pygame.display.get_surface():
        offset = [x+y+(z//2+1) for x, y, z in zip(offset, widget._absolute_pos, widget._padding)]

        if not isinstance(widget.container, display.Window) and widget.container != pygame.display.get_surface():
            get_abs_pos(widget.container, offset=offset)

    return offset
    #
    # return widget.get_rect().topleft

# Style Requirements:
"""
cornerradius
borderwidth

background
hover_bg
active_bg
disabled_bg

foreground
hover_fg
active_fg
disabled_fg

bordercolor
hover_bc
active_bc
disabled_fg

shadowcolor
hover_sc
active_sc
disabled_sc
shadow_blur
shadow_offsety
shadow_offsetx

gradient_orient
gradient_blend
"""

"""

inactive:

    body:
        color
        gradient_blend
        gradient_angle
    
    border:
        color
        gradient_blend
        gradient_angle
    
    text:
        color
        gradient_blend
        gradient_angle
        
    shadow:
        color
        blur
        offsetx
        offsety
        
hover:

    body:
        color
        gradient_blend
        gradient_angle
    
    border:
        color
        gradient_blend
        gradient_angle
    
    text:
        color
        gradient_blend
        gradient_angle
        
    shadow:
        color
        blur
        offsetx
        offsety
        
active:

    body:
        color
        gradient_blend
        gradient_angle
    
    border:
        color
        gradient_blend
        gradient_angle
    
    text:
        color
        gradient_blend
        gradient_angle
        
    shadow:
        color
        blur
        offsetx
        offsety

"""


class Widget(pygame.Surface):
    instances = []
    interactives = []

    placed_widgets_PREVIOUS = []
    placed_widgets = []

    triggered_widgets = []
    triggered_widgets_PREVIOUS = []

    @classmethod
    def reset(cls):
        cls.placed_widgets_PREVIOUS = cls.placed_widgets
        cls.placed_widgets = []

        cls.triggered_widgets_PREVIOUS = cls.triggered_widgets
        cls.triggered_widgets = []

        for widget in cls.interactives:
            if isinstance(widget, widgetsV2.Panel):
                widget._children_active = False

    @property
    def style(self):
        return self._style

    @style.setter
    def style(self, style):
        self._style = style

        self._base_hierarchy_rendering = self.render_custom_hierarchy(self._style['inactive'])

        if self in Widget.interactives and not isinstance(self, widgetsV2.Entry):
            self._base_secondary_rendering = self.render_custom_hierarchy(self._style['hover'])
            self._base_tertiary_rendering = self.render_custom_hierarchy(self._style['active'])

        elif isinstance(self, widgetsV2.Entry):
            self._base_secondary_rendering = self.render_custom_hierarchy(self._style['active'])

        if isinstance(self, widgetsV2.Label):
            self.string = self.string

    def __init__(self, container, style, size=(50, 15), padding=(10, 10)):
        sizepadding = [x+y for x, y in zip(size, padding)]
        shadow_offset = style['inactive']['shadow']['offsetx'], style['inactive']['shadow']['offsetx']
        shadow_blur = style['inactive']['shadow']['blur']*2

        if isinstance(self, (widgetsV2.Button, widgetsV2.RadioButton, widgetsV2.ToggleButton, widgetsV2.Checkbox)):
            shadow_offsetx = max(style['inactive']['shadow']['offsetx'],
                                 style['hover']['shadow']['offsetx'],
                                 style['active']['shadow']['offsetx'], 0)

            shadow_offsety = max(style['inactive']['shadow']['offsety'],
                                 style['hover']['shadow']['offsety'],
                                 style['active']['shadow']['offsety'], 0)

            shadow_offset = shadow_offsetx, shadow_offsety
            shadow_blur = max(style['inactive']['shadow']['blur'],
                              style['hover']['shadow']['blur'],
                              style['active']['shadow']['blur'], 0)*2

        elif isinstance(self, widgetsV2.Entry):
            shadow_offsetx = max(style['inactive']['shadow']['offsetx'],
                                 style['active']['shadow']['offsetx'], 0)

            shadow_offsety = max(style['inactive']['shadow']['offsety'],
                                 style['active']['shadow']['offsety'], 0)

            shadow_offset = shadow_offsetx, shadow_offsety
            shadow_blur = max(style['inactive']['shadow']['blur'],
                              style['active']['shadow']['blur'], 0)*2

        super().__init__([x+2+y+shadow_blur for x, y in zip(sizepadding, shadow_offset)], pygame.SRCALPHA, 32)

        self._base_size = size
        self._padding = padding

        self.rect = pygame.Rect((-1000, 0), sizepadding)
        self.container = container
        self._style = style
        if self._style['cornerradius'] in [0, 1]: self._style['cornerradius'] = [1, 1, 0, 1]

        self._relative_pos = (-1100, 0)
        self._absolute_pos = (-1100, 0)
        self._base_hierarchy_rendering = self.render_custom_hierarchy(self._style['inactive'])
        self._hierarchy_rendering = None
        self._isplaced = False
        self._placed_hierarchy = False
        self.is_custom_rect = False

        Widget.instances.append(self)
        if isinstance(self, (widgetsV2.Button, widgetsV2.Entry, widgetsV2.ToggleButton,
                             widgetsV2.RadioButton)):
            Widget.interactives.append(self)

    def render_custom_hierarchy(self, style):
        pos = [self._style['borderwidth']] * 2
        size = [x - self._style['borderwidth'] * 2 for x in self.rect.size]

        body = style['body']
        border = style['border']
        shadow = style['shadow']

        padding = graphics.draw.render_dynamic_rect(pygame.Rect(pos, size), body['color'], self._style['cornerradius'],
                                                    orient=body['gradient_orient'],
                                                    gradient_blend=body['gradient_blend'])
        content = pygame.Surface(self._base_size, pygame.SRCALPHA, 32)
        padding.blit(content, [x//2-y//2 for x, y in zip(self.rect.size, self._base_size)])

        bordercolor = (0, 0, 0, 0) if not self._style['borderwidth'] else border['color']

        border = graphics.draw.render_dynamic_rect(pygame.Rect(0, 0, *self.rect.size), bordercolor,
                                                   self._style['cornerradius'], orient=border['gradient_orient'],
                                                   gradient_blend=border['gradient_blend'])

        shadow = graphics.draw.render_dynamic_rect(pygame.Rect(0, 0, *self.rect.size), shadow['color'],
                                                   self._style['cornerradius'], orient=['gradient_orient'],
                                                   gradient_blend=shadow['gradient_blend'], gaussian=shadow['blur'])

        return [padding, border, content, shadow]

    def enable_custom_rect(self):
        self.is_custom_rect = True
    def disable_custom_rect(self):
        self.is_custom_rect = False

    def place_hierarchy(self):
        pos = [self._style['borderwidth']] * 2
        self.fill((0, 0, 0, 0))

        self._hierarchy_rendering = [self._base_hierarchy_rendering[0].copy(),
                                     self._base_hierarchy_rendering[1].copy(),
                                     self._base_hierarchy_rendering[2].copy(),
                                     self._base_hierarchy_rendering[3].copy()]

        self.blit(self._hierarchy_rendering[2], (self._style['inactive']['shadow']['offsetx'], self._style['inactive']['shadow']['offsety']))
        self.blit(self._hierarchy_rendering[1], (0, 0))
        self.blit(self._hierarchy_rendering[0], pos)

    def absolute_placement(self, x, y):
        Widget.placed_widgets.append(self)
        if isinstance(self.container, widgetsV2.Panel):
            if not (self.container in Widget.placed_widgets_PREVIOUS):
                return

        self._relative_pos = (x, y)
        if isinstance(self.container, display.Window):
            self._absolute_pos = self._relative_pos
        else:
            self._absolute_pos = [x+y for x, y in zip(self._relative_pos, get_abs_pos(self.container))]

        if self.rect != pygame.Rect(self._absolute_pos, self.rect.size) and not self.is_custom_rect:
            self.rect = pygame.Rect(self._absolute_pos, self.rect.size)

        self._isplaced = True
        if not self._placed_hierarchy:
            self.place_hierarchy()
            self._placed_hierarchy = True

        if isinstance(self.container, (widgetsV2.Panel, display.Window)):
            self.container.blit_wid(self, self._relative_pos)
        else:
            self.container.blit(self, self._relative_pos)