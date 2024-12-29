# coding: UTF-8

import PySimpleGUI as sg
from function.config import get_config
from classes.log import Log
from classes.encryption import Encryption
from classes.registAction import RegistAction as RegistAction
from classes.autoregist import AutoRegist as AutoRegist

# コマンドラインの引数(固定値)
create_mode = "0"

# ウィジェットのプロパティ
font = ("meiryo", 20)
font_popup = ("meiryo", 16)
size = (20, 2)
list_size = (20, 1)
row=0

log = Log()
encryption = Encryption()
autoregist = AutoRegist()

try:
    autoregist_list = autoregist.search()
except Exception as e:
    log.write("error", str(e))
    autoregist_list = {}
    sg.Popup("仮登録パスワード一覧の取得に失敗しました。",
             font=font, title=get_config("MODULECONSTANT", "AUTOREGISTLIST"))

# ヘッダー部のレイアウト
layout = [
    [sg.Text(get_config("MODULECONSTANT", "AUTOREGISTLIST"), size=size, font=font)],
    [sg.Text("アプリ名", font=font, size=list_size),
     sg.Text("アカウント名", font=font, size=list_size),
     sg.Text("パスワード", font=font, size=list_size)]
]

# read_only=Trueのテキストボックスで表示する
for autoregist in autoregist_list:
    row += 1
    layout.append([sg.InputText(size=list_size, font=font,
                                key="app" + str(row),
                                default_text=autoregist["app"], disabled=True),
                   sg.InputText(size=list_size, font=font,
                                key="other_info" + str(row),
                                default_text=autoregist["other_info"],
                                disabled=True),
                   sg.InputText(size=list_size, font=font,
                                key="pwd" + str(row),
                                default_text=encryption.decrypt(autoregist["pwd"]),
                                disabled=True, password_char="*"),
                   sg.Button("本登録", font=font, key="regist" + str(row))])
    
# フッター部のレイアウト
layout.append([sg.Button("終了", font=font, key="cancel")])

window = sg.Window(get_config("MODULECONSTANT", "AUTOREGISTLIST"), layout)

while True:
    event, value = window.read()

    if event == None:
        break

    if event.startswith("regist"):
        confirm_regist = sg.PopupYesNo("パスワードを本登録しますか。",
                                       font=font_popup,
                                       title=get_config("MODULECONSTANT", "TITLE"))
        # eventから登録ボタンの番号を取得
        if confirm_regist == "Yes":
            exec_row = event.replace("regist", "")
            uuid = autoregist_list[int(exec_row) - 1]["uuid"]
            pwd = value["pwd" + exec_row]
            app = value["app" + exec_row]
            other_info = value["other_info" + exec_row]

            action = RegistAction(pwd, app, other_info)
            result = action.execute()

            if not(result[0]):
                sg.PopupOK(result[1], font=font_popup,
                           title=get_config("MODULECONSTANT", "ERRORTITLE"))

            else:
                try:
                    result = autoregist.delete(uuid)

                    if not(result):
                        sg.Popup("本登録に失敗しました。",
                                 font=font_popup,
                                 title=get_config("MODULECONSTANT", "AUTOREGISTLIST"))
                    else:
                        sg.Popup(result[1], font=font_popup,
                                 title=get_config("MODULECONSTANT", "AUTOREGISTLIST"))

                except Exception as e:
                    log.write("error", str(e))
                    sg.Popup("本登録に失敗しました。", font=font_popup,
                             title=get_config("MODULECONSTANT", "AUTOREGISTLIST"))

    if event == "cancel":
        sg.PopupOK("アプリケーションを終了します。", font=font_popup,
                   title=get_config("MODULECONSTANT", "TITLE"))
        break

window.close()