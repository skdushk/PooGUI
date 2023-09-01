import natrium
from natrium import widgetsV2


window = natrium.display.Window(background='grey92', size=(800, 450))

panel = widgetsV2.Panel(container=window, size=(450, 295))

label = widgetsV2.Label(container=window, text='Label:')
entry = widgetsV2.Entry(container=window, placeholder_text="Entry", size=(190, 15))

label2 = widgetsV2.Label(container=window, text='Button:')
button = widgetsV2.Button(container=window, text="Button", command=lambda:print(window.get_rate()), anchor='center',
                        size=(85, 15))
button2 = widgetsV2.ToggleButton(container=window, text="Toggle", anchor='center', size=(85, 15))

label3 = widgetsV2.Label(container=window, text='Radio:')
radio = widgetsV2.RadioButton(container=window, text="Radio", anchor='center', size=(50, 15))
radio2 = widgetsV2.RadioButton(container=window, text="Radio", anchor='center', size=(50, 15))
radio3 = widgetsV2.RadioButton(container=window, text="Radio", anchor='center', size=(50, 15))

radio.associate_with = [radio2, radio3]
radio2.associate_with = [radio, radio3]
radio3.associate_with = [radio, radio2]

checkbox = widgetsV2.Checkbox(window)
checkbox1 = widgetsV2.Checkbox(window)
checkbox2 = widgetsV2.Checkbox(window)

listbox = widgetsV2.Listbox(container=panel, size=(140, 290), padding=(2, 2),
                          options=[f'Option{i+1}' for i in range(10)])
seperator = widgetsV2.Seperator(container=panel, length=297, orient='vertical', color='grey55')
label4 = widgetsV2.Label(container=panel, text="The selected option is: ", size=(300, 20), anchor='midleft')


while True:
    window.trigger()

    if label4.string != f'The selected option is: {listbox.get_selected_option()}':
        label4.string = f'The selected option is: {listbox.get_selected_option()}'

    label.absolute_placement(10, 16)
    entry.absolute_placement(60, 12)

    label2.absolute_placement(10, 56)
    button.absolute_placement(60, 52)
    button2.absolute_placement(165, 52)

    label3.absolute_placement(10, 96)
    radio.absolute_placement(60, 92)
    radio2.absolute_placement(130, 92)
    radio3.absolute_placement(200, 92)

    checkbox.absolute_placement(270, 12)
    checkbox1.absolute_placement(270, 52)
    checkbox2.absolute_placement(270, 92)

    listbox.absolute_placement(306, 0)
    seperator.absolute_placement(300, 1)
    label4.absolute_placement(10, 10)

    panel.absolute_placement(10, 132)


    window.refresh()
