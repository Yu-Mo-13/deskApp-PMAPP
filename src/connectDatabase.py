# coding: UTF-8
import pymysql as pm
from config import Config as Config
from encryption import Encryption as Encryption

class ConnectDatabase():

    def __init__(self):
        # 2023/05/12 add issue #1
        insConfig = Config()
        insEncryption = Encryption()

        self.host = insEncryption.decrypt(insConfig.get('dbhost'))
        # 2023/05/12 mod issue #1 start
        self.user = insEncryption.decrypt(insConfig.get('dbuser'))
        self.password = insEncryption.decrypt(insConfig.get('dbpassword'))
        self.dbname = insEncryption.decrypt(insConfig.get('dbname'))
        # 2023/05/12 mod issue #1 end
        self.charset = 'utf8'
        self.cursorclass = pm.cursors.DictCursor
        self.ssl = {'ca': '/etc/ssl/cert.pem', 'check_hostname': False}

    def makeConnection(self):
        connection = pm.connect(
            host = self.host,
            user = self.user,
            password = self.password,
            db = self.dbname,
            charset = self.charset,
            cursorclass = self.cursorclass,
            ssl = self.ssl
        )
        return connection
