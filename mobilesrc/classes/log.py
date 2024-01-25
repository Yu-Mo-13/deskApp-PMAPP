# coding: UTF-8

import logging
import os
from classes.execDate import ExecuteDate

class Log():

    def __init__(self):
        self.level = ''
        self.message = ''

    def write(self, logLevel, logMessage):
        # ログファイルを出力するディレクトリの指定(固定値)
        dirName = './log'
        fileName = dirName + '/log_0.log'

        # ログレベルとログメッセージの代入
        self.level = logLevel
        self.message = logMessage

        if not(os.path.exists(fileName)):
            # ログファイルを作成
            os.mkdir(dirName)
            f = open(fileName, 'w')
            f.close

        # ログの基本設定
        logging.basicConfig(filename='log/log_0.log', level=logging.DEBUG)

        # 実行日時取得
        insCreateExecDate = ExecuteDate()
        dtExec = insCreateExecDate.get()

        if (self.level == 'info'):
            logging.info(dtExec + ' ' + self.message)
            return True

        if (self.level == 'error'):
            logging.error(dtExec + ' ' + self.message)
            return True
        
        if (self.level == 'sql'):
            logging.info(dtExec + ' ' + self.message)
