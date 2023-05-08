# coding: UTF-8
from dbLogicBase import DbLogicBase as DbLogicBase
# import Log

class ManageApplicationLogic(DbLogicBase):

    def __init__(self, method):
        super().__init__(method)

    def regist(self, appName, accountClas, rDate):
        sql = "insert into manage_password.tbl_appln(name, accountclas, registered_date)"
        sql = sql + " values('" + appName + "','" + accountClas + "','" + rDate + "')"

        DbLogicBase.execInsSql(self, sql)
        return True

    def search(self, app):
        sql = "select no, name, accountclas, registered_date from manage_password.tbl_appln "
        sql = sql + "where name = '" + app + "'"

        return DbLogicBase.execSelSql(self, sql)

    def getAccountClas(self, app):
        sql = "select accountclas from manage_password.tbl_appln "
        sql = sql + "where name = '" + app + "'"

        return DbLogicBase.execSelSql(self, sql)
