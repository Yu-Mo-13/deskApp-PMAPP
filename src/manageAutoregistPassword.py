# coding: UTF-8

import PySimpleGUI as sg
from function.config import get_config
from classes.curl import Curl
from classes.log import Log
from classes.encryption import Encryption
from classes.registAction import RegistAction as RegistAction

# コマンドラインの引数(固定値)
create_mode = "0"

# ウィジェットのプロパティ
font = ("meiryo", 20)
font_popup = ("meiryo", 16)
size = (20, 2)
list_size = (20, 1)
row=0

insLog = Log()
insEncryption = Encryption()

# ユーザー一覧を取得
insCurl = Curl(get_config("CURLURL", "ROOTURL") + get_config("CURLURL", "AUTOREGISTURL"))

try:
    autoregistList = insCurl.get()
except Exception as e:
    insLog.write("error", str(e))
    autoregistList = {}
    sg.Popup("仮登録パスワード一覧の取得に失敗しました。", font=font, title=get_config("MODULECONSTANT", "AUTOREGISTLIST"))

# ヘッダー部のレイアウト
layout = [
    [sg.Text(get_config("MODULECONSTANT", "AUTOREGISTLIST"), size=size, font=font)],
    [sg.Text("アプリ名", font=font, size=list_size),
     sg.Text("アカウント名", font=font, size=list_size),
     sg.Text("パスワード", font=font, size=list_size)]
]

# ユーザー一覧のレイアウト
# read_only=Trueのテキストボックスで表示する
for ar in autoregistList:
    row += 1
    layout.append([sg.InputText(size=list_size, font=font, key="app" + str(row), default_text=ar["app"], disabled=True),
                   sg.InputText(size=list_size, font=font, key="other_info" + str(row), default_text=ar["other_info"], disabled=True),
                   sg.InputText(size=list_size, font=font, key="pwd" + str(row), default_text=insEncryption.decrypt(ar["pwd"]), disabled=True, password_char="*"),
                   sg.Button("本登録", font=font, key="regist" + str(row))])
    
# フッター部のレイアウト
layout.append([sg.Button("終了", font=font, key="cancel")])

window = sg.Window(get_config("MODULECONSTANT", "AUTOREGISTLIST"), layout)

while True:
    event, value = window.read()

    if event == None:
        break

    if event.startswith("regist"):
        confirm_register = sg.PopupYesNo("パスワードを本登録しますか。", font=font_popup, title=get_config("MODULECONSTANT", "TITLE"))
        # eventから登録ボタンの番号を取得
        if confirm_register == "Yes":
            exec_row = event.replace("regist", "")
            uuid = autoregistList[int(exec_row) - 1]["uuid"]
            pwd = value["pwd" + exec_row]
            app = value["app" + exec_row]
            other_info = value["other_info" + exec_row]

            insAction = RegistAction(pwd, app, other_info)
            result = insAction.execute()

            if not(result[0]):
                sg.PopupOK(result[1], font=font_popup, title=get_config("MODULECONSTANT", "ERRORTITLE"))

            else:
                try:
                    # 登録したデータを削除
                    insCurl = Curl(get_config("CURLURL", "ROOTURL") + get_config("CURLURL", "AUTOREGISTURL"))
                    insCurl.post(f"delete/uuid={uuid}")
                    # 登録成功時の処理
                    sg.Popup(result[1], font=font_popup, title=get_config("MODULECONSTANT", "AUTOREGISTLIST"))
                except Exception as e:
                    insLog.write("error", str(e))
                    sg.Popup("本登録に失敗しました。", font=font_popup, title=get_config("MODULECONSTANT", "AUTOREGISTLIST"))

    if event == "cancel":
        sg.PopupOK("アプリケーションを終了します。", font=font_popup, title=get_config("MODULECONSTANT", "TITLE"))
        break

window.close()