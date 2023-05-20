# coding: UTF-8

import PySimpleGUI as sg
from log import Log as Log
from execDate import ExecuteDate as ExecuteDate
from generatePassword import GeneratePassword as GeneratePassword
from connectDatabase import ConnectDatabase as ConnectDatabase
from password import Password as Password
from passwordNoAccount import PasswordNoAccount as PasswordNoAccount
from application import Application as Application
from accountClass import AccountClass as AccountClass
# 2023/04/29 add ref: 20230429_PasswordEncryption
from encryption import Encryption as Encryption

# ウィジェットのプロパティ
font = ("meiryo", 20)
size = (20, 3)

font_popup = ("meiryo", 16)
title_popup_success = "パスワード管理アプリ"
title_popup = "エラー"

layout = [
    [sg.Text("パスワード管理アプリ", size=(20,2), font=font)],
    [sg.Text("パスワード", font=font), sg.InputText(size=size, font=font, key="password")],
    [sg.Text("使用アプリ", font=font), sg.InputText(size=size, font=font, key="application")],
    [sg.Text("備　　　考", font=font), sg.InputText(size=size, font=font, key="other_info")],
    [sg.Text("パスワード桁数", font=font), sg.InputText(size=(size[0] - 10, size[1]), font=font, key="length")],
    [sg.Button("パスワード生成", font=font, key="generate"), sg.Button("パスワード登録", font=font, key="register"), 
    sg.Button("パスワード検索", font=font, key="search"), sg.Button("アプリ終了", font=font, key="cancel")]
]

window = sg.Window("パスワード管理アプリ", layout)

while True:
    event, value = window.read()
    insLog = Log()
    # 2023/04/29 add ref: 20230429_PasswordEncryption
    insEncryption = Encryption()

    if event == None:
        break

    if event == "generate":
        try:
            # パスワード桁数をint型に変換
            intLength = int(value["length"])

            # パスワードの生成
            insGeneratePassword = GeneratePassword(intLength)
            password = insGeneratePassword.generate()

            # パスワード入力欄にパスワードを表示
            window['password'].update(password)
            insLog.write('info', '正常：パスワード作成完了')

        except ValueError as e:
            insLog.write('error', 'エラー：パスワード桁数データ型不正')
            sg.PopupOK("パスワード桁数は整数を入力してください。" , font=font_popup, title=title_popup)

    if event == "register":
        regFlg = False
        confirm_register = sg.PopupYesNo("パスワードを登録しますか。", font=font_popup, title=title_popup_success)
        if confirm_register == "Yes":
            pwd = value["password"]
            app = value["application"]
            # 2023/2/12 備考を追加
            other_info = value["other_info"]
            registered_date = ExecuteDate().get()

            if pwd == "":
                insLog.write('error', 'エラー：パスワード未入力')
                sg.PopupOK("パスワードが入力されていません。", font=font_popup, title=title_popup)
            
            else:
                if app == "":
                    insLog.write('error', 'エラー：アプリケーション名未入力')
                    sg.PopupOK("登録先のアプリケーション名を入力してください。", font=font_popup, title=title_popup)

                else:
                    # パスワード登録処理
                    # 登録前にアカウント情報が入力済みかをチェックする
                    insApplication = Application('select')
                    accountClas = AccountClass('select').search(app)

                    if not(accountClas):
                        insLog.write('error', 'エラー：アプリケーション未登録')
                        sg.PopupOK('アプリケーションマスタにアプリを登録してください。', font=font_popup, title=title_popup)

                    # 2023/04/29 add ref: 20230429_PasswordEncryption
                    enc_pwd = insEncryption.encrypt(pwd)

                    if (accountClas == '0'):
                        # アカウント必要区分が不要の場合、備考列にはNULLが入る
                        insPassword = PasswordNoAccount('insert')
                        regFlg = insPassword.regist(enc_pwd, app, registered_date)

                    if (accountClas == '1'):
                        if (other_info == ''):
                            insLog.write('error', 'エラー：アカウント情報未入力')
                            sg.PopupOK('備考欄にアカウント情報を入力してください。', font=font_popup, title=title_popup)
                        
                        else:
                            insPassword = Password('insert')
                            regFlg = insPassword.regist(enc_pwd, app, other_info, registered_date)
                    
                    if not(regFlg):
                        # 登録失敗時の処理
                        sg.Popup("パスワードの登録に失敗しました。", font=font_popup, title=title_popup)
                    else:
                        # 登録成功時の処理
                        sg.Popup("パスワードをデータベースに登録しました。", font=font_popup, title=title_popup_success)
                    
        elif confirm_register == "No":
            sg.Popup("パスワード登録処理をキャンセルします。", font=font_popup, title=title_popup_success)

        else:
            sg.Popup("パスワード登録処理をキャンセルします。", font=font_popup, title=title_popup_success)

    if event == "search":
        app = value["application"]
        other_info = value["other_info"]
        pwd = ''

        if app == "":
            insLog.write('error', 'アプリケーション名未入力')
            sg.PopupOK("パスワードを検索するアプリケーションを入力してください。", font=font_popup, title=title_popup)

        else:
            # アプリケーションマスタからアカウント必要区分を取得する
            insApplication = Application('select')
            accountClas = AccountClass('select').search(app)

            if not(accountClas):
                insLog.write('error', 'エラー：アプリケーション未登録')
                sg.PopupOK('アプリケーションマスタにアプリを登録してください。', font=font_popup, title=title_popup)

            if (accountClas == '0'):
                # 現時点では、アカウント必要区分が不要の場合は、備考の情報は検索条件として扱っていない
                # 備考の情報の扱いは、今後のアプデで考えていくものとする
                insPassword = PasswordNoAccount('select')

                # 2023/04/29 mod ref: 20230429_PasswordEncryption
                pwd = insEncryption.decrypt(insPassword.search(app))

            if (accountClas == '1'):
                # アカウント必要区分が「必要」かつ備考欄が未入力の場合、未入力エラーを出す
                if (other_info == ''):
                    insLog.write('error', 'エラー：アカウント情報未入力')
                    sg.PopupOK('備考欄にアカウント情報を入力してください。', font=font_popup, title=title_popup)

                else:
                    insPassword = Password('select')

                    # 2023/04/29 mod ref: 20230429_PasswordEncryption
                    pwd = insEncryption.decrypt(insPassword.search(app, other_info))

            if accountClas and not(pwd):
                sg.PopupOK('該当するパスワードは見つかりませんでした。', font=font_popup, title=title_popup_success)
            
            else:
                # 管理画面のパスワード入力欄を更新
                window['password'].update(pwd)
 
    if event == "cancel":
        sg.PopupOK("アプリケーションを終了します。", font=font_popup, title=title_popup_success)
        break

window.close()