from natrium import widgets

default_style = {
    'cornerradius':4,
    'borderwidth': 1,

    'background':'#EFEFEF',
    'bordercolor':'grey55',

    'gradial_orient': 'horizontal',
    'gradient_blend': 10
}

class Panel(widgets.Widget):
    def __init__(self, container, style=None, size=(400, 300), padding=(10, 10)):

        style = style if style else default_style

        super().__init__(container, style, size, padding)
        self._isplaced = True
        self._previous_isplaced = True
        self._children_active = False

        self._children = []

    def blit_wid(self, widget, position):
        self._children.append((widget, position))

    def _trigger(self):
        super(Panel, self)._trigger()
        self._children_active = False

    def place_hierarchy(self):
        pos = [self.style['borderwidth']]*2
        self.fill((0, 0, 0, 0))

        self._hierarchy_rendering = [self._base_hierarchy_rendering[0].copy(),
                                     self._base_hierarchy_rendering[1].copy(),
                                     self._base_hierarchy_rendering[2].copy()]

        for widget, position in self._children:
            self._hierarchy_rendering[2].blit(widget, position)

        self._hierarchy_rendering[0].blit(self._hierarchy_rendering[2], [x//2-y//2 for x, y in zip(self.rect.size, self._base_size)])

        self.blit(self._hierarchy_rendering[1], (0, 0))
        self.blit(self._hierarchy_rendering[0], pos)

    def absolute_placement(self, x, y):
        for widget, position in self._children:
            if widget in widgets.Widget.interactives:
                if isinstance(widget, widgets.InputBox):
                    if widget._event_mode:
                        self.place_hierarchy()
                        self._children_active = True
                        break

                if widget._pre_event_mode != widget._event_mode:
                    self.place_hierarchy()
                    self._children_active = True
                    break

            if isinstance(widget, widgets.Label):
                if widget._pre_text != widget.string:
                    self.place_hierarchy()
                    self._children_active = True
                    break

            if isinstance(widget, widgets.Panel):
                if widget._children_active:
                    self.place_hierarchy()
                    self._children_active = True

        super().absolute_placement(x, y)

        self._children = []

default_style2 = {
    'cornerradius':4,
    'borderwidth': 1,

    'background':'#EFEFEF',
    'bordercolor':'grey55',

    'gradial_orient': 'horizontal',
    'gradient_blend': 10,

    'header':{
        'cornerradius':4,
        'borderwidth': 1,

        'background':'dodgerblue2',
        'foreground':'white',
        'bordercolor':'dodgerblue4',

        'gradial_orient': 'horizontal',
        'gradient_blend': 10
    }
}

class HeaderPanel(Panel):
    def __init__(self, container, style=None, size=(400, 300), padding=(10, 10), header_height=20,
                 header_padding=(10, 10), header_anchor='midleft'):
        style = style if style else default_style2
        super().__init__(container, style, size, padding)

        header_style = style['header']
        header_size = [s-p for s, p in zip([size[0], header_height], header_padding)]
        self._header_label = widgets.Label(self.container, style=header_style, size=header_size, padding=header_padding,
                                     anchor=header_anchor)

    def absolute_placement(self, x, y):
        super().absolute_placement(x, y+self._header_label.rect.height-1)
        self._header_label.absolute_placement(x, y)