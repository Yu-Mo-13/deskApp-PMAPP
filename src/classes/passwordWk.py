# coding: UTF-8
from classes.curl import Curl as Curl
from classes.log import Log as Log
from function.config import get_config

class PasswordWk():

    def __init__(self):
        self.rooturl = f"{get_config('CURLURL', 'ROOTURL')}{get_config('CURLURL', 'PASSWORDWKURL')}"
        self.addedurl = ""
        self.insLog = Log()

    def regist(self, pwd, app, oInfo):
        try:
            self.addedurl = f"create?pwd={pwd}&app={app}&other_info={oInfo}"
            insCurl = Curl(f"{self.rooturl}")
            insCurl.post(self.addedurl)

        except Exception as e:
            self.insLog.write('error', str(e))
            return False
        
        return True
    
    # 全件取得
    def selectAll(self):
        try:
            insCurl = Curl(f"{self.rooturl}")
            passwordWkList = insCurl.get()

        except Exception as e:
            self.insLog.write('error', str(e))
            return False
        
        return passwordWkList
    
    def delete(self, app, oInfo):
        try:
            insCurl = Curl(f"{self.rooturl}")
            insCurl.delete(f"?app={app}&other_info={oInfo}")
        
        except Exception as e:
            self.insLog.write('error', str(e))
            return False
        
        return True
    
    def deleteAll(self):
        try:
            insCurl = Curl(f"{self.rooturl}")
            insCurl.deleteAll()
        
        except Exception as e:
            self.insLog.write('error', str(e))
            return False
        
        return True