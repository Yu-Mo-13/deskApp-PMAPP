# coding: UTF-8

import PySimpleGUI as sg

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
                           sg.Button("登録", font=self.font, key="register" + str(row + 1))])
            
        layout.append([sg.Button("取得", font=self.font, key="get")])
        layout.append([sg.Button("終了", font=self.font, key="quit")])

        window = sg.Window("パスワード管理アプリ", layout)

        while True:
            event, value = window.read()
            if event == None:
                break

            # 終了ボタン
            if event == "quit":
                message_quit = sg.PopupYesNo("この画面を閉じますか。", font=self.font_popup, title=self.title)
                if message_quit == "Yes":
                    break