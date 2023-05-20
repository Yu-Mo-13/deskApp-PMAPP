# coding: UTF-8
from dbLogicBase import DbLogicBase as DbLogicBase
# import Log

class Application(DbLogicBase):

    def __init__(self, method):
        super().__init__(method)

    def regist(self, appName, accountClas, rDate):
        sql = "insert into " + self.tblapp + "(name, accountclas, registered_date)"
        sql = sql + " values('" + appName + "','" + accountClas + "','" + rDate + "')"

        self.insSql.insert(self, sql)
        return True

    def search(self, app):
        sql = "select no, name, accountclas, registered_date from " + self.tblapp + " "
        sql = sql + "where name = '" + app + "'"

        return self.insSql.select(self, sql, 'pwd')
