# coding: UTF-8
from dbLogicBase import DbLogicBase as DbLogicBase
from execSql import ExecSql as ExecSql

class PasswordWk(DbLogicBase):

    def __init__(self, method):
        super().__init__(method)

    def regist(self, pwd, app, oInfo, rDate):
        # 必須項目入力チェック
        # pwdとappとoInfoの文字列の長さのいずれかが1未満の場合はfalseを返す
        if len(pwd) < 1 or len(app) < 1 or len(oInfo) < 1:
            return False
        
        sql = "insert into " + self.tblpasswk + "(pwd, app, other_info, registered_date)"
        sql = sql + " values('" + pwd + "','" + app + "', null ,'" + rDate + "')"

        ExecSql().insert(sql)
        return True
    
    def count(self):
        sql = "select count(*) as cnt from " + self.tblpasswk

        return int(ExecSql().select(sql, 'cnt'))
    
    def delete(self, app, oInfo):
        sql = "delete from " + self.tblpasswk + " "
        sql = sql + "where app = '" + app + "' and other_info = '" + oInfo + "'"

        ExecSql().delete(sql)
        return True
    
    def deleteAll(self):
        sql = "delete from " + self.tblpasswk

        ExecSql().delete(sql)
        return True