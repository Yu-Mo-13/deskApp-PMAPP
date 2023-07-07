# coding: UTF-8

import PySimpleGUI as sg

class ButtonActionBase():

    def __init__(self, pwd, app, oInfo, rDate):
        self.pwd = pwd
        self.app = app
        self.oInfo = oInfo
        self.rDate = rDate

    def execute(self):
        return True