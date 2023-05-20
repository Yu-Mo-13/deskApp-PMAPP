# coding: UTF-8
import csv

class Config():

    def __init__(self):
        # 1階層上のconf.csvのパスをself.pathに格納
        self.path = './conf.csv'

    # 設定ファイルを読み取る
    def get(self, name):
        with open(self.path, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] == name:
                    return row[1]