# coding: UTF-8

import PySimpleGUI as sg
from function.config import get_config
from classes.curl import Curl
from classes.subprocess import Subprocess

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
    subprocess = Subprocess(["python3", "src/accountMasterList.py"])

    if event == None:
        break

    if event == "regist":
        # 登録処理
        app = value["app"]
        account = value["account"]
        curl = Curl(get_config("CURLURL", "ROOTURL") + get_config("CURLURL", "ACCOUNTLISTURL"))
        curl.post("create/app=" + app + "/account=" + account)
        sg.Popup("アカウントの登録が完了しました。", font=font, title=get_config("MODULECONSTANT", "ACCOUNTMASTERDETAIL"))
        subprocess.run_async()
        break

    if event == "cancel":
        subprocess.run_async()
        break

window.close()