import pymysql


def connect_db():
    db = pymysql.connect(
        host='wecode.cyokdecyw78y.ap-northeast-2.rds.amazonaws.com',
        port=3306,
        user='root',
        password='wecode!wecode!',
        database='brandi',
        charset='utf8mb4',
        autocommit=False,
        read_timeout=20,
        db='brandi',
    )

    return db
