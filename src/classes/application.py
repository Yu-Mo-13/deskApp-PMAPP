# coding: UTF-8
from classes.curl import Curl as Curl
from classes.log import Log as Log
from function.config import get_config


class Application:
    def __init__(self):
        root = get_config("CURLURL", "ROOTURL")
        application_root = get_config("CURLURL", "APPLICATIONURL")

        self.rooturl = f"{root}{application_root}"
        self.addedurl = ""
        self.log = Log()

    def regist(self, app_name, account_class, notice_class, mark_class, auto_size):
        try:
            params = {
                "app_name": f"name={app_name}",
                "account_class": f"accountclass={account_class}",
                "notice_class": f"noticeclass={notice_class}",
                "mark_class": f"markclass={mark_class}",
                "auto_size": f"autosize={auto_size}",
            }
            self.addedurl = f"create?{'&'.join(params.values())}"
            curl = Curl(f"{self.rooturl}")
            curl.post(self.addedurl)

        except Exception as e:
            self.log.write("error", str(e))
            return False

        return True

    def update(self, no, app_name, account_class, notice_class, mark_class, auto_size):
        try:
            params = {
                "no": f"no={no}",
                "app_name": f"name={app_name}",
                "account_class": f"accountclass={account_class}",
                "notice_class": f"noticeclass={notice_class}",
                "mark_class": f"markclass={mark_class}",
                "auto_size": f"autosize={auto_size}",
            }
            self.addedurl = f"update?{'&'.join(params.values())}"
            curl = Curl(f"{self.rooturl}")
            curl.post(self.addedurl)

        except Exception as e:
            self.log.write("error", str(e))
            return False

        return True

    def search(self, app_name):
        try:
            curl = Curl(f"{self.rooturl}search/app={app_name}")
            application = curl.get()

        except Exception as e:
            self.log.write("error", str(e))
            return False

        return application
