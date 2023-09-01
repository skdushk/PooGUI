import natrium
from glob_style import box_label

def increase_string():
    count_label.string = str(int(count_label.string) + 1)

def decrease_string():
    count_label.string = str(int(count_label.string) - 1)

def reset_string():
    count_label.string = "0"

disp = natrium.display.Window((200, 120), '#FAFAFA', resizable=False, title='Counter')

count_label = natrium.widgetsV2.Entry(disp, placeholder_text="0", font=('gadugi', 40), padding=(10, 10),
                                      size=(100, 96), anchor='center')
increase = natrium.widgetsV2.Button(disp, text='+', size=(60, 22), anchor='center', font=('gadugi', 16),
                                    command=increase_string)

decrease = natrium.widgetsV2.Button(disp, text='-', size=(60, 22), anchor='center', font=('gadugi', 16),
                                    command=decrease_string)

reset = natrium.widgetsV2.Button(disp, text='Reset', size=(60, 22), anchor='center', font=('gadugi', 16),
                                 command=reset_string)

while True:
    disp.trigger()

    count_label.absolute_placement(5, 5)
    increase.absolute_placement(120, 5)
    decrease.absolute_placement(120, 42)
    reset.absolute_placement(120, 79)

    disp.refresh()