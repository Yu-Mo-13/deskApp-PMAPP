# coding: UTF-8

from classes.encryption import Encryption as Encryption
from classes.log import Log as Log
from classes.buttonActionBase import ButtonActionBase as ButtonActionBase
from classes.accountClass import AccountClass as AccountClass
from classes.password import Password as Password
from classes.passwordNoAccount import PasswordNoAccount as PasswordNoAccount
import function.const as CONST

class SearchAction(ButtonActionBase):

    def __init__(self, pwd, app, oInfo, rDate):
        super().__init__(pwd, app, oInfo, rDate)

    def execute(self):
        
        # ログ
        insLog = Log()

        if self.app == '':
            insLog.write('error', 'エラー：アプリケーション未登録')
            return False, 'パスワードを検索するアプリケーションを入力してください。'
        
        accountClass = AccountClass().search(self.app)

        if accountClass == CONST.ErrorCode:
            insLog.write('error', 'エラー；アプリケーション未登録')
            return False, 'アプリケーションマスタにアプリを登録してください。'
        
        tupInsPassword = self.decideSql(accountClass)
        if not(tupInsPassword[0]):
            insLog.write('error', 'エラー：アカウント情報未入力')
            return False, '備考欄にアカウント情報を入力してください。'

        # 該当するパスワードテーブルデータを取得
        res = tupInsPassword[1].search(self.app) if accountClass == CONST.NoNeedAccount else tupInsPassword[1].search(self.app, self.oInfo)
        
        if len(res) < 1:
            insLog.write('error', '正常：該当パスワードなし')
            return False, '該当するパスワードは見つかりませんでした。'
        
        insEncryption = Encryption()
        decPwd = insEncryption.decrypt(res['pwd'])

        return True, decPwd
        
    def decideSql(self, accountClass):
        if (accountClass == CONST.NoNeedAccount):
            # 現時点では、アカウント必要区分が不要の場合は、備考の情報は検索条件として扱っていない
            insPassword = PasswordNoAccount()
        
        if (accountClass == CONST.NeedAccount):
            # アカウント必要区分が「必要」かつ備考欄が未入力の場合、未入力エラーを出す
            if (self.oInfo == ''):
                return False, False
            
            insPassword = Password()

        return True, insPassword
