import natrium
import glob_style

def change_val(val):
    selection_num[0] = val

root = natrium.display.Window((600, 200), '#F0F0F0', title="BasicForm", resizable=False)

selection_panel = natrium.widgets.Panel(root, size=(122, 177), style=glob_style.dark_left_panel)
login_button = natrium.widgets.RadioButton(selection_panel, text='Log-in', anchor='center', size=(100, 20),
                                           style=glob_style.metal_button)

signup_button = natrium.widgets.RadioButton(selection_panel, text='Sign-up', anchor='center',
                                            size=(100, 20), style=glob_style.metal_button)

login_button.associate_with = [signup_button]
signup_button.associate_with = [login_button]
login_button.active = True

selection_num = [0]
login_panel = natrium.widgets.Panel(root, size=(459, 177), style=glob_style.right_panel)
signup_panel = natrium.widgets.Panel(root, size=(459, 177), style=glob_style.right_panel)

login_label1 = natrium.widgets.Label(login_panel, text="Username:")
login_user_entry = natrium.widgets.InputBox(login_panel)

login_label2 = natrium.widgets.Label(login_panel, text="Password:")
login_pass_entry = natrium.widgets.InputBox(login_panel, show_characters='*')

login_submit = natrium.widgets.Button(login_panel, text="Submit", anchor='center', size=(150, 20),
                                      style=glob_style.emerald_button)


signup_label1 = natrium.widgets.Label(signup_panel, text="Username:")
signup_user_entry = natrium.widgets.InputBox(signup_panel)

signup_label2 = natrium.widgets.Label(signup_panel, text="Password:")
signup_pass_entry = natrium.widgets.InputBox(signup_panel, show_characters='*')

signup_submit = natrium.widgets.Button(signup_panel, text="Submit", anchor='center', size=(150, 20),
                                       style=glob_style.emerald_button)

while True:
    root.trigger()

    login_button.absolute_placement(0, 0)
    signup_button.absolute_placement(0, 34)

    selection_panel.absolute_placement(5, 5)

    login_label1.absolute_placement(10, 10)
    login_user_entry.absolute_placement(100, 10)

    login_label2.absolute_placement(10, 50)
    login_pass_entry.absolute_placement(100, 50)

    login_submit.absolute_placement(176, 90)

    signup_label1.absolute_placement(10, 10)
    signup_user_entry.absolute_placement(100, 10)

    signup_label2.absolute_placement(10, 50)
    signup_pass_entry.absolute_placement(100, 50)

    signup_submit.absolute_placement(176, 90)

    if signup_button.active:
        signup_panel.absolute_placement(125, 5)
    else:
        login_panel.absolute_placement(125, 5)

    root.refresh()
