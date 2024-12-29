# coding: UTF-8
from classes.curl import Curl as Curl
from classes.log import Log as Log
from function.config import get_config


class Password:

    def __init__(self):
        self.rooturl = (
            f"{get_config('CURLURL', 'ROOTURL')}{get_config('CURLURL', 'PASSWORDURL')}"
        )
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

    # 最新のパスワードを取得
    def search(self, app, oInfo):
        try:
            curl = Curl(f"{self.rooturl}app={app}/account={oInfo}")
            password = curl.get()

        except Exception as e:
            self.log.write("error", str(e))
            return False

        return password
