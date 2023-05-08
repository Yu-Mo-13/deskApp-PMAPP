# coding: UTF-8
import pymysql as pm

class ConnectDatabase():

    def __init__(self):
        self.host = 'localhost'
        self.user = 'user01'
        self.password = 'user01'
        self.dbname = 'manage_password'
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
