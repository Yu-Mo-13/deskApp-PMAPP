# coding: UTF-8
from dbLogicBase import DbLogicBase as DbLogicBase

class ManagePasswordLogicNoAccount(DbLogicBase):

    def __init__(self, method):
        super().__init__(method)

    def regist(self, pwd, app, rDate):
        sql = "insert into manage_password.tbl_pwd(pwd, app, other_info, registered_date)"
        sql = sql + " values('" + pwd + "','" + app + "', null ,'" + rDate + "')"

        DbLogicBase.execInsSql(self, sql)
        return True

    # 最新のパスワードを取得
    def search(self, app):
        sql = "select pwd from manage_password.tbl_pwd "
        sql = sql + "where no = (select max(no) from manage_password.tbl_pwd where app = '" + app + "')"

        return DbLogicBase.execSelPassSql(self, sql)
