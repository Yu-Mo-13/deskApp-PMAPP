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
        result = False
        log = Log()

        if self.pwd == "":
            log.write("error", "エラー：パスワード未入力")
            return False, "パスワードが入力されていません。"

        if self.app == "":
            log.write("error", "エラー：アプリケーション未入力")
            return False, "アプリケーション名が入力されていません。"

        # パスワード登録処理
        # 登録前にアカウント情報が入力済みかチェック
        account_class = AccountClass().search(self.app)

        if account_class == CONST.ErrorCode:
            log.write("error", "エラー：アプリケーション未登録")
            return False, "アプリケーションマスタにアプリを登録してください。"

        encryption = Encryption()
        enc_pwd = encryption.encrypt(self.pwd)

        password = self.decideSql(account_class)
        if not (password[0]):
            log.write("error", "エラー：アカウント情報未入力")
            return False, "備考欄にアカウント情報を入力してください。"

        result = password[1].regist(enc_pwd, self.app, self.oInfo)
        return result, "パスワードをデータベースに登録しました。"

    def decideSql(self, account_class):
        if account_class == CONST.NoNeedAccount:
            # アカウント必要区分が「不要」の場合、備考列にNULLが入る
            password = PasswordNoAccount()
            return True, password

        if account_class == CONST.NeedAccount:
            if self.oInfo == "":
                return False, False

            password = Password()

        return True, password
