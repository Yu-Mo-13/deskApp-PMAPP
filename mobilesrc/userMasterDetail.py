# coding: UTF-8

import PySimpleGUI as sg
import sys

import classes.subprocess as subprocess
from classes.curl import Curl
from classes.log import Log
from classes.encryption import Encryption
from function.config import get_config

# ウィジェットのプロパティ
font = ("meiryo", 20)
size = (25, 2)
size_column = (10, 1)
url_prefix = "id="

# ログオブジェクト作成
insLog = Log()

# 暗号化オブジェクト作成
insEncryption = Encryption()

# コマンドの引数からユーザーIDを取得
userDetail = {
    "id": "",
    "engname": "",
    "jpnname": "",
    "password": "",
    "authcd": ""
}
authList = []
userid = int(sys.argv[1])

if userid > 0:
    # ユーザーマスター詳細情報を取得
    insCurl = Curl(get_config("CURLURL", "ROOTURL") + get_config("CURLURL", "USERLISTURL") + url_prefix + str(userid))
    try:
        userDetail = insCurl.get()
    except Exception as e:
        insLog.write("error", str(e))
        sg.Popup("ユーザーマスター詳細情報の取得に失敗しました。", font=font, title=get_config("MODULECONSTANT", "USERMASTERDETAIL"))

# 権限一覧を取得(画面上にはラジオボタンとして表示する)
insAuthList = Curl(get_config("CURLURL", "ROOTURL") + get_config("CURLURL", "AUTHORITYLISTURL"))
try:
    authList = insAuthList.get()
except Exception as e:
    insLog.write("error", str(e))
    sg.Popup("権限一覧の取得に失敗しました。", font=font, title=get_config("MODULECONSTANT", "USERMASTERDETAIL"))

# 詳細部(固定)レイアウト
layout = [
    [sg.Text(get_config("MODULECONSTANT", "USERMASTERDETAIL"), size=size, font=font)],
    [sg.Text("ユーザー名(英)", font=font, size=size_column), 
     sg.InputText(size=size, font=font, key="engname", default_text=userDetail["engname"])],
    [sg.Text("ユーザー名(日)", font=font, size=size_column), 
     sg.InputText(size=size, font=font, key="jpnname", default_text=userDetail["jpnname"])],
    [sg.Text("パスワード", font=font, size=size_column),
     sg.InputText(size=size, font=font, key="password", default_text=insEncryption.decrypt(userDetail["password"]), password_char="*")],
    [sg.Text("権限", font=font, size=size_column)]
]

# 詳細部(可変)レイアウト(権限)
# 権限一覧の数だけ、ラジオボタンを作成する
for auth in authList:
    layout.append([sg.Radio(auth["name"], key=auth["name"], group_id="authority", font=font, default=auth["cd"] == userDetail["id"])])

# ボタン部のレイアウト
layout.append([sg.Button("登録", font=font, key="regist"), 
               sg.Button("削除", font=font, key="delete", disabled=userid <= 0), 
               sg.Button("終了", font=font, key="cancel")])

window = sg.Window(get_config("MODULECONSTANT", "USERMASTERDETAIL"), layout)

while True:
    event, value = window.read()
    newengname = value["engname"]
    newjpnname = value["jpnname"]
    newpassword = insEncryption.encrypt(value["password"])
    # ラジオボタンで選択した権限名に対応する権限CDを取得
    for auth in authList:
        if value[auth["name"]]:
            newauthcd = auth["cd"]
            break
    
    # 一覧画面インスタンス
    insSubprocess = subprocess.Subprocess(["python3", "userMasterList.py"])

    if event == None:
        break

    if event == "regist":
        # ユーザーマスター登録処理
        insCurl = Curl(get_config("CURLURL", "ROOTURL") + get_config("CURLURL", "USERLISTURL"))
        try:
            if userid > 0:
                # ユーザーマスター更新処理
                insCurl.post({"id": userid, "engname": newengname, "jpnname": newjpnname, "password": newpassword, "authcd": newauthcd}, 
                             "update/id=" + str(userid) + "&engname=" + newengname + "&jpnname=" + newjpnname + "&password=" + newpassword + "&authcd=" + str(newauthcd))
            else:
                # ユーザーマスター登録処理
                insCurl.post({"engname": newengname, "jpnname": newjpnname, "password": newpassword, "authcd": newauthcd}, 
                             "create/engname=" + newengname + "&jpnname=" + newjpnname + "&password=" + newpassword + "&authcd=" + str(newauthcd))

            sg.Popup("登録が完了しました。", font=font, title=get_config("MODULECONSTANT", "USERMASTERDETAIL"))

        except Exception as e:
            insLog.write("error", str(e))
            sg.Popup("登録に失敗しました。", font=font, title=get_config("MODULECONSTANT", "USERMASTERDETAIL"))

    if event == "delete":
        message_delete = sg.PopupYesNo("ユーザーを削除しますか。", font=font, title=get_config("MODULECONSTANT", "USERMASTERDETAIL"))
        if message_delete == "Yes":
            # ユーザーマスター削除処理
            try:
                insCurl = Curl(get_config("CURLURL", "ROOTURL") + get_config("CURLURL", "USERLISTURL"))
                insCurl.post({"id": userid}, "delete/id=" + str(userid))
                sg.Popup("削除が完了しました。", font=font, title=get_config("MODULECONSTANT", "USERMASTERDETAIL"))

            except Exception as e:
                insLog.write("error", str(e))
                sg.Popup("削除に失敗しました。", font=font, title=get_config("MODULECONSTANT", "USERMASTERDETAIL"))

    if event == "cancel":
        insSubprocess.run_async()
        break

window.close()
