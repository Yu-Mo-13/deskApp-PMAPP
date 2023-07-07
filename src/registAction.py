# coding: UTF-8

from buttonActionBase import ButtonActionBase as ButtonActionBase
from log import Log as Log
from application import Application as Application
from accountClass import AccountClass as AccountClass
from encryption import Encryption as Encryption
from password import Password as Password
from passwordNoAccount import PasswordNoAccount as PasswordNoAccount

class RegistAction(ButtonActionBase):

    def __init__(self, pwd, app, oInfo, rDate):
        super().__init__(pwd, app, oInfo, rDate)

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
        accountClass = AccountClass('select').search(self.app)

        if not(accountClass):
            insLog.write('error', 'エラー：アプリケーション未登録')
            return False, 'アプリケーションマスタにアプリを登録してください。'
        
        insEncryption = Encryption()
        encPwd = insEncryption.encrypt(self.pwd)

        tupInsPassword = self.decideSql(accountClass)
        if not(tupInsPassword[0]):
            insLog.write('error', 'エラー：アカウント情報未入力')
            return False, '備考欄にアカウント情報を入力してください。'
        
        isRegisted = tupInsPassword[1].regist(encPwd, self.app, self.oInfo, self.rDate)
        return isRegisted, 'パスワードをデータベースに登録しました。'

    def decideSql(self, accountClass):
        if (accountClass == '0'):
            # アカウント必要区分が「不要」の場合、備考列にNULLが入る
            insPassword = PasswordNoAccount('insert')
            return True, insPassword
        
        if (accountClass == '1'):
            if (self.oInfo == ''):
                return False, False
            
            insPassword = Password('insert')
            return True, insPassword
