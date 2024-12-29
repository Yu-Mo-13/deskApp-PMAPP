# coding: UTF-8


class ButtonActionBase:

    def __init__(self, pwd, app, oInfo):
        self.pwd = pwd
        self.app = app
        self.oInfo = oInfo

    def execute(self):
        return True
