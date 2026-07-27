import pymssql

from config import DB_CONFIG


class Database:

    def __init__(self):

        self.connection = None
        self.cursor = None

    def __enter__(self):

        self.connection = pymssql.connect(
            server=DB_CONFIG["server"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["database"],
            port=DB_CONFIG["port"],
            as_dict=True
        )

        self.cursor = self.connection.cursor()

        return self

    def __exit__(self, exc_type, exc_value, traceback):

        if exc_type is None:
            self.connection.commit()
        else:
            self.connection.rollback()

        self.cursor.close()
        self.connection.close()

    def execute(self, sql, params=None):

        self.cursor.execute(sql, params or ())

    def executemany(self, sql, params):

        self.cursor.executemany(sql, params)

    def fetch_one(self, sql, params=None):

        self.cursor.execute(sql, params or ())

        return self.cursor.fetchone()

    def fetch_all(self, sql, params=None):

        self.cursor.execute(sql, params or ())

        return self.cursor.fetchall()