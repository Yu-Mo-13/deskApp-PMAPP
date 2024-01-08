# coding: UTF-8

import PySimpleGUI as sg
from function.config import get_config
from classes.curl import Curl

# ウィジェットのプロパティ
font = ("meiryo", 20)
size = (25, 2)
size_column = (10, 1)

# ヘッダー部のレイアウト
layout = [
    [sg.Text(get_config("MODULECONSTANT", "ACCOUNTMASTERDETAIL"), size=size, font=font)],
    [sg.Text("アプリ名", font=font, size=size_column), sg.InputText(size=size, font=font, key="app")],
    [sg.Text("アカウント", font=font, size=size_column), sg.InputText(size=size, font=font, key="account")],
    [sg.Button("登録", font=font, key="regist"),sg.Button("終了", font=font, key="cancel")]
]

window = sg.Window(get_config("MODULECONSTANT", "ACCOUNTMASTERDETAIL"), layout)

while True:
    event, value = window.read()

    if event == None:
        break

    if event == "regist":
        # 登録処理
        app = value["app"]
        account = value["account"]
        insCurl = Curl(get_config("CURLURL", "ROOTURL") + get_config("CURLURL", "ACCOUNTLISTURL"))
        insCurl.post({"app": app, "account": account}, "create/app=" + app + "/account=" + account)
        sg.Popup("アカウントの登録が完了しました。一覧の表示は更新されません。", font=font, title=get_config("MODULECONSTANT", "ACCOUNTMASTERDETAIL"))

    if event == "cancel":
        break

window.close()