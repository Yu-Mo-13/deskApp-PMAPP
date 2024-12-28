# coding: UTF-8

from classes.buttonActionBase import ButtonActionBase as ButtonActionBase
from classes.generatePassword import GeneratePassword as GeneratePassword
from classes.passwordWk import PasswordWk as PasswordWk
from classes.log import Log as Log

class GenerateAction(ButtonActionBase):

    def __init__(self, pwd, app, oInfo):
        super().__init__(pwd, app, oInfo)

    def execute(self, length, cmb_val, mode):
        try:
            result = False
            log = Log()

            # 未入力チェック
            if not(length) or not(self.app):
                log.write('error', 'エラー：必須項目未入力')
                return False, '必須項目が入力されていません。'

            # パスワードの生成
            password = GeneratePassword(int(length))

            if mode == cmb_val[0]:
                self.pwd = password.generate()
                log.write('info', 'パスワード作成：記号ありモード')
            elif mode == cmb_val[1]:
                self.pwd = password.generateWithoutSymbol()
                log.write('info', 'パスワード作成：記号なしモード')

            if not(self.pwd):
                log.write('error', 'エラー：パスワード桁数エラー')
                return False, 'パスワード桁数は1以上の数値を入力してください。'
            
            # ワークテーブルにパスワードを登録
            passwordwk = PasswordWk()
            result = passwordwk.regist(self.pwd, self.app, self.oInfo)

            if not(result):
                log.write('error', 'エラー：ワークテーブルへのパスワード登録失敗')
                return False, '必須項目が入力されていません。'
            
            log.write('error', 'パスワード作成：パスワード作成完了')
            return True, self.pwd
        
        except ValueError as e:
            log.write('error', 'エラー：パスワード桁数データ不正')
            return False, 'パスワード桁数は整数を入力してください。'