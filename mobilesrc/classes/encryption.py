# coding: UTF-8

import base64

class Encryption():

    def __init__(self):
        self.code = 'utf-8'

    def encrypt(self, word):
        # パスワードを暗号化
        encPassword = base64.b64encode(word.encode(self.code)).decode(self.code)
        return encPassword
    
    def decrypt(self, word):
        # パスワードを復号化
        decPassword = base64.b64decode(word).decode(self.code)
        return decPassword