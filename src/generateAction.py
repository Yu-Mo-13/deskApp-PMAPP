# coding: UTF-8

from buttonActionBase import ButtonActionBase as ButtonActionBase
from generatePassword import GeneratePassword as GeneratePassword
from passwordWk import PasswordWk as PasswordWk
from log import Log as Log

class GenerateAction(ButtonActionBase):

    def __init__(self, pwd, app, oInfo, rDate):
        super().__init__(pwd, app, oInfo, rDate)

    def execute(self, length):
        try:
            isRegisted = False

            # ログ
            insLog = Log()

            # パスワードの生成
            insGeneratePassword = GeneratePassword(length)
            self.pwd = insGeneratePassword.generate()

            # ワークテーブルにパスワードを登録
            insPassword = PasswordWk('insert')
            isRegisted = insPassword.regist(self.pwd, self.app, self.oInfo, self.rDate)

            if not(isRegisted):
                insLog.write('error', 'エラー：ワークテーブルへのパスワード登録失敗')
                return False, '必須項目が入力されていません。'
            
            insLog.write('error', 'エラー：パスワード作成完了')
            return True, self.pwd
        
        except ValueError as e:
            insLog.write('error', 'エラー：パスワード桁数データ不正')
            return False, 'パスワード桁数は整数を入力してください。'