import pymysql
from config import DATABASE

def connect_db():
    db = pymysql.connect(
                        host     = DATABASE['host'],
                        port     = DATABASE['port'],
                        user     = DATABASE['user'],
                        password = DATABASE['password'],
                        database = DATABASE['database'],
                        charset  = DATABASE['charset'],
                        autocommit = False,
                        read_timeout = 20
                        )
    return db
