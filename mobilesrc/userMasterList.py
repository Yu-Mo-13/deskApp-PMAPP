# coding: UTF-8

import PySimpleGUI as sg
from function.config import get_config

# ウィジェットのプロパティ
font = ("meiryo", 20)
size = (20, 3)

layout = [sg.Text(get_config("MODULECONSTANT", "USERMASTERLIST"), size=(20,2), font=font)]

window = sg.Window(get_config("MODULECONSTANT", "USERMASTERLIST"), layout)