# coding: UTF-8
from log import Log as Log
from connectDatabase import ConnectDatabase as ConnectDatabase

class DbLogicBase():

    def __init__(self, method):
        self.insLog = Log()
        if not(method == 'insert' or method == 'select'):
            self.insLog.writeLog('error', 'エラー：データベース処理')
            return False

        self.method = method
        self.execOutput = False
        return True
    
    def makeConnection(self):
        insConDb = ConnectDatabase()
        return insConDb.makeConnection()
    
    def execInsSql(self, sSQL):
        con = self.makeConnection()
        with con.cursor() as cur:
            cur.execute(sSQL)
            con.commit()

            self.insLog.writeLog('info', '正常：登録完了')
            self.insLog.writeLog('info', sSQL)

        con.close()

    def execSelSql(self, sSQL):
        # 最初は結果をFalseにしておく
        # 取得したらFalseから取得結果に変更する
        con = self.makeConnection()
        with con.cursor() as cur:
            cur.execute(sSQL)

            # SQL実行結果出力
            results = cur.fetchall()
            if len(results) <= 0:
                self.insLog.writeLog('info', '検索結果なし')
                self.insLog.writeLog('sql', sSQL)
                return self.execOutput
            
            result = results[0]
            self.execOutput = result["accountclas"]
            self.insLog.writeLog('info', 'パスワード検索完了')
            self.insLog.writeLog('sql', sSQL)
            return self.execOutput
        
    # パスワードの検検索処理で使われるSQL
    def execSelPassSql(self, sSQL):
        con = self.makeConnection()
        with con.cursor() as cur:
            cur.execute(sSQL)
            results = cur.fetchall()
            if len(results) <= 0:
                self.insLog.writeLog('info', '検索結果なし')
                self.insLog.writeLog('sql', sSQL)
                return self.execOutput
            
            result = results[0]
            self.execOutput = result["pwd"]
            self.insLog.writeLog('info', 'パスワード検索完了')
            self.insLog.writeLog('sql', sSQL)
            return self.execOutput