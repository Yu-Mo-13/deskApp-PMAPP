# coding: UTF-8

import PySimpleGUI as sg
from passwordWk import PasswordWk as PasswordWk
from registAction import RegistAction as RegistAction

class ShowPasswordWkList():

    def __init__(self, font, size, font_popup, title):
        self.font = font
        self.size = size
        self.font_popup = font_popup
        self.title = title

    def show(self):
        layout = [
            [sg.Text("登録されていないパスワード一覧", size=self.size, font=self.font)],
        ]
        for row in range(5):
            layout.append([sg.Text("パスワード" + str(row + 1), font=self.font), sg.InputText(size=self.size, font=self.font, key="password" + str(row + 1)),
                           sg.Text("アプリ名" + str(row + 1), font=self.font), sg.InputText(size=self.size, font=self.font, key="application" + str(row + 1)),
                           sg.Text("アカウント" + str(row + 1), font=self.font), sg.InputText(size=self.size, font=self.font, key="other_info" + str(row + 1)),
                           sg.Text("登録日" + str(row + 1), font=self.font), sg.InputText(size=self.size, font=self.font, key="registered_date" + str(row + 1)),
                           sg.Button("登録", font=self.font, key="regist" + str(row + 1))])
            
        layout.append([sg.Button("取得", font=self.font, key="get")])
        layout.append([sg.Button("終了", font=self.font, key="quit")])

        window = sg.Window("パスワード管理アプリ", layout)

        while True:
            event, value = window.read()
            if event == None:
                break

            if event.startswith("regist"):
                # eventから登録ボタンの番号を取得
                exec_row = event.replace("regist", "")
                pwd = value["password" + exec_row]
                app = value["application" + exec_row]
                other_info = value["other_info" + exec_row]
                registered_date = value["registered_date" + exec_row]

                message_regist = sg.PopupYesNo("パスワードを登録しますか。", font=self.font_popup, title=self.title)
                if message_regist == "Yes":
                    # 登録処理
                    insAction = RegistAction(pwd, app, other_info, registered_date)
                    result = insAction.execute()

                    if not(result[0]):
                        sg.Popup(result[1], font=self.font_popup, title=self.title)
                    else:
                        insPasswordWk = PasswordWk('delete')
                        insPasswordWk.delete(pwd, app, other_info)
                        # 登録成功時の処理
                        sg.Popup(result[1], font=self.font_popup, title=self.title)

            # 終了ボタン
            if event == "quit":
                message_quit = sg.PopupYesNo("この画面を閉じますか。", font=self.font_popup, title=self.title)
                if message_quit == "Yes":
                    break