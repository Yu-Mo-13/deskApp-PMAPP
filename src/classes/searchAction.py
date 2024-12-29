# coding: UTF-8

from classes.encryption import Encryption as Encryption
from classes.log import Log as Log
from classes.buttonActionBase import ButtonActionBase as ButtonActionBase
from classes.accountClass import AccountClass as AccountClass
from classes.password import Password as Password
from classes.passwordNoAccount import PasswordNoAccount as PasswordNoAccount
import function.const as CONST


class SearchAction(ButtonActionBase):

    def __init__(self, pwd, app, oInfo):
        super().__init__(pwd, app, oInfo)

    def execute(self):
        log = Log()

        if self.app == "":
            log.write("error", "エラー：アプリケーション未登録")
            return False, "パスワードを検索するアプリケーションを入力してください。"

        account_class = AccountClass().search(self.app)

        if account_class == CONST.ErrorCode:
            log.write("error", "エラー；アプリケーション未登録")
            return False, "アプリケーションマスタにアプリを登録してください。"

        password = self.decideSql(account_class)
        if not (password[0]):
            log.write("error", "エラー：アカウント情報未入力")
            return False, "備考欄にアカウント情報を入力してください。"

        # 該当するパスワードテーブルデータを取得
        result = (
            password[1].search(self.app)
            if account_class == CONST.NoNeedAccount
            else password[1].search(self.app, self.oInfo)
        )

        if not (result) or len(result) < 1:
            log.write("error", "正常：該当パスワードなし")
            return False, "該当するパスワードは見つかりませんでした。"

        decrypt_password = Encryption().decrypt(result["pwd"])

        return True, decrypt_password

    def decideSql(self, account_class):
        if account_class == CONST.NoNeedAccount:
            # 現時点では、アカウント必要区分が不要の場合は、備考の情報は検索条件として扱っていない
            password = PasswordNoAccount()

        if account_class == CONST.NeedAccount:
            # アカウント必要区分が「必要」かつ備考欄が未入力の場合、未入力エラーを出す
            if self.oInfo == "":
                return False, False

            password = Password()

        return True, password
