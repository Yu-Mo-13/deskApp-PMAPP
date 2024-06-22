# coding: UTF-8

import PySimpleGUI as sg
from classes.log import Log as Log
from classes.curl import Curl as Curl
from function.config import get_config
import function.const as CONST

# ウィジェットのプロパティ
font = ("meiryo", 20)
size = (20, 3)

font_popup = ("meiryo", 16)
title_popup_success = get_config("MODULECONSTANT", "APPLICATIONMASTERDETAIL")
title_popup = get_config("MODULECONSTANT", "ERRORTITLE")

# 現在表示されているアプリケーション情報
applicationDetail = {
    "no": 0,
    "name": "",
    "accountclass": "",
    "noticeclass": "",
    "registered_date": ""
}

layout = [
    [sg.Text(get_config("MODULECONSTANT", "APPLICATIONMASTERDETAIL"), size=(20,2), font=font)],
    [sg.Text("アプリケーション名", font=font), sg.InputText(size=size, font=font, key="app_name")],
    [sg.Text("アカウント必要区分", font=font), 
     sg.Combo(values=["必要","不要"], default_value="必要", font=font, key="account_class", readonly=True)],
    [sg.Text("パスワード定期変更区分", font=font), 
     sg.Combo(values=["必要","不要"], default_value="必要", font=font, key="notice_class", readonly=True)],
    [sg.Button("登録", font=font, key="regist"), sg.Button("検索", font=font, key="search"), 
    sg.Button("終了", font=font, key="cancel")]
]

window = sg.Window(get_config("MODULECONSTANT", "TITLE"), layout)

while True:
    event, value = window.read()
    insLog = Log()

    if event == None:
        break

    if event == 'regist':
        confirm_register = sg.PopupYesNo("アプリケーションを登録しますか。", font=font_popup, title=title_popup_success)
        if confirm_register == "Yes":
            insCurl = Curl(get_config("CURLURL", "ROOTURL") + get_config("CURLURL", "APPLICATIONLISTURL"))
            appName = value["app_name"]
            accountClas = CONST.NeedAccount if value["account_class"] == "必要" else CONST.NoNeedAccount
            # Issue21: パスワード変更通知(パスワード定期変更区分の追加)
            noticeClas = CONST.NeedNotice if value["notice_class"] == "必要" else CONST.NoNeedNotice

            if appName == "":
                insLog.write('error', 'エラー：アプリ名未入力')
                sg.PopupOK("アプリ名が入力されていません。", font=font_popup, title=title_popup)
            
            else:
                # アプリケーションマスタ登録処理
                try:
                    if applicationDetail["no"] == 0:
                        # 登録処理
                        insCurl.post(f"create?name={appName}&accountclass={accountClas}&noticeclass={noticeClas}")
                    else:
                        # 更新処理
                        postNo = str(applicationDetail["no"])
                        insCurl.post(f"update?no={postNo}&name={appName}&accountclass={accountClas}&noticeclass={noticeClas}")
                    
                    sg.Popup("アプリケーションをデータベースに登録しました。", font=font_popup, title=title_popup_success)

                    # データのリセット
                    applicationDetail["no"] = 0
                
                except Exception as e:
                    insLog.write("error", str(e))
                    sg.Popup("アプリケーションの登録に失敗しました。", font=font_popup, title=title_popup_success)

        elif confirm_register == "No":
            sg.Popup("パスワード登録処理をキャンセルします。", font=font_popup, title=title_popup_success)

        else:
            sg.Popup("パスワード登録処理をキャンセルします。", font=font_popup, title=title_popup_success)

    if event == 'search':
        appName = value["app_name"]
        insCurl = Curl(f"{get_config('CURLURL', 'ROOTURL')}{get_config('CURLURL', 'APPLICATIONLISTURL')}search/app={appName}")
        if appName == "":
            insLog.write('error', 'エラー：アプリ名未入力')
            sg.PopupOK("アプリ名が入力されていません。", font=font_popup, title=title_popup)
        else:
            try:
                applicationDetail = insCurl.get()
                accountClas = applicationDetail["accountclas"]
                if (accountClas == CONST.NeedAccount):
                    window["account_class"].update('必要')
                elif (accountClas == CONST.NoNeedAccount):
                    window["account_class"].update('不要')
                
                # Issue21: パスワード変更通知(パスワード定期変更区分の追加)
                noticeClas = applicationDetail["noticeclas"]
                if (noticeClas == CONST.NeedNotice):
                    window["notice_class"].update('必要')
                elif (noticeClas == CONST.NoNeedNotice):
                    window["notice_class"].update('不要')

            except Exception as e:
                    if str(e.msg) == "Expecting value":
                        insLog.write("error", "検索結果なし")
                        sg.PopupOK("アプリケーションが見つかりませんでした。", font=font_popup, title=title_popup)
                    else:
                        insLog.write("error", str(e))
                        sg.PopupOK("アプリケーションの取得に失敗しました。", font=font_popup, title=title_popup)

    if event == 'cancel':
        sg.PopupOK("アプリケーションを終了します。", font=font_popup, title=title_popup_success)
        break

window.close()