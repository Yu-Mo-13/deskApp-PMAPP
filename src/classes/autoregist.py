# coding: UTF-8
from classes.curl import Curl as Curl
from classes.log import Log as Log
from function.config import get_config

class AutoRegist():
  def __init__(self):
    root = get_config('CURLURL', 'ROOTURL')
    autoregist_root = get_config('CURLURL', 'AUTOREGISTURL')
    self.rooturl = f"{root}{autoregist_root}"
    self.addedurl = ""
    self.log = Log()
  
  def search(self, app):
    try:
      curl = Curl(f"{self.rooturl}")
      autoregist = curl.get()
    
    except Exception as e:
      self.log.write('error', str(e))
      return False
    
    return autoregist
  
  def delete(self, uuid):
    try:
      self.addedurl = f"delete/uuid={uuid}"
      curl = Curl(f"{self.rooturl}")
      curl.post(self.addedurl)
    
    except Exception as e:
      self.log.write('error', str(e))
      return False
    
    return True