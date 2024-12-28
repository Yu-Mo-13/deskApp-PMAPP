# coding: UTF-8

import logging
import os
from classes.execDate import ExecuteDate as ExecuteDate

class Log():

    def __init__(self):
        self.level = ''
        self.message = ''

    def write(self, level, message):
        # ログファイルを出力するディレクトリの指定(固定値)
        dir_name = './log'
        file_name = dir_name + '/log_0.log'

        # ログレベルとログメッセージの代入
        self.level = level
        self.message = message

        if not(os.path.exists(file_name)):
            # ログファイルを作成
            os.mkdir(dir_name)
            f = open(file_name, 'w')
            f.close

        # ログの基本設定
        logging.basicConfig(filename='log/log_0.log', level=logging.DEBUG)

        # 実行日時取得
        date = ExecuteDate().get()

        if (self.level == 'info'):
            logging.info(date + ' ' + self.message)
            return True

        if (self.level == 'error'):
            logging.error(date + ' ' + self.message)
            return True
        
        if (self.level == 'sql'):
            logging.info(date + ' ' + self.message)
