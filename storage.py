# Storage.py

# Imports the required modules
import os
import sqlite3

# Price setting for each month
_database_file_extension = "db"
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

    pass


class DatabaseStartUpFailure(SystemError):
    pass


class Database:
    """
    This database object is used to handle
    the connection to the database, this makes
    sure that the database is closed when the instance
    is deleted.

    This could also be used to moderate queries which
    could be useful for security purposes.
    """

    _auto_save = True
    _remove_on_setup_failure = True
    active_count = 0

    @property
    def con(self):
        return self._con

    # Save function, data validation for system errors
    def save(self):
        try:
            self._con.commit()
            return True
        except SystemError:
            return False

    def _setup(self):
        try:
            con = self._con
            con.execute(
                """
                  CREATE TABLE users(
                    username CHAR(30) PRIMARY KEY NOT NULL,
                    password CHAR(255) NOT NULL,
                    level INT(1) NOT NULL
                  );
                  """
            )

            con.execute(
                """
                  CREATE TABLE bookings(
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

            con.execute(
                """
                  CREATE TABLE holiday_prices(
                    month INTEGER(2) PRIMARY KEY NOT NULL,
                    price REAL(5) NOT NULL
                  );
                  """
            )

            con.execute(
                """
                  INSERT INTO users(username, password, level)
                  VALUES(?, ?, ?)
                  """,
                ("System", "root", 3),
            )

            con.execute(
                """
                  INSERT INTO users(username, password, level)
                  VALUES(?, ?, ?)
                  """,
                ("Admin", "root", 2),
            )

            con.execute(
                """
                  INSERT INTO users(username, password, level)
                  VALUES(?, ?, ?)
                  """,
                ("Guest", "root", 1),
            )

            super_admins = ["JakeJR0", "squashedbanana2", "MStreet5"]

            for i in super_admins:
                con.execute(
                    """
                  INSERT INTO users(username, password, level)
                  VALUES(?, ?, ?)
                  """,
                    (i, "root", 3),
                )

            for month_id in month_prices:
                self._con.execute(
                    """
                            INSERT INTO holiday_prices(month, price)
                            VALUES(?,?)""",
                    (month_id, month_prices[month_id]),
                )

            con.commit()

        # Database error handling
        except Exception as e:
            if self._remove_on_setup_failure:
                file = f"{self._db_name}.{_database_file_extension}"
                if os.path.exists(file):
                    os.remove(file)

                if os.path.exists("{}.db-journal".format(self._db_name)):
                    os.remove("{}.db-journal".format(self._db_name))
            print("Database Error: {}".format(e))
            raise DatabaseStartUpFailure(e)

    def __del__(self):
        try:
            if self._auto_save:
                self._con.commit()
            self._con.close()

            if self._delete_on_close:
                file = f"{self._db_name}.{_database_file_extension}"
                if os.path.exists(file):
                    os.remove(file)
        except AttributeError:
            pass

        if not self._test_mode:
            try:
                Database.active_count -= 1
            except AttributeError:
                pass

    def __init__(self, db_name="", test_mode=False, delete_on_close=False):
        self._test_mode = test_mode

        # Slices the name to isolate any extension within the file name.

        file_name_extension = db_name[: -len(_database_file_extension)]

        # Checks if the file extension is present for any
        # of the file extensions below.
        if file_name_extension == ".db":
            # Removes the extension from the file name as this will count
            # towards the data validation.
            db_name = db_name[0:-3]
        if db_name == "":
            error_msg = "No File Name has been provided, "
            error_msg += "please specify a file name."
            raise DatabaseNamingError(error_msg)
        elif len(db_name) > 20:
            error_msg = "File Name provided is longer than 20 characters, "
            error_msg += " please choose a shorter name."
            raise DatabaseNamingError(error_msg)
        elif len(db_name) <= 3:
            raise DatabaseNamingError("File Name provided is too short.")
        elif not db_name.isalpha():
            error_msg = "File Name includes forbidden characters."
            raise DatabaseNamingError(error_msg)

        if test_mode:
            # Stops the code before it creates a database connection.
            return

        setup_file = "{}.{}".format(db_name, _database_file_extension)
        setup = os.path.exists(setup_file)
        self._con = sqlite3.connect(f"{db_name}.{_database_file_extension}")
        self._db_name = db_name
        self._delete_on_close = delete_on_close

        # Run setup if 'not setup'
        if not setup:
            self._setup()

        Database.active_count += 1
