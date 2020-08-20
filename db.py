import sqlite3


class DB:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.get_cursor()
        self.create_db()

    def get_cursor(self):
        return self.connection.cursor()

    def close_db(self):
        self.connection.close()

    def create_db(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS users\
                      (key TEXT, expires_in INTEGER)")
        self.connection.commit()

    def insert_record(self, key, expire_in):
        self.cursor.execute(
            "INSERT INTO users VALUES (?, ?)", (key, expire_in))
        self.connection.commit()
        return self.cursor.lastrowid

    def get_record_by_id(self, id_number):
        self.cursor.execute("SELECT * FROM users WHERE rowid=?", (id_number, ))
        return self.cursor.fetchone()
