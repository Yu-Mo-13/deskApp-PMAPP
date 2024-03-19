# coding: UTF-8

from classes.buttonActionBase import ButtonActionBase as ButtonActionBase
from classes.log import Log as Log
from classes.curl import Curl as Curl
from classes.encryption import Encryption as Encryption
from classes.accountClass import AccountClass as AccountClass
from classes.password import Password as Password
from classes.passwordNoAccount import PasswordNoAccount as PasswordNoAccount
import function.const as CONST

class RegistAction(ButtonActionBase):

    def __init__(self, pwd, app, oInfo):
        super().__init__(pwd, app, oInfo)

    def execute(self):
        isRegisted = False

        # ログ
        insLog = Log()

        if self.pwd == '':
            insLog.write('error', 'エラー：パスワード未入力')
            return False, 'パスワードが入力されていません。'
        
        if self.app == '':
            insLog.write('error', 'エラー：アプリケーション未入力')
            return False, 'アプリケーション名が入力されていません。'
        
        # パスワード登録処理
        # 登録前にアカウント情報が入力済みかチェック
        accountClass = AccountClass().search(self.app)

        if accountClass == CONST.ErrorCode:
            insLog.write('error', 'エラー：アプリケーション未登録')
            return False, 'アプリケーションマスタにアプリを登録してください。'
        
        insEncryption = Encryption()
        encPwd = insEncryption.encrypt(self.pwd)

        tupInsPassword = self.decideSql(accountClass)
        if not(tupInsPassword[0]):
            insLog.write('error', 'エラー：アカウント情報未入力')
            return False, '備考欄にアカウント情報を入力してください。'
        
        isRegisted = tupInsPassword[1].regist(encPwd, self.app, self.oInfo)
        return isRegisted, 'パスワードをデータベースに登録しました。'

    def decideSql(self, accountClass):
        if (accountClass == CONST.NoNeedAccount):
            # アカウント必要区分が「不要」の場合、備考列にNULLが入る
            insPassword = PasswordNoAccount()
            return True, insPassword
        
        if (accountClass == CONST.NeedAccount):
            if (self.oInfo == ''):
                return False, False
            
            insPassword = Password()

        return True, insPassword
