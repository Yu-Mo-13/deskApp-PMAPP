# coding: UTF-8

import PySimpleGUI as sg
from classes.passwordWk import PasswordWk as PasswordWk
from classes.registAction import RegistAction as RegistAction
from classes.curl import Curl as Curl
from classes.log import Log as Log
from function.config import get_config

# ウィジェットのプロパティ
font = ("meiryo", 20)
size = (20, 3)

font_popup = ("meiryo", 16)
title_popup_success = get_config("MODULECONSTANT", "TITLE")
title_popup = get_config("MODULECONSTANT", "ERRORTITLE")

layout = [
    [sg.Text(get_config("MODULECONSTANT", "PASSWORDWKDETAIL"), size=size, font=font)],
]
for row in range(5):
    layout.append([sg.Text("パスワード" + str(row + 1), font=font), sg.InputText(size=size, font=font, key="password" + str(row + 1), disabled=True),
                    sg.Text("アプリ名" + str(row + 1), font=font), sg.InputText(size=size, font=font, key="application" + str(row + 1), disabled=True),
                    sg.Text("アカウント" + str(row + 1), font=font), sg.InputText(size=size, font=font, key="other_info" + str(row + 1), disabled=True),
                    sg.Button("登録", font=font, key="regist" + str(row + 1))])
    
layout.append([sg.Button("取得", font=font, key="get"),sg.Button("終了", font=font, key="quit")])

window = sg.Window("パスワード管理アプリ", layout)

while True:
    event, value = window.read()
    insLog = Log()
    if event == None:
        break

    if event.startswith("regist"):
        insCurl = Curl(f"{get_config('CURLURL', 'ROOTURL')}{get_config('CURLURL', 'PASSWORDURL')}")

        # eventから登録ボタンの番号を取得
        exec_row = event.replace("regist", "")
        pwd = value["password" + exec_row]
        app = value["application" + exec_row]
        other_info = value["other_info" + exec_row]

        if not(pwd) or not(app):
            sg.PopupOK("未出力項目があります。", font=font_popup, title=title_popup)
        
        else:
            message_regist = sg.PopupYesNo("パスワードを登録しますか。", font=font_popup, title=title_popup_success)
            if message_regist == "Yes":
                try:
                    # 登録処理
                    if not(other_info):
                        insCurl.post(f"create?pwd={pwd}&app={app}&other_info")
                    else:
                        insCurl.post(f"create?pwd={pwd}&app={app}&other_info={other_info}")

                    # Issue25: デスクトップアプリAPI移行
                    # ワークテーブルを削除する際のキー項目からパスワードを除外
                    # 一度パスワードを登録したパスワードのアプリのワークデータを残しておく必要は無い
                    insPasswordWk = PasswordWk()
                    insPasswordWk.delete(app, other_info)

                    sg.Popup("パスワードの登録が完了しました。", font=font_popup, title=title_popup_success)

                except Exception as e:
                    insLog.write('error', str(e))
                    sg.Popup("パスワードの登録に失敗しました。", font=font_popup, title=title_popup)

    if event == "get":
        try:
            # 入力欄をクリア
            for row in range(5):
                window["password" + str(row + 1)].update('')
                window["application" + str(row + 1)].update('')
                window["other_info" + str(row + 1)].update('')

            # 未登録パスワード一覧を取得
            passwordwkList = PasswordWk().selectAll()

            if len(passwordwkList) == 0:
                insLog.write('info', '未登録パスワードなし')
                exec_length = 0
                sg.PopupOK('未登録パスワードはありません。', font=font_popup, title=title_popup_success)
            elif len(passwordwkList) > 5:
                exec_length = 5
            else:
                exec_length = len(passwordwkList)

            for row in range(exec_length):
                window["password" + str(row + 1)].update(passwordwkList[row]['pwd'])
                window["application" + str(row + 1)].update(passwordwkList[row]['app'])
                window["other_info" + str(row + 1)].update(passwordwkList[row]['other_info'])
                insLog.write('info', passwordwkList[row]['app'])
                
        except TypeError as e:
            insLog.write('error', '未登録パスワードなし')
            sg.PopupOK('未登録パスワードの取得に失敗しました。', font=font_popup, title=title_popup_success)

    # 終了ボタン
    if event == "quit":
        message_quit = sg.PopupYesNo("この画面を閉じますか。", font=font_popup, title=title_popup_success)
        if message_quit == "Yes":
            break