# coding: UTF-8
from dbLogicBase import DbLogicBase as DbLogicBase
# import Log

class ManagePasswordLogic(DbLogicBase):

    def __init__(self, method):
        super().__init__(method)

    def regist(self, pwd, app, oInfo, rDate):
        sql = "insert into manage_password.tbl_pwd(pwd, app, other_info, registered_date)"
        sql = sql + " values('" + pwd + "','" + app + "','" + oInfo + "','" + rDate + "')"

        DbLogicBase.execInsSql(self, sql)
        return True

    # 最新のパスワードを取得
    def search(self, app, oInfo):
        sql = "select pwd from manage_password.tbl_pwd "
        sql = sql + "where no = (select max(no) from manage_password.tbl_pwd where app = '" + app + "' "
        sql = sql + "and other_info = '" + oInfo + "')"

        return DbLogicBase.execSelPassSql(self, sql)
