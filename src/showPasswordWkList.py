# coding: UTF-8

import PySimpleGUI as sg
from passwordWk import PasswordWk as PasswordWk
from registAction import RegistAction as RegistAction
from log import Log as Log

# ウィジェットのプロパティ
font = ("meiryo", 20)
size = (20, 3)

font_popup = ("meiryo", 16)
title_popup_success = "パスワード管理アプリ"
title_popup = "エラー"

layout = [
    [sg.Text("未登録パスワード一覧", size=size, font=font)],
]
for row in range(5):
    layout.append([sg.Text("パスワード" + str(row + 1), font=font), sg.InputText(size=size, font=font, key="password" + str(row + 1)),
                    sg.Text("アプリ名" + str(row + 1), font=font), sg.InputText(size=size, font=font, key="application" + str(row + 1)),
                    sg.Text("アカウント" + str(row + 1), font=font), sg.InputText(size=size, font=font, key="other_info" + str(row + 1)),
                    sg.Text("登録日" + str(row + 1), font=font), sg.InputText(size=size, font=font, key="registered_date" + str(row + 1)),
                    sg.Button("登録", font=font, key="regist" + str(row + 1))])
    
layout.append([sg.Button("取得", font=font, key="get"),sg.Button("終了", font=font, key="quit")])

window = sg.Window("パスワード管理アプリ", layout)

while True:
    event, value = window.read()
    insLog = Log()
    if event == None:
        break

    if event.startswith("regist"):
        # eventから登録ボタンの番号を取得
        exec_row = event.replace("regist", "")
        pwd = value["password" + exec_row]
        app = value["application" + exec_row]
        other_info = value["other_info" + exec_row]
        registered_date = value["registered_date" + exec_row]

        if not(pwd) or not(app) or not(other_info) or not(registered_date):
            sg.PopupOK("未出力項目があります。", font=font_popup, title=title_popup)
        
        else:
            message_regist = sg.PopupYesNo("パスワードを登録しますか。", font=font_popup, title=title_popup_success)
            if message_regist == "Yes":
                # 登録処理
                insAction = RegistAction(pwd, app, other_info, registered_date)
                result = insAction.execute()

                if not(result[0]):
                    sg.Popup(result[1], font=font_popup, title=title_popup_success)
                else:
                    insPasswordWk = PasswordWk('delete')
                    insPasswordWk.delete(pwd, app, other_info)
                    # 登録成功時の処理
                    sg.Popup(result[1], font=font_popup, title=title_popup_success)

    if event == "get":
        try:
            # 入力欄をクリア
            for row in range(5):
                window["password" + str(row + 1)].update('')
                window["application" + str(row + 1)].update('')
                window["other_info" + str(row + 1)].update('')
                window["registered_date" + str(row + 1)].update('')

            # 取得処理
            insPasswordWk = PasswordWk('select')
            result = insPasswordWk.selectAll()

            if len(result) > 5:
                exec_length = 5
            else:
                exec_length = len(result)

            for row in range(exec_length):
                window["password" + str(row + 1)].update(result[row]['pwd'])
                window["application" + str(row + 1)].update(result[row]['app'])
                window["other_info" + str(row + 1)].update(result[row]['other_info'])
                window["registered_date" + str(row + 1)].update(result[row]['registered_date'])
                insLog.write('info', result[row]['app'])
                
        except TypeError as e:
            insLog.write('error', '未登録パスワードなし')
            sg.PopupOK('未登録パスワードはありません。', font=font_popup, title=title_popup_success)

    # 終了ボタン
    if event == "quit":
        message_quit = sg.PopupYesNo("この画面を閉じますか。", font=font_popup, title=title_popup_success)
        if message_quit == "Yes":
            break