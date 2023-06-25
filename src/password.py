# coding: UTF-8
from dbLogicBase import DbLogicBase as DbLogicBase
from execSql import ExecSql as ExecSql
# import Log

class Password(DbLogicBase):

    def __init__(self, method):
        super().__init__(method)

    def regist(self, pwd, app, oInfo, rDate):
        sql = "insert into " + self.tblpass + "(pwd, app, other_info, registered_date)"
        sql = sql + " values('" + pwd + "','" + app + "','" + oInfo + "','" + rDate + "')"

        ExecSql().insert(sql)
        return True

    def count(self, app, oInfo):
        sql = "select count(*) as cnt from " + self.tblpass
        sql = sql + " where app = '" + app + "' and other_info = '" + oInfo + "'"

        return int(ExecSql().select(sql, 'cnt'))
    
    # 最新のパスワードを取得
    def search(self, app, oInfo):
        sql = "select pwd from " + self.tblpass + " "
        sql = sql + "where no = (select max(no) from " + self.tblpass + " where app = '" + app + "' "
        sql = sql + "and other_info = '" + oInfo + "')"

        return ExecSql().select(sql, 'pwd')
