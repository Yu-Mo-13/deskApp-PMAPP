# coding: UTF-8

import PySimpleGUI as sg
from function.config import get_config
from classes.connectDatabase import ConnectDatabase

# ウィジェットのプロパティ
font = ("meiryo", 20)
size = (20, 3)

# ヘッダー部のレイアウト
layout = [
    [sg.Text(get_config("MODULECONSTANT", "ACCOUNTMASTERLIST"), size=(20,2), font=font)]
]

# アカウント一覧を取得
insConnectDatabase = ConnectDatabase()
insConnectDatabase.make_connection()

# フッター部のレイアウト
layout.append([sg.Button("終了", font=font, key="cancel")])

window = sg.Window(get_config("MODULECONSTANT", "ACCOUNTMASTERLIST"), layout)

while True:
    event, value = window.read()

    if event == None:
        break

    if event == "cancel":
        break

window.close()