# coding: UTF-8

import PySimpleGUI as sg
from classes.generateAction import GenerateAction as GenerateAction

# 2023/06/25 add issue #7 ワークテーブルの参照を追加
from classes.passwordWk import PasswordWk as PasswordWk

# アクションクラス呼び出し
from classes.registAction import RegistAction as RegistAction
from classes.searchAction import SearchAction as SearchAction
from classes.subprocess import Subprocess as Subprocess
from function.config import get_config

# ウィジェットのプロパティ
font = ("meiryo", 20)
size = (20, 3)
# モード選択 記号あり、記号なし Issue #18
need_symbol = ("記号あり", "記号なし")

font_popup = ("meiryo", 16)

layout = [
    [sg.Text(get_config("MODULECONSTANT", "PASSWORDDETAIL"), size=(20, 2), font=font)],
    [
        sg.Text("パスワード", font=font),
        sg.InputText(size=size, font=font, key="password"),
        sg.Button("作成", font=font, key="generate"),
        sg.Combo(
            need_symbol,
            default_value=need_symbol[0],
            size=(size[0] - 10, size[1]),
            font=font,
            key="symbol_mode",
        ),
    ],
    [
        sg.Text("使用アプリ", font=font),
        sg.InputText(size=size, font=font, key="application"),
    ],
    [
        sg.Text("備　　　考", font=font),
        sg.InputText(size=size, font=font, key="other_info"),
    ],
    [
        sg.Text("パスワード桁数", font=font),
        sg.InputText(size=(size[0] - 10, size[1]), font=font, key="length"),
    ],
    [
        sg.Button("パスワード登録", font=font, key="register"),
        sg.Button("パスワード検索", font=font, key="search"),
        sg.Button("未登録パスワード一覧", font=font, key="work_list"),
        sg.Button("アプリ終了", font=font, key="cancel"),
    ],
]

window = sg.Window("パスワード管理アプリ", layout)

while True:
    event, value = window.read()

    if event is None:
        break

    if event == "generate":
        # 記号あり、記号なしの判定
        symbol_mode = value["symbol_mode"]
        app = value["application"]
        other_info = value["other_info"]
        # パスワード桁数をint型に変換
        length = value["length"]

        action = GenerateAction("", app, other_info)
        result = action.execute(length, need_symbol, symbol_mode)

        if result[0]:
            # パスワード入力欄にパスワードを表示
            window["password"].update(result[1])
        else:
            sg.PopupOK(
                result[1],
                font=font_popup,
                title=get_config("MODULECONSTANT", "ERRORTITLE"),
            )

    if event == "register":
        confirm_regist = sg.PopupYesNo(
            "パスワードを登録しますか。",
            font=font_popup,
            title=get_config("MODULECONSTANT", "TITLE"),
        )
        if confirm_regist == "Yes":
            pwd = value["password"]
            app = value["application"]
            # 2023/2/12 備考を追加
            other_info = value["other_info"]

            action = RegistAction(pwd, app, other_info)
            result = action.execute()

            if not (result[0]):
                sg.PopupOK(
                    result[1],
                    font=font_popup,
                    title=get_config("MODULECONSTANT", "ERRORTITLE"),
                )

            else:
                passwordwk = PasswordWk()
                passwordwk.delete(app, other_info)
                # 登録成功時の処理
                sg.Popup(
                    result[1],
                    font=font_popup,
                    title=get_config("MODULECONSTANT", "TITLE"),
                )

        elif confirm_regist == "No":
            sg.Popup(
                "パスワード登録処理をキャンセルします。",
                font=font_popup,
                title=get_config("MODULECONSTANT", "TITLE"),
            )

        else:
            sg.Popup(
                "パスワード登録処理をキャンセルします。",
                font=font_popup,
                title=get_config("MODULECONSTANT", "TITLE"),
            )

    if event == "search":
        app = value["application"]
        other_info = value["other_info"]
        pwd = ""

        action = SearchAction(pwd, app, other_info)
        result = action.execute()

        if not (result[0]):
            sg.PopupOK(
                result[1],
                font=font_popup,
                title=get_config("MODULECONSTANT", "ERRORTITLE"),
            )

        else:
            # 管理画面のパスワード入力欄を更新
            window["password"].update(result[1])

    # 2023/07/10 add issue #14
    if event == "work_list":
        # 入力欄をクリア
        window["password"].update("")
        window["application"].update("")
        window["other_info"].update("")
        window["length"].update("")
        Subprocess(["python3", "src/showPasswordWkList.py"]).run()

    if event == "cancel":
        passwordwk = PasswordWk()
        # 2023/06/25 add issue #7
        # ワークテーブルに1件でもデータが残っていたら、ワークテーブルのデータを全削除するかの確認を行う
        if len(passwordwk.selectAll()) > 0:
            confirm_cancel = sg.PopupYesNo(
                "ワークテーブルにデータが残っています。データを削除してアプリケーションを終了しますか。",
                font=font_popup,
                title=get_config("MODULECONSTANT", "ERRORTITLE"),
            )
            if confirm_cancel == "Yes":
                passwordwk.deleteAll()
                sg.PopupOK(
                    "アプリケーションを終了します。",
                    font=font_popup,
                    title=get_config("MODULECONSTANT", "TITLE"),
                )
                break
        else:
            sg.PopupOK(
                "アプリケーションを終了します。",
                font=font_popup,
                title=get_config("MODULECONSTANT", "TITLE"),
            )
            break

window.close()
