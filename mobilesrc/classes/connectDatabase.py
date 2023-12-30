# coding: UTF-8
import psycopg2 as pg
from function.config import get_config

class ConnectDatabase:

    def __init__(self):
        self.conn = None
        self.host = get_config("DATABASE", "HOST")
        self.port = get_config("DATABASE", "PORT")
        self.dbname = get_config("DATABASE", "NAME")
        self.user = get_config("DATABASE", "USER")
        self.password = get_config("DATABASE", "PASSWORD")

    def make_connection(self):
        try:
            self.conn = pg.connect(
                host=self.host, 
                port=self.port, 
                dbname=self.dbname, 
                user=self.user, 
                password=self.password
            )
            print("接続成功")
        except Exception as e:
            print(e)