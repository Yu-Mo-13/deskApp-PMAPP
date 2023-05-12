# coding: UTF-8
import pymysql as pm
from getConfig import GetConfig as GetConfig
from encryption import Encryption as Encryption

class ConnectDatabase():

    def __init__(self):
        # 2023/05/12 add issue #1
        insGetConfig = GetConfig()
        insEncryption = Encryption()

        self.host = 'localhost'
        # 2023/05/12 mod issue #1 start
        self.user = insEncryption.decrypt(insGetConfig.read('dbuser'))
        self.password = insEncryption.decrypt(insGetConfig.read('dbpassword'))
        self.dbname = insEncryption.decrypt(insGetConfig.read('dbname'))
        # 2023/05/12 mod issue #1 end
        self.charset = 'utf8'
        self.cursorclass = pm.cursors.DictCursor

    def makeConnection(self):
        connection = pm.connect(
            host = self.host,
            user = self.user,
            password = self.password,
            db = self.dbname,
            charset = self.charset,
            cursorclass = self.cursorclass
        )
        return connection
