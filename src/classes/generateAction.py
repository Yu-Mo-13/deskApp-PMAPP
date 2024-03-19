# coding: UTF-8

from classes.buttonActionBase import ButtonActionBase as ButtonActionBase
from classes.generatePassword import GeneratePassword as GeneratePassword
from passwordWk import PasswordWk as PasswordWk
from classes.log import Log as Log

class GenerateAction(ButtonActionBase):

    def __init__(self, pwd, app, oInfo):
        super().__init__(pwd, app, oInfo)

    def execute(self, length, cmb_val, mode):
        try:
            isRegisted = False

            # ログ
            insLog = Log()

            # パスワードの生成
            insGeneratePassword = GeneratePassword(int(length))

            if mode == cmb_val[0]:
                self.pwd = insGeneratePassword.generate()
                insLog.write('info', 'パスワード作成：記号ありモード')
            elif mode == cmb_val[1]:
                self.pwd = insGeneratePassword.generateWithoutSymbol()
                insLog.write('info', 'パスワード作成：記号なしモード')

            # ワークテーブルにパスワードを登録
            insPassword = PasswordWk()
            isRegisted = insPassword.regist(self.pwd, self.app, self.oInfo)

            if not(isRegisted):
                insLog.write('error', 'エラー：ワークテーブルへのパスワード登録失敗')
                return False, '必須項目が入力されていません。'
            
            insLog.write('error', 'エラー：パスワード作成完了')
            return True, self.pwd
        
        except ValueError as e:
            insLog.write('error', 'エラー：パスワード桁数データ不正')
            return False, 'パスワード桁数は整数を入力してください。'