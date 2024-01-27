# coding: UTF-8

import PySimpleGUI as sg
from function.config import get_config
from classes.curl import Curl
import classes.subprocess as subprocess
from classes.log import Log

# コマンドラインの引数(固定値)
create_mode = "0"

# ウィジェットのプロパティ
font = ("meiryo", 20)
size = (20, 2)
list_size_code = (5, 1)
list_size_name = (15, 1)
list_size_admin = (2, 1)
row=0

insLog = Log()

# 権限一覧を取得
insCurl = Curl(get_config("CURLURL", "ROOTURL") + get_config("CURLURL", "AUTHORITYLISTURL"))
try:
    authorityList = insCurl.get()
except Exception as e:
    insLog.write("error", str(e))
    authorityList = {}
    sg.Popup("権限マスター一覧の取得に失敗しました。", font=font, title=get_config("MODULECONSTANT", "AUTHORITYMASTERLIST"))

# ヘッダー部のレイアウト
layout = [
    [sg.Text(get_config("MODULECONSTANT", "AUTHORITYMASTERLIST"), size=size, font=font)],
    [sg.Button("新規登録", font=font, key="regist")],
    [sg.Text("コード", font=font, size=list_size_code), sg.Text("権限名", font=font, size=list_size_name), 
     sg.Text("  ", font=font)]
]

# 権限一覧のレイアウト
# read_only=Trueのテキストボックスで表示する
for authority in authorityList:
    is_admin = ""
    row += 1
    if (authority["adminflg"] == "1"):
        is_admin = "権"
    layout.append([sg.InputText(size=list_size_code, font=font, key="code" + str(row), default_text=authority["cd"], disabled=True),
                   sg.InputText(size=list_size_name, font=font, key="name" + str(row), default_text=authority["name"], disabled=True),
                   sg.InputText(size=list_size_admin, font=font, key="admin" + str(row), default_text=is_admin, disabled=True),
                   sg.Button("詳細", font=font, key="detail" + str(row))])

# フッター部のレイアウト
layout.append([sg.Button("終了", font=font, key="cancel")])

window = sg.Window(get_config("MODULECONSTANT", "AUTHORITYMASTERLIST"), layout)

while True:
    event, value = window.read()

    if event == None:
        break

    if event == "regist":
        subprocess.Subprocess(["python3", "authorityMasterDetail.py", create_mode]).run_async()
        break

    if event.startswith("detail"):
        # eventから登録ボタンの番号を取得
        exec_row = event.replace("detail", "")
        code = value["code" + exec_row]
        subprocess.Subprocess(["python3", "authorityMasterDetail.py", code]).run_async()
        break

    if event == "cancel":
        break

window.close()