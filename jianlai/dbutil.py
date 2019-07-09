import pymysql

class DbOperate():
    def __init__(self, conn):
        self.conn = conn

    def get_chapter(self):
        cursor = self.conn.cursor()
        cursor.execute("select chapter from notice")
        return cursor.fetchone()[0]

    def update_chapter(self, chapter):
        cursor = self.conn.cursor()
        sql = "update notice set chapter = %d " % chapter
        cursor.execute(sql)
        self.conn.commit()

    def close(self):
        self.conn.close();

class Dbconn():
    def __init__(self, config):
        url = config.get("DataSource", "url")
        username = config.get("DataSource", "username")
        password = config.get("DataSource", "password")
        database = config.get("DataSource", "database")
        self.conn = pymysql.connect(url, username, password, database)

    def get_conn(self):
        return self.conn
