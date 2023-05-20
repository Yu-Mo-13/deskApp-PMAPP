# coding: UTF-8
from dbLogicBase import DbLogicBase as DbLogicBase

class AccountClass(DbLogicBase):

    def __init__(self, method):
        super().__init__(method)

    def search(self, app):
        sql = "select accountclas from manage_password.tbl_appln "
        sql = sql + "where name = '" + app + "'"

        return DbLogicBase.execSelSql(self, sql)