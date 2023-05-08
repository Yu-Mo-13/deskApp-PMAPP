# coding: UTF-8

import PySimpleGUI as sg
from log import Log as Log
from connectDatabase import ConnectDatabase as ConnectDatabase
from createExecDate import CreateExecuteDate as CreateExecuteDate
from manageApplicationLogic import ManageApplicationLogic as ManageAppLogic

# ウィジェットのプロパティ
font = ("meiryo", 20)
size = (20, 3)

font_popup = ("meiryo", 16)
title_popup_success = "アプリケーションマスタ管理画面"
title_popup = "エラー"

layout = [
    [sg.Text("アプリケーションマスタ", size=(20,2), font=font)],
    [sg.Text("アプリケーション名", font=font), sg.InputText(size=size, font=font, key="app_name")],
    [sg.Text("アカウント必要区分", font=font), 
     sg.Combo(values=["必要","不要"], default_value="必要", font=font, key="account_class", readonly=True)],
    [sg.Button("登録", font=font, key="regist"), sg.Button("検索", font=font, key="search"), 
    sg.Button("終了", font=font, key="cancel")]
]

window = sg.Window("パスワード管理アプリ", layout)

while True:
    event, value = window.read()

    insLog = Log()

    if event == None:
        break

    if event == 'regist':
        regFlg = False
        confirm_register = sg.PopupYesNo("アプリケーションを登録しますか。", font=font_popup, title=title_popup_success)
        if confirm_register == "Yes":
            appName = value["app_name"]
            if value["account_class"] == "必要":
                accountClas = '1'
            else:
                accountClas = '0'

            insCreateExecDate = CreateExecuteDate()
            registered_date = insCreateExecDate.createExecDate()

            if appName == "":
                insLog.writeLog('error', 'エラー：アプリ名未入力')
                sg.PopupOK("アプリ名が入力されていません。", font=font_popup, title=title_popup)
            
            else:
                # アプリケーションマスタ登録処理
                insManageApplication = ManageAppLogic('insert')
                regFlg = insManageApplication.regist(appName, accountClas, registered_date)
                if not(regFlg):
                    # 登録失敗時の処理
                    sg.Popup("パスワードの登録に失敗しました。", font=font_popup, title=title_popup_success)
                else:
                    # 登録成功時の処理
                    sg.Popup("パスワードをデータベースに登録しました。", font=font_popup, title=title_popup_success)

        elif confirm_register == "No":
            sg.Popup("パスワード登録処理をキャンセルします。", font=font_popup, title=title_popup_success)

        else:
            sg.Popup("パスワード登録処理をキャンセルします。", font=font_popup, title=title_popup_success)

    if event == 'search':
        appName = value["app_name"]
        if appName == "":
            insLog.writeLog('error', 'エラー：アプリ名未入力')
            sg.PopupOK("アプリ名が入力されていません。", font=font_popup, title=title_popup)
        else:
            insManageApplication = ManageAppLogic('select')
            accountClas = insManageApplication.search(appName)
            if (accountClas == '1'):
                window["account_class"].update('必要')
            elif (accountClas == '0'):
                window["account_class"].update('不要')
            else:
                insLog.writeLog('info', '該当データなし')
                sg.PopupOK("該当するデータがありませんでした。", font=font_popup, title=title_popup)

    if event == 'cancel':
        sg.PopupOK("アプリケーションを終了します。", font=font_popup, title=title_popup_success)
        break

window.close()