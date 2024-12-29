# coding: UTF-8

import PySimpleGUI as sg
from classes.application import Application as Application
from classes.log import Log as Log
from classes.curl import Curl as Curl
from function.config import get_config
import function.const as CONST

# ウィジェットのプロパティ
font = ("meiryo", 20)
size = (20, 3)
size_small = (2, 3)

font_popup = ("meiryo", 16)
title_popup_success = get_config("MODULECONSTANT", "APPLICATIONMASTERDETAIL")
title_popup = get_config("MODULECONSTANT", "ERRORTITLE")

# 現在表示されているアプリケーション情報
application_detail = {
    "no": 0,
    "name": "",
    "accountclass": "",
    "noticeclass": "",
    "markclass": "",
    "autosize": "",
    "registered_date": ""
}

layout = [
    [sg.Text(get_config("MODULECONSTANT", "APPLICATIONMASTERDETAIL"),
             size=(20,2), font=font)],
    [sg.Text("アプリケーション名", font=font),
     sg.InputText(size=size, font=font, key="app_name")],
    [sg.Text("アカウント必要区分", font=font),
     sg.Combo(values=["必要","不要"],
              default_value="必要", font=font, key="account_class",
              readonly=True)],
    [sg.Text("パスワード定期変更区分", font=font),
     sg.Combo(values=["必要","不要"], default_value="必要", font=font,
              key="notice_class", readonly=True)],
    [sg.Text("記号区分", font=font),
     sg.Combo(values=["あり","なし"], default_value="あり", font=font,
              key="mark_class", readonly=True)],
    [sg.Text("仮登録パスワード桁数", font=font),
     sg.Spin(size=size_small, values=[i for i in range(1, 100)], font=font,
             key="auto_size", readonly=True)],
    [sg.Button("登録", font=font, key="regist"),
     sg.Button("検索", font=font, key="search"),
    sg.Button("終了", font=font, key="cancel")]
]

window = sg.Window(get_config("MODULECONSTANT", "TITLE"), layout)

while True:
    event, value = window.read()

    application = Application()
    log = Log()

    if event == None:
        break

    if event == 'regist':
        confirm_regist = sg.PopupYesNo("アプリケーションを登録しますか。",
                                       font=font_popup,
                                       title=title_popup_success)
        if confirm_regist == "Yes":
            app_name = value["app_name"]
            if value["account_class"] == "必要":
                account_class = CONST.NeedAccount
            else:
                account_class = CONST.NoNeedAccount
            # Issue21: パスワード変更通知(パスワード定期変更区分の追加)
            if value["notice_class"] == "必要":
                notice_class = CONST.NeedNotice
            else:
                notice_class = CONST.NoNeedNotice
            # Issue29: 次世代PMAPP(記号区分と仮登録パスワード桁数の追加)
            if value["mark_class"] == "あり":
                mark_class = CONST.NeedMark
            else:
                mark_class = CONST.NoNeedMark
            auto_size = value["auto_size"]

            if app_name == "":
                log.write('error', 'エラー：アプリ名未入力')
                sg.PopupOK("アプリ名が入力されていません。",
                           font=font_popup,
                           title=title_popup)
            
            else:
                # アプリケーションマスタ登録処理
                try:
                    if application_detail["no"] == 0:
                        # 登録処理
                        application.regist(app_name, account_class,
                                           notice_class, mark_class, auto_size)
                        # curl.post(f"create?name={app_name}&accountclass={account_class}&noticeclass={notice_class}&markclass={mark_class}&autosize={auto_size}")
                    else:
                        # 更新処理
                        no = str(application_detail["no"])
                        application.update(no, app_name, account_class,
                                           notice_class, mark_class, auto_size)
                        # curl.post(f"update?no={no}&name={app_name}&accountclass={account_class}&noticeclass={notice_class}&markclass={mark_class}&autosize={auto_size}")
                    
                    sg.Popup("アプリケーションをデータベースに登録しました。",
                             font=font_popup, title=title_popup_success)

                    # データのリセット
                    application_detail["no"] = 0
                
                except Exception as e:
                    log.write("error", str(e))
                    sg.Popup("アプリケーションの登録に失敗しました。",
                             font=font_popup, title=title_popup_success)

        elif confirm_regist == "No":
            sg.Popup("パスワード登録処理をキャンセルします。", font=font_popup,
                     title=title_popup_success)

        else:
            sg.Popup("パスワード登録処理をキャンセルします。", font=font_popup,
                     title=title_popup_success)

    if event == 'search':
        app_name = value["app_name"]
        # curl = Curl(f"{get_config('CURLURL', 'ROOTURL')}{get_config('CURLURL', 'APPLICATIONLISTURL')}search/app={app_name}")
        if app_name == "":
            log.write('error', 'エラー：アプリ名未入力')
            sg.PopupOK("アプリ名が入力されていません。", font=font_popup,
                       title=title_popup)
        else:
            try:
                # application_detail = curl.get()
                application_detail = application.search(app_name)
                account_class = application_detail["accountclas"]
                if (account_class == CONST.NeedAccount):
                    window["account_class"].update('必要')
                elif (account_class == CONST.NoNeedAccount):
                    window["account_class"].update('不要')
                
                # Issue21: パスワード変更通知(パスワード定期変更区分の追加)
                notice_class = application_detail["noticeclas"]
                if (notice_class == CONST.NeedNotice):
                    window["notice_class"].update('必要')
                elif (notice_class == CONST.NoNeedNotice):
                    window["notice_class"].update('不要')

                # Issue29: 次世代PMAPP(記号区分と仮登録パスワード桁数の追加)
                mark_class = application_detail["markclas"]
                if (mark_class == CONST.NeedMark):
                    window["mark_class"].update('あり')
                elif (mark_class == CONST.NoNeedMark):
                    window["mark_class"].update('なし')
                
                window["auto_size"].update(application_detail["autosize"])

            except Exception as e:
                    if str(e.msg) == "Expecting value":
                        log.write("error", "検索結果なし")
                        sg.PopupOK("アプリケーションが見つかりませんでした。",
                                   font=font_popup, title=title_popup)
                    else:
                        log.write("error", str(e))
                        sg.PopupOK("アプリケーションの取得に失敗しました。",
                                   font=font_popup, title=title_popup)

    if event == 'cancel':
        sg.PopupOK("アプリケーションを終了します。", font=font_popup,
                   title=title_popup_success)
        break

window.close()