# coding: UTF-8
from dbLogicBase import DbLogicBase as DbLogicBase
from log import Log as Log

class ExecSql():

    def __init__(self):
        self.insConnection = DbLogicBase('connect')
        self.insLog = Log()
        self.execOutput = False

    def insert(self, sSQL):
        con = self.insConnection.makeConnection()
        with con.cursor() as cur:
            cur.execute(sSQL)
            con.commit()

            self.insLog.write('info', '正常：登録完了')
            self.insLog.write('info', sSQL)

        con.close()

    def select(self, sSQL, target):
        # 最初は結果をFalseにしておく
        # 取得したらFalseから取得結果に変更する
        con = self.insConnection.makeConnection()
        with con.cursor() as cur:
            cur.execute(sSQL)

            # SQL実行結果出力
            results = cur.fetchall()
            if len(results) <= 0:
                self.insLog.write('info', '検索結果なし')
                self.insLog.write('sql', sSQL)
                return self.execOutput
            
            result = results[0]
            self.execOutput = result[target]
            self.insLog.write('info', 'パスワード検索完了')
            self.insLog.write('sql', sSQL)
            return self.execOutput
    
    # 2023/06/25 add issue #7
    # ワークテーブルの削除に使うため追加
    def delete(self, sSQL):
        con = self.insConnection.makeConnection()
        with con.cursor() as cur:
            cur.execute(sSQL)
            con.commit()

            self.insLog.write('info', '正常：ワークテーブル削除完了')
            self.insLog.write('info', sSQL)

        con.close()
