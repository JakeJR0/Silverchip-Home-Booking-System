"""
    This file manages the database for the program.
"""

import sqlite3
import re as regex
import os

month_prices = {
    1: 125,
    2: 125,
    3: 125,
    4: 125,
    5: 200,
    6: 200,
    7: 200,
    8: 200,
    9: 150,
    10: 150,
    11: 150,
    12: 150,
}

class DatabaseNamingError(ValueError):
    """
    Used to create a naming error, for the program
    if the database file name is incorrect.
    """

    def __init__(self, *args, **kwargs):
        """
        This is used to initialise the class.
        """
        ValueError.__init__(self, *args, **kwargs)

class Database:
    """
        This class is used to manage the database for the program.
    """
    def save(self):
        """
            This is used to save the database.
        """
        self._connection.commit()

    def __enter__(self):
        """
            This is used to create cursors for the database.
        """
        try:
            self._cursor = self._connection.cursor()
            return self._cursor
        except AttributeError:
            return None

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
            This is used to close cursors for the database.
        """
        try:
            self.save()
            self._cursor.close()
        except AttributeError:
            pass

    def __del__(self):
        """
            This is used to close the database.
        """
        try:
            self._connection.close()
            if self._delete_on_close:
                os.remove(self._file_name)
        except AttributeError:
            pass
        except SystemError:
            pass

    def __init__(self, file_name="database", test_mode=False, delete_on_close=False):
        """
            This is used to initialise the class.
        """
        self._file_name = file_name
        setup = os.path.exists(self._file_name)
        self._cursor = None
        self._delete_on_close = delete_on_close

        if test_mode:
            return

        file_pattern = r"[a-z]*_*^[^.()1-9/\\]+$"

        if not regex.match(file_pattern, self._file_name):
            raise DatabaseNamingError("Database file name is incorrect.")

        if regex.match(r"^$|\s+", self._file_name):
            raise DatabaseNamingError("Database file name contains forbidden characters.")

        if len(self._file_name) <= 3:
            raise DatabaseNamingError("Database file name is too short.")

        if len(self._file_name) >= 20:
            raise DatabaseNamingError("Database file name is too long.")

        self._connection = sqlite3.connect(self._file_name)

        with self as cur:
            cur.execute(
                """
                  CREATE TABLE IF NOT EXISTS users(
                    username CHAR(30) PRIMARY KEY NOT NULL,
                    password CHAR(255) NOT NULL,
                    level INT(1) NOT NULL
                  );
                  """
            )
            cur.execute(
                """
                  CREATE TABLE IF NOT EXISTS  bookings(
                    ID INTEGER PRIMARY KEY NOT NULL,
                    first_name CHAR(20) NOT NULL,
                    last_name CHAR(30) NOT NULL,
                    mobile_number CHAR(11) NOT NULL,
                    email_address CHAR(50) NOT NULL,
                    postcode CHAR(8) NOT NULL,
                    pets INT(1) NOT NULL,
                    start_time CHAR(16) NOT NULL,
                    end_time CHAR(16) NOT NULL
                  );
                  """
            )
            cur.execute(
                """
                  CREATE TABLE IF NOT EXISTS  holiday_prices(
                    month INTEGER(2) PRIMARY KEY NOT NULL,
                    price REAL(5) NOT NULL
                  );
                  """
            )
            if not setup:
                print("Adding data")
                cur.execute(
                    """
                      INSERT INTO users(username, password, level)
                      VALUES(?, ?, ?)
                      """,
                    ("System", "root", 3),
                )

                cur.execute(
                    """
                      INSERT INTO users(username, password, level)
                      VALUES(?, ?, ?)
                      """,
                    ("Admin", "root", 2),
                )

                cur.execute(
                    """
                      INSERT INTO users(username, password, level)
                      VALUES(?, ?, ?)
                      """,
                    ("Guest", "root", 1),
                )

                super_admins = ["JakeJR0", "squashedbanana2", "MStreet5"]

                for admin in super_admins:
                    cur.execute(
                        """
                      INSERT INTO users(username, password, level)
                      VALUES(?, ?, ?)
                      """,
                        (admin, "root", 3),
                    )
                for month_data in month_prices.items():
                    cur.execute(
                        """
                                INSERT INTO holiday_prices(month, price)
                                VALUES(?,?)""",
                        (month_data[0], month_data[1]),
                    )



if __name__ == '__main__':
    db = Database('test.db')
    with db as cursor:
        print(cursor)
        users = cursor.execute('SELECT username FROM users')
        for i in users:
            print(i[0])
