# coding: UTF-8
import csv

class GetConfig():

    def __init__(self):
        self.path = '../conf.csv'

    # 設定ファイルを読み取る
    def read(self, name):
        with open(self.path, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] == name:
                    return row[1]