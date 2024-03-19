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
            insCurl = Curl(f"{get_config('CURLURL', 'ROOTURL')}{get_config('CURLURL', 'APPLICATIONLISTURL')}app={app}")
            accountClass = insCurl.get()

        except Exception as e:
            insLog = Log()
            insLog.write("error", str(e))
            return CONST.ErrorCode
        return accountClass["accountclas"]