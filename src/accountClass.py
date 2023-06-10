# coding: UTF-8
from dbLogicBase import DbLogicBase as DbLogicBase
from execSql import ExecSql as ExecSql

class AccountClass(DbLogicBase):

    def __init__(self, method):
        super().__init__(method)

    def search(self, app):
        sql = "select accountclas from " + self.tblapp + " "
        sql = sql + "where name = '" + app + "'"

        return ExecSql().select(sql, 'accountclas')