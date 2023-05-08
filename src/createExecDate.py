# coding: UTF-8

import datetime

class CreateExecuteDate():

    def __init__(self):
        sExecDt = datetime.datetime.now()
        self.execDate = sExecDt.strftime('%Y-%m-%d')

    def createExecDate(self):
        return self.execDate
