# coding: UTF-8

import PySimpleGUI as sg
from execDate import ExecuteDate as ExecuteDate
# 2023/06/25 add issue #7 ワークテーブルの参照を追加
from passwordWk import PasswordWk as PasswordWk
# アクションクラス呼び出し
from generateAction import GenerateAction as GenerateAction
from registAction import RegistAction as RegistAction
from searchAction import SearchAction as SearchAction

from showPasswordWkList import ShowPasswordWkList as WkList

# ウィジェットのプロパティ
font = ("meiryo", 20)
size = (20, 3)

font_popup = ("meiryo", 16)
title_popup_success = "パスワード管理アプリ"
title_popup = "エラー"

layout = [
    [sg.Text("パスワード管理アプリ", size=(20,2), font=font)],
    [sg.Text("パスワード", font=font), sg.InputText(size=size, font=font, key="password"), sg.Button("パスワード生成", font=font, key="generate")],
    [sg.Text("使用アプリ", font=font), sg.InputText(size=size, font=font, key="application")],
    [sg.Text("備　　　考", font=font), sg.InputText(size=size, font=font, key="other_info")],
    [sg.Text("パスワード桁数", font=font), sg.InputText(size=(size[0] - 10, size[1]), font=font, key="length")],
    [sg.Button("パスワード登録", font=font, key="register"), sg.Button("パスワード検索", font=font, key="search"),
    sg.Button("未登録パスワード一覧", font=font, key="work_list"), sg.Button("アプリ終了", font=font, key="cancel")]
]

window = sg.Window("パスワード管理アプリ", layout)

while True:
    event, value = window.read()
    # 2023/04/29 add ref: 20230429_PasswordEncryption

    if event == None:
        break

    if event == "generate":
        app = value["application"]
        other_info = value["other_info"]
        registered_date = ExecuteDate().get()
        # パスワード桁数をint型に変換
        intLength = value["length"]

        insAction = GenerateAction('', app, other_info, registered_date)
        result = insAction.execute(intLength)

        if result[0]:
            # パスワード入力欄にパスワードを表示
            window['password'].update(result[1])
        else:
            sg.PopupOK(result[1], font=font_popup, title=title_popup)

    if event == "register":
        confirm_register = sg.PopupYesNo("パスワードを登録しますか。", font=font_popup, title=title_popup_success)
        if confirm_register == "Yes":
            pwd = value["password"]
            app = value["application"]
            # 2023/2/12 備考を追加
            other_info = value["other_info"]
            registered_date = ExecuteDate().get()

            insAction = RegistAction(pwd, app, other_info, registered_date)
            result = insAction.execute()

            if not(result[0]):
                sg.PopupOK(result[1], font=font_popup, title=title_popup)

            else:
                insPasswordWk = PasswordWk('delete')
                insPasswordWk.delete(pwd, app, other_info)
                # 登録成功時の処理
                sg.Popup(result[1], font=font_popup, title=title_popup_success)
                    
        elif confirm_register == "No":
            sg.Popup("パスワード登録処理をキャンセルします。", font=font_popup, title=title_popup_success)

        else:
            sg.Popup("パスワード登録処理をキャンセルします。", font=font_popup, title=title_popup_success)

    if event == "search":
        app = value["application"]
        other_info = value["other_info"]
        pwd = ''

        insAction = SearchAction(pwd, app, other_info, '')
        result = insAction.execute()

        if not(result[0]):
            sg.PopupOK(result[1], font=font_popup, title=title_popup)

        else:
            # 管理画面のパスワード入力欄を更新
            window['password'].update(result[1])
    
    # 2023/07/10 add issue #14
    if event == "work_list":
        insWkList = WkList(font, size, font_popup, title_popup_success)
        insWkList.show()
 
    if event == "cancel":
        # 2023/06/25 add issue #7
        # ワークテーブルに1件でもデータが残っていたら、ワークテーブルのデータを全削除するかの確認を行う
        insPassword = PasswordWk('select')
        if insPassword.count() > 0:
            confirm_cancel = sg.PopupYesNo("ワークテーブルにデータが残っています。データを削除してアプリケーションを終了しますか。", font=font_popup, title=title_popup)
            if confirm_cancel == "Yes":
                PasswordWk('delete').deleteAll()
                sg.PopupOK("アプリケーションを終了します。", font=font_popup, title=title_popup_success)
                break
        else:
            sg.PopupOK("アプリケーションを終了します。", font=font_popup, title=title_popup_success)
            break

window.close()