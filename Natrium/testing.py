from natrium import display as natdisp
from natrium import widgets

window = natdisp.Window(size=(900, 500), background='#EFEFEF', title='Password Generator',
                        icon='L:\malek\programs\python\Password Generator 2\img\icon.png',
                        resizable=False)

label = widgets.Label(container=window, text='Label:')
entry = widgets.InputBox(container=window, placeholder_text="Entry")

label2 = widgets.Label(container=window, text='Button:')
button = widgets.Button(container=window, text="Button", command=lambda:print(window.get_rate()), anchor='center',
                        size=(140, 20))
button2 = widgets.ToggleButton(container=window, text="Toggle", anchor='center', size=(140, 20))

label3 = widgets.Label(container=window, text='Radio:')
radio = widgets.RadioButton(container=window, text="Radio", anchor='center', size=(140, 20))
radio2 = widgets.RadioButton(container=window, text="Radio", anchor='center', size=(140, 20))

radio.associate_with = [radio2]
radio2.associate_with = [radio]

panel = widgets.Panel(container=window, size=(450, 300))
listbox = widgets.Listbox(container=panel, size=(140, 296), padding=(2, 2),
                          options=[f'Option{i+1}' for i in range(10)])
label4 = widgets.Label(container=panel, text="The selected option is: ", size=(240, 100))
spinbox = widgets.Spinbox(container=panel, size=(250, 20))

seperator = widgets.Seperator(container=panel, length=297, orient='vertical', color='grey55')

checkbox = widgets.Checkbox(window)
checkbox1 = widgets.Checkbox(window)
checkbox2 = widgets.Checkbox(window)

label5 = widgets.Label(container=window, text='Checkbox1')
label6 = widgets.Label(container=window, text='Checkbox2')
label7 = widgets.Label(container=window, text='Checkbox3')

while True:
    window.trigger()

    if label4.string != f'The selected option is: {listbox.get_selected_option()}':
        label4.string = f'The selected option is: {listbox.get_selected_option()}'

    label.absolute_placement(10, 12)
    entry.absolute_placement(70, 12)

    label2.absolute_placement(10, 52)
    button.absolute_placement(70, 52)
    button2.absolute_placement(230, 52)

    label3.absolute_placement(10, 92)
    radio.absolute_placement(70, 92)
    radio2.absolute_placement(230, 92)

    seperator.absolute_placement(300, 1)
    label4.absolute_placement(0, 0)
    listbox.absolute_placement(306, 0)
    spinbox.absolute_placement(0, 40)
    panel.absolute_placement(10, 142)

    checkbox.absolute_placement(400, 12)
    checkbox1.absolute_placement(400, 52)
    checkbox2.absolute_placement(400, 92)

    label5.absolute_placement(434, 12)
    label6.absolute_placement(434, 52)
    label7.absolute_placement(434, 92)

    window.refresh()