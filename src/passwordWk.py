# coding: UTF-8
from dbLogicBase import DbLogicBase as DbLogicBase
from execSql import ExecSql as ExecSql

class PasswordWk(DbLogicBase):

    def __init__(self, method):
        super().__init__(method)

    def regist(self, pwd, app, rDate):
        sql = "insert into " + self.tblpasswk + "(pwd, app, other_info, registered_date)"
        sql = sql + " values('" + pwd + "','" + app + "', null ,'" + rDate + "')"

        ExecSql().insert(sql)
        return True
    
    def delete(self, app, oInfo):
        sql = "delete from " + self.tblpasswk + " "
        sql = sql + "where app = '" + app + "' and other_info = '" + oInfo + "'"

        ExecSql().delete(sql)
        return True
