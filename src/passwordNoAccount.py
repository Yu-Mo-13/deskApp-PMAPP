# coding: UTF-8
from dbLogicBase import DbLogicBase as DbLogicBase

class PasswordNoAccount(DbLogicBase):

    def __init__(self, method):
        super().__init__(method)

    def regist(self, pwd, app, rDate):
        sql = "insert into " + self.tblpass + "(pwd, app, other_info, registered_date)"
        sql = sql + " values('" + pwd + "','" + app + "', null ,'" + rDate + "')"

        self.insSql.insert(self, sql)
        return True

    # 最新のパスワードを取得
    def search(self, app):
        sql = "select pwd from " + self.tblpass + " "
        sql = sql + "where no = (select max(no) from " + self.tblpass + " where app = '" + app + "')"

        return self.insSql.select(self, sql, 'pwd')
