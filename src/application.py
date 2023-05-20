# coding: UTF-8
from dbLogicBase import DbLogicBase as DbLogicBase
from execSql import ExecSql as ExecSql
# import Log

class Application(DbLogicBase):

    def __init__(self, method):
        super().__init__(method)

    def regist(self, appName, accountClas, rDate):
        sql = "insert into " + self.tblapp + "(name, accountclas, registered_date)"
        sql = sql + " values('" + appName + "','" + accountClas + "','" + rDate + "')"

        ExecSql().insert(sql)
        return True

    def search(self, app):
        sql = "select no, name, accountclas, registered_date from " + self.tblapp + " "
        sql = sql + "where name = '" + app + "'"

        return ExecSql().select(sql, 'accountclas')
