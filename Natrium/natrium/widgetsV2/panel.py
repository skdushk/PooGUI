from natrium import widgetsV2

default_style = {
    'cornerradius': 0,
    'borderwidth': 1,

    'inactive':
        {
            'body':
                {
                    'color': '#EFEFEF',
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

class Panel(widgetsV2.Widget):
    def __init__(self, container, style=None, size=(400, 300), padding=(10, 10)):

        style = style if style else default_style

        super().__init__(container, style, size, padding)
        self._isplaced = True
        self._previous_isplaced = True
        self._children_active = False

        self._children = []
        self._events = []

    def blit_wid(self, widget, position):
        self._children.append((widget, position))

    def place_hierarchy(self):
        pos = [self._style['borderwidth']] * 2
        self.fill((0, 0, 0, 0))
        self._hierarchy_rendering = [self._base_hierarchy_rendering[0].copy(),
                                     self._base_hierarchy_rendering[1].copy(),
                                     self._base_hierarchy_rendering[2].copy(),
                                     self._base_hierarchy_rendering[3].copy()]

        for widget, position in self._children:
            self._hierarchy_rendering[2].blit(widget, position)

        self._hierarchy_rendering[0].blit(self._hierarchy_rendering[2], [x//2-y//2 for x, y in zip(self.rect.size, self._base_size)])

        self.blit(self._hierarchy_rendering[3], (self._style['inactive']['shadow']['offsetx'], self._style['inactive']['shadow']['offsety']))
        self.blit(self._hierarchy_rendering[1], (0, 0))
        self.blit(self._hierarchy_rendering[0], pos)


    def trigger(self, events):
        self._events = events

    def absolute_placement(self, x, y):
        if not (self in Panel.placed_widgets):
            self.place_hierarchy()

        super().absolute_placement(x, y)

        self._children = []
