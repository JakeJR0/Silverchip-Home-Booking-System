"""
    This file tests the storage module.
"""

import pytest
from storage import Database, DatabaseNamingError, month_prices

class TestDatabase:
    """
        This is used to test the Database class.
    """
    def test___init__(self):
        """
            This tests the __init__ method.
        """

        # These test the data validation
        # that is applied to the name of
        # the database.

        # This test checks if the class will
        # raise an error if the name is over
        # 20 characters.

        with pytest.raises(DatabaseNamingError):
            assert Database("i" * 21, test_mode=True)

            # This test checks if the database will
            # raise an error if the name is empty.

        with pytest.raises(DatabaseNamingError):
            assert Database("", test_mode=True)

            # This tests if the class will raise an
            # error if the name is 3 characters or
            # less.

        with pytest.raises(DatabaseNamingError):
            assert Database("tes", test_mode=True)

            # This tests if the database raise an error
            # if just restriced characters have been entered
            # into the name.

        with pytest.raises(DatabaseNamingError):
            assert Database("____", test_mode=True)

            # This tests if the database will raise an error
            # if the name includes any mix of both allowed and
            # restricted characters

        with pytest.raises(DatabaseNamingError):
            assert Database("Test_Database", test_mode=True)

        # These test makes sure the database was correctly setup.

        # This test makes sure the System user was added with level 3 access.

        setup_test_db = Database("test", delete_on_close=True)
        found = False
        with setup_test_db as cur:
            rows = cur.execute("SELECT * FROM users WHERE username = 'System'")
            for row in rows:
                message = f"System User level is not at level 3 instead it is at level {str(row[2])}."
                assert (row[2] == 3), message
            found = True

        assert found is True, "System User was not found within the database."

        # This test checks if the database is able to save
        # changes.
        with setup_test_db as cur:
            cur.execute(
                """
                                INSERT INTO users(username, password, level)
                                VALUES(?, ?, ?)
                                """,
                ("test_user", "test", 1),
            )

            saved = setup_test_db.save()

            assert saved is True, "Failed to add a new row into the users table."

        # This test checks to verify the correct
        # prices have been assigned to the prices.
        with setup_test_db as cur:
            for row in cur.execute(
                """SELECT month,
                                                price FROM holiday_prices"""
            ):
                correct_price = month_prices[row[0]]
                assert (
                    row[1] == correct_price
                ), """Incorrect Month Price set in
                                                    the database."""

        del setup_test_db
