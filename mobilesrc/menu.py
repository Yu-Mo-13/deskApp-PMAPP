# coding: UTF-8

import PySimpleGUI as sg
from function.config import get_config

# ウィジェットのプロパティ
font = ("meiryo", 20)
size = (20, 3)

layout = [
    [sg.Text(get_config("MODULECONSTANT", "TITLE"), size=(20,2), font=font)],
    [sg.Button(get_config("MODULECONSTANT", "USERMASTER"), font=font, key="usermaster")],
    [sg.Button(get_config("MODULECONSTANT", "AUTHORITYMASTER"), font=font, key="authoritymaster")],
    [sg.Button(get_config("MODULECONSTANT", "ACCOUNTMASTER"), font=font, key="accountmaster")],
    [sg.Button("終了", font=font, key="cancel")]
]

window = sg.Window(get_config("MODULECONSTANT", "TITLE"), layout)

while True:
    event, value = window.read()

    if event == None:
        break

    if event == "usermaster":
        # ユーザーマスター画面呼び出し
        import userMasterList

    if event == "authoritymaster":
        # 権限マスター画面呼び出し
        import authorityMasterList

    if event == "accountmaster":
        # アカウントマスター画面呼び出し
        import accountMasterList

    if event == "cancel":
        break

window.close()