# coding: UTF-8

import PySimpleGUI as sg
from function.config import get_config
from classes.curl import Curl
import classes.subprocess as subprocess
from classes.log import Log

# ウィジェットのプロパティ
font = ("meiryo", 20)
size = (20, 2)
list_size_app = (15, 1)
list_size_account = (30, 1)
row=0

# ログ出力オブジェクト
insLog = Log()

# アカウント一覧を取得
insCurl = Curl(get_config("CURLURL", "ROOTURL") + get_config("CURLURL", "ACCOUNTLISTURL"))

try:
    accountList = insCurl.get()
except Exception as e:
    accountList = []
    insLog.write("error", e)
    sg.Popup("アカウント一覧の取得に失敗しました。", font=font, title=get_config("MODULECONSTANT", "ACCOUNTMASTERLIST"))

# ヘッダー部のレイアウト
layout = [
    [sg.Text(get_config("MODULECONSTANT", "ACCOUNTMASTERLIST"), size=size, font=font)],
    [sg.Button("新規登録", font=font, key="regist")],
    [sg.Text("アプリ名", font=font, size=list_size_app), sg.Text("アカウント", font=font, size=list_size_app)]
]
# アカウント一覧のレイアウト
# ラベルで表示する
for account in accountList:
    row += 1
    layout.append([sg.InputText(size=list_size_app, font=font, key="app" + str(row), default_text=account["app"], disabled=True),
                   sg.InputText(size=list_size_account, font=font, key="account" + str(row), default_text=account["account"], disabled=True),
                   sg.Button("削除", font=font, key="delete" + str(row))])

# フッター部のレイアウト
layout.append([sg.Button("終了", font=font, key="cancel")])

window = sg.Window(get_config("MODULECONSTANT", "ACCOUNTMASTERLIST"), layout)

while True:
    event, value = window.read()
    insSubprocess = subprocess.Subprocess(["python3", "accountMasterDetail.py"])

    if event == None:
        break

    if event == "regist":
        insSubprocess.run_async()
        break

    if event.startswith("delete"):
        # eventから登録ボタンの番号を取得
        exec_row = event.replace("delete", "")
        app = value["app" + exec_row]
        account = value["account" + exec_row]
        message_delete = sg.PopupYesNo("アカウントを削除しますか。", font=font, title=get_config("MODULECONSTANT", "ACCOUNTMASTERLIST"))
        if message_delete == "Yes":
            # 削除処理
            try:
                insCurl.post({"app": app, "account": account}, "delete/app=" + app + "/account=" + account)
            except Exception as e:
                pass

            sg.Popup("アカウントの削除が完了しました。一覧の表示は更新されません。", font=font, title=get_config("MODULECONSTANT", "ACCOUNTMASTERLIST"))

    if event == "cancel":
        break

window.close()