# coding: UTF-8

import PySimpleGUI as sg
import sys

import classes.subprocess as subprocess
from function.config import get_config
from classes.curl import Curl
from classes.log import Log

# ウィジェットのプロパティ
font = ("meiryo", 20)
size = (25, 2)
size_column = (10, 1)
url_prefix = "cd="
admin_radio_values = [
    ["あり", "admin"],
    ["なし", "general"]
]

# ログオブジェクト作成
insLog = Log()

# コマンドの引数から権限CDを取得
authorityDetail = {
    "name": "",
    "adminflg": ""
}
authoritycd = int(sys.argv[1])
authorityname = ""
adminflg = ""
newadminflg = ""

if authoritycd > 0:
    # 権限マスター詳細情報を取得
    insCurl = Curl(get_config("CURLURL", "ROOTURL") + get_config("CURLURL", "AUTHORITYLISTURL") + url_prefix + str(authoritycd))
    try:
        authorityDetail = insCurl.get()
        authorityname = authorityDetail["name"]
        adminflg = authorityDetail["adminflg"]
    except Exception as e:
        insLog.write("error", str(e))
        sg.Popup("権限マスター詳細情報の取得に失敗しました。", font=font, title=get_config("MODULECONSTANT", "AUTHORITYMASTERDETAIL"))

# ヘッダー部のレイアウト
layout = [
    [sg.Text(get_config("MODULECONSTANT", "AUTHORITYMASTERDETAIL"), size=size, font=font)],
    [sg.Text("名称", font=font, size=size_column), sg.InputText(size=size, font=font, key="name", default_text=authorityname)],
    [sg.Text("Admin権限有無", font=font, size=size_column),
     sg.Radio(admin_radio_values[0][0], key=admin_radio_values[0][1], group_id="adminflg", font=font),
     sg.Radio(admin_radio_values[1][0], key=admin_radio_values[1][1], group_id="adminflg", font=font, default=True)],
    [sg.Button("登録", font=font, key="regist"),sg.Button("削除", font=font, key="delete", disabled=authoritycd <= 0),sg.Button("終了", font=font, key="cancel")]
]

window = sg.Window(get_config("MODULECONSTANT", "AUTHORITYMASTERDETAIL"), layout)

while True:
    event, value = window.read()
    newauthorityname = value["name"]
    # 一覧画面インスタンス
    insSubprocess = subprocess.Subprocess(["python3", "authorityMasterList.py"])

    if event == None:
        break

    if event == "regist":
        insCurl = Curl(get_config("CURLURL", "ROOTURL") + get_config("CURLURL", "AUTHORITYLISTURL"))
        # DBに登録するadminフラグを設定
        if value[admin_radio_values[0][1]] == True:
            newadminflg = "1"
        elif value[admin_radio_values[1][1]] == True:
            newadminflg = "0"
        else:
            newadminflg = ""

        try:
            if authoritycd > 0:
                # 更新処理
                insCurl.post({"cd": authoritycd, "name": newauthorityname, "adminflg": newadminflg}, "update/cd=" + str(authoritycd) + "&name=" + newauthorityname + "&adminflg=" + newadminflg)
            else:
                # 登録処理
                insCurl.post({"name": newauthorityname, "adminflg": newadminflg}, "create/name=" + newauthorityname + "&adminflg=" + newadminflg)

            sg.Popup("登録が完了しました。", font=font, title=get_config("MODULECONSTANT", "AUTHORITYMASTERDETAIL"))

        except Exception as e:
            insLog.write("error", str(e))
            sg.Popup("登録に失敗しました。", font=font, title=get_config("MODULECONSTANT", "AUTHORITYMASTERDETAIL"))

    if event == "delete":
        message_delete = sg.PopupYesNo("権限を削除しますか。", font=font, title=get_config("MODULECONSTANT", "AUTHORITYMASTERDETAIL"))
        if message_delete == "Yes":
            # 削除処理
            try:
                insCurl = Curl(get_config("CURLURL", "ROOTURL") + get_config("CURLURL", "AUTHORITYLISTURL"))
                insCurl.post({"cd": authoritycd}, "delete/cd=" + str(authoritycd))
                sg.Popup("削除が完了しました。", font=font, title=get_config("MODULECONSTANT", "AUTHORITYMASTERDETAIL"))

            except Exception as e:
                insLog.write("error", str(e))
                sg.Popup("削除に失敗しました。", font=font, title=get_config("MODULECONSTANT", "AUTHORITYMASTERDETAIL"))

    if event == "cancel":
        # メニュー画面呼び出し
        insSubprocess.run_async()
        break

window.close()