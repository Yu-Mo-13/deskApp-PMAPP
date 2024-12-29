# coding: UTF-8

import PySimpleGUI as sg
from function.config import get_config
from classes.subprocess import Subprocess

# ウィジェットのプロパティ
font = ("meiryo", 20)
size = (20, 3)

layout = [
    [sg.Text(get_config("MODULECONSTANT", "TITLE"), size=(20, 2), font=font)],
    [
        sg.Button(
            get_config("MODULECONSTANT", "PASSWORDDETAIL"), font=font, key="password"
        )
    ],
    [
        sg.Button(
            get_config("MODULECONSTANT", "APPLICATIONMASTERDETAIL"),
            font=font,
            key="applicationmaster",
        )
    ],
    [
        sg.Button(
            get_config("MODULECONSTANT", "ACCOUNTMASTERLIST"),
            font=font,
            key="accountmaster",
        )
    ],
    [
        sg.Button(
            get_config("MODULECONSTANT", "AUTOREGISTLIST"), font=font, key="autoregist"
        )
    ],
    [
        sg.Button(
            get_config("MODULECONSTANT", "PASSWORDWKDETAIL"),
            font=font,
            key="passwordwk",
        )
    ],
    [sg.Button(get_config("MODULECONSTANT", "CONVERTER"), font=font, key="converter")],
    [sg.Button("終了", font=font, key="cancel")],
]

window = sg.Window(get_config("MODULECONSTANT", "TITLE"), layout)

while True:
    event, value = window.read()

    if event == None:
        break

    if event == "password":
        subprocess = Subprocess(["python3", "src/managePassword.py"])
        subprocess.run()

    if event == "applicationmaster":
        subprocess = Subprocess(["python3", "src/manageApplication.py"])
        subprocess.run()

    if event == "accountmaster":
        subprocess = Subprocess(["python3", "src/accountMasterList.py"])
        subprocess.run()

    if event == "autoregist":
        subprocess = Subprocess(["python3", "src/manageAutoregistPassword.py"])
        subprocess.run()

    if event == "passwordwk":
        subprocess = Subprocess(["python3", "src/showPasswordWkList.py"])
        subprocess.run()

    if event == "converter":
        subprocess = Subprocess(["python3", "src/converter.py"])
        subprocess.run()

    if event == "cancel":
        break

window.close()
