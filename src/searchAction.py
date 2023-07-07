# coding: UTF-8

from buttonActionBase import ButtonActionBase as ButtonActionBase
from log import Log as Log
from accountClass import AccountClass as AccountClass
from password import Password as Password
from passwordNoAccount import PasswordNoAccount as PasswordNoAccount
from encryption import Encryption as Encryption

class SearchAction(ButtonActionBase):

    def __init__(self, pwd, app, oInfo, rDate):
        super().__init__(pwd, app, oInfo, rDate)

    def execute(self):
        
        # ログ
        insLog = Log()

        if self.app == '':
            insLog.write('error', 'エラー：アプリケーション未登録')
            return False, 'パスワードを検索するアプリケーションを入力してください。'
        
        accountClass = AccountClass('select').search(self.app)

        if not(accountClass):
            insLog.write('error', 'エラー；アプリケーション未登録')
            return False, 'アプリケーションマスタにアプリを登録してください。.'
        
        insPassword = self.decideSql(accountClass)

        if insPassword.count(self.app, self.oInfo) < 1:
            insLog.write('error', '正常：該当パスワードなし')
            return False, '該当するパスワードは見つかりませんでした。'
        
        insEncryption = Encryption()
        decPwd = insEncryption.decrypt(insPassword.search(self.app, self.oInfo))

        return True, decPwd
        
    def decideSql(self, accountClass):
        if (accountClass == '0'):
            # 現時点では、アカウント必要区分が不要の場合は、備考の情報は検索条件として扱っていない
            # 備考の情報の扱いは、今後のアプデで考えていくものとする
            insPassword = PasswordNoAccount('select')
        
        if (accountClass == '1'):
            # アカウント必要区分が「必要」かつ備考欄が未入力の場合、未入力エラーを出す
            insPassword = Password('select')

        return insPassword
