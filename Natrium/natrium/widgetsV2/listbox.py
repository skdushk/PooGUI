from natrium import widgetsV2
import pygame

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
                    'blur': 10,
                    'offsetx': 10,
                    'offsety': 10,
                    'gradient_orient': 'vertical',
                    'gradient_blend': 10
                }

        },

    'option_button': {
            'uppercornerradius': 0,
            'lowercornerradius': 0,
            'cornerradius': 0,
            'borderwidth': 0,

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
                            'color': '#EFEFEF',
                            'gradient_orient': 'vertical',
                            'gradient_blend': 10
                        },

                    'border':
                        {
                            'color': 'dodgerblue',
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
                            'color': 'dodgerblue',
                            'gradient_orient': 'vertical',
                            'gradient_blend': 10
                        },

                    'border':
                        {
                            'color': 'dodgerblue2',
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
}

class Listbox(widgetsV2.Panel):
    def __init__(self, container, style=None, size=(140, 300), padding=(10, 10), options=None,
                 option_height=21, font=('gadugi', 12)):

        style = style if style else default_style

        box_style = {k:v for k, v in style.items() if 'option' not in k}
        option_style = style['option_button']

        for x in ['inactive', 'hover', 'active']:
            option_style[x]['shadow'] = {
                'color': (0, 0, 0, 0),
                'blur': 10,
                'offsetx': 10,
                'offsety': 10,
                'gradient_orient': 'vertical',
                'gradient_blend': 10
            }

        super().__init__(container, box_style, size, padding)

        self.options = options if options else ['Option1', 'Option2', 'Option3']
        self._option_widgets = []

        for i, option in enumerate(self.options):
            loop_style = option_style.copy()
            loop_style['cornerradius'] = option_style['uppercornerradius'] if not i else option_style['uppercornerradius']

            widget = widgetsV2.RadioButton(self, style=loop_style, size=[size[0] - 12, option_height],
                                         text=option, font=font, anchor='midleft', padding=(10, 0))
            self._option_widgets.append(widget)

        for widget in self._option_widgets:
            copy_list = self._option_widgets.copy()
            copy_list.remove(widget)
            widget.associate_with = copy_list

        self._option_height = option_height
        self.font = font

    def get_selected_option(self):
        selected = ""
        for widget in self._option_widgets:
            if widget._event_mode == 2:
                selected = widget.string
        return selected

    def clear_selected_option(self):
        for widget in self._option_widgets:
            if widget._event_mode == 2:
                widget._event_mode = 0

    def get_option_name(self, index):
        return self.options[index]

    def get_option_index(self, name):
        return self.options.index(name)

    def set_selected_option(self, index):
        self.clear_selected_option()
        self._option_widgets[index]._event_mode = 2

    def absolute_placement(self, x, y):
        for i, widget in enumerate(self._option_widgets):
            widget.absolute_placement(0, self._option_height*i)

        super().absolute_placement(x, y)
