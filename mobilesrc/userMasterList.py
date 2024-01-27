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
list_size_id = (3, 1)
list_size_engname = (15, 1)
list_size_jpnname = (20, 1)
row=0

insLog = Log()

# ユーザー一覧を取得
insCurl = Curl(get_config("CURLURL", "ROOTURL") + get_config("CURLURL", "USERLISTURL"))

try:
    userList = insCurl.get()
except Exception as e:
    insLog.write("error", str(e))
    userList = {}
    sg.Popup("ユーザーマスター一覧の取得に失敗しました。", font=font, title=get_config("MODULECONSTANT", "USERMASTERLIST"))

# ヘッダー部のレイアウト
layout = [
    [sg.Text(get_config("MODULECONSTANT", "USERMASTERLIST"), size=size, font=font)],
    [sg.Button("新規登録", font=font, key="regist")],
    [sg.Text("ID", font=font, size=list_size_id),
     sg.Text("ユーザー名(英)", font=font, size=list_size_engname),
     sg.Text("ユーザー名(日)", font=font, size=list_size_jpnname), sg.Text("  ", font=font)]
]

# ユーザー一覧のレイアウト
# read_only=Trueのテキストボックスで表示する
for user in userList:
    row += 1
    layout.append([sg.InputText(size=list_size_id, font=font, key="id" + str(row), default_text=user["id"], disabled=True),
                   sg.InputText(size=list_size_engname, font=font, key="engname" + str(row), default_text=user["engname"], disabled=True),
                   sg.InputText(size=list_size_jpnname, font=font, key="jpnname" + str(row), default_text=user["jpnname"], disabled=True),
                   sg.Button("詳細", font=font, key="detail" + str(row))])
    
# フッター部のレイアウト
layout.append([sg.Button("終了", font=font, key="cancel")])

window = sg.Window(get_config("MODULECONSTANT", "USERMASTERLIST"), layout)

while True:
    event, value = window.read()

    if event == None:
        break

    if event == "regist":
        subprocess.Subprocess(["python3", "userMasterDetail.py", create_mode]).run_async()
        break

    if event.startswith("detail"):
        # eventから登録ボタンの番号を取得
        exec_row = event.replace("detail", "")
        id = value["id" + exec_row]
        subprocess.Subprocess(["python3", "userMasterDetail.py", id]).run_async()
        break

    if event == "cancel":
        break

window.close()