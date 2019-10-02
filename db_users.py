"""Simple work with DataBase."""

import sqlite3
import datetime

DB_NAME = 'users.db'
DB_TABLE_NAME = 'users'


class DataBaseConn:
    """Context Manager, which work with sqlite3."""

    def __init__(self, db_name):
        self._db_name = db_name

    def __enter__(self):
        self._conn = sqlite3.connect(self._db_name)
        return self._conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._conn.commit()
        self._conn.close()
        if exc_val:
            raise


class UsersDB:
    """Class works with DataBase of users."""

    def __init__(self):
        """Constructor.

        Create table 'users' if it isn't exist.

        """
        with DataBaseConn(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(f'''CREATE TABLE if not exists 
                            {DB_TABLE_NAME}
                            (user_id text,
                             first_name text,
                             last_name text,
                             message text,
                             time text)
                            '''
                           )

    @classmethod
    def push_user(cls, about_user: {}, message: str):
        """Push info about user to DataBase.

        :param about_user: info about user, which send msg
        :param message: message, which user send

        """
        sql = '''INSERT INTO {} VALUES
                ('{}','{}','{}','{}', '{}')
              '''.format(DB_TABLE_NAME,
                         about_user.get('id', ''),
                         about_user.get('first_name', ''),
                         about_user.get('last_name', ''),
                         message,
                         datetime.datetime.now()
                         )
        with DataBaseConn(DB_NAME) as conn:
            conn.cursor().execute(sql)
