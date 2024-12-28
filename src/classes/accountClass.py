# coding: UTF-8
from classes.curl import Curl as Curl
from classes.log import Log as Log
from function.config import get_config
import function.const as CONST

class AccountClass():

    def __init__(self):
        pass

    def search(self, app):
        try:
            curl = Curl(f"{get_config('CURLURL', 'ROOTURL')}{get_config('CURLURL', 'APPLICATIONLISTURL')}app={app}")
            account_class = curl.get()

        except Exception as e:
            log = Log()
            log.write("error", str(e))
            return CONST.ErrorCode
        return account_class["accountclas"]