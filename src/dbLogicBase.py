# coding: UTF-8
from log import Log as Log
from connectDatabase import ConnectDatabase as ConnectDatabase
from execSql import ExecSql as ExecSql
# 2023/05/13 add issue #1
from config import Config as Config
from encryption import Encryption as Encryption

class DbLogicBase():

    # 2023/05/13 mod issue #1
    def __init__(self, method):
        insConfig = Config()
        insEncryption = Encryption()

        self.insLog = Log()
        self.insSql = ExecSql()

        if not(method == 'insert' or method == 'select'):
            self.insLog.write('error', 'エラー：データベース処理')
            return False

        self.method = method
        self.tblpass = insEncryption.decrypt(insConfig.get('tablepassword'))
        self.tblapp = insEncryption.decrypt(insConfig.get('tableapplication'))
        self.execOutput = False
        return True
    
    def makeConnection(self):
        insConDb = ConnectDatabase()
        return insConDb.makeConnection()
