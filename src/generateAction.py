# coding: UTF-8

from buttonActionBase import ButtonActionBase as ButtonActionBase

class GenerateAction(ButtonActionBase):

    def __init__(self, pwd, app, oInfo, rDate):
        super().__init__(pwd, app, oInfo, rDate)

    def execute(self):
        return super().execute()