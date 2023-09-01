import pygame
from natrium import widgets, widgetsV2

def trigger(events, mpos, mprd):
    for widget in widgetsV2.Widget.interactives:
        listen(widget, events, mpos, mprd)

    widgetsV2.Widget.reset()

def listen(widget:widgets.Widget, events, mpos, mprd):
    params = []

    if isinstance(widget, (widgetsV2.Button, widgetsV2.Entry, widgetsV2.ToggleButton,
                           widgetsV2.RadioButton, widgets.Spinbox, widgetsV2.Panel)):
        params.append(events)

    if not (isinstance(widget, widgets.Panel) and not isinstance(widget, widgets.Listbox)):
        params.append(mpos)

    if isinstance(widget, (widgetsV2.Button, widgets.Spinbox)):
        params.append(mprd)

    widget.trigger(*params)