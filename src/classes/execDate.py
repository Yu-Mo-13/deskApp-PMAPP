# coding: UTF-8

import datetime


class ExecuteDate:

    def __init__(self):
        self.execDate = datetime.datetime.now()

    def get(self):
        return self.execDate.strftime("%Y-%m-%d")
