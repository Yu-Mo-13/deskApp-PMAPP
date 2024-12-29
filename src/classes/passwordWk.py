# coding: UTF-8
from classes.curl import Curl as Curl
from classes.log import Log as Log
from function.config import get_config


class PasswordWk:

    def __init__(self):
        root = get_config("CURLURL", "ROOTURL")
        passwordwk_root = get_config("CURLURL", "PASSWORDWKURL")
        self.rooturl = (f"{root}{passwordwk_root}")
        self.addedurl = ""
        self.log = Log()

    def regist(self, pwd, app, oInfo):
        try:
            self.addedurl = f"create?pwd={pwd}&app={app}&other_info={oInfo}"
            curl = Curl(f"{self.rooturl}")
            curl.post(self.addedurl)

        except Exception as e:
            self.log.write("error", str(e))
            return False

        return True

    # 全件取得
    def selectAll(self):
        try:
            curl = Curl(f"{self.rooturl}")
            passwordWk_list = curl.get()

        except Exception as e:
            self.log.write("error", str(e))
            return False

        return passwordWk_list

    def delete(self, app, oInfo):
        try:
            curl = Curl(f"{self.rooturl}")
            curl.delete(f"?app={app}&other_info={oInfo}")

        except Exception as e:
            self.log.write("error", str(e))
            return False

        return True

    def deleteAll(self):
        try:
            curl = Curl(f"{self.rooturl}")
            curl.deleteAll()

        except Exception as e:
            self.log.write("error", str(e))
            return False

        return True
